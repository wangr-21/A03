import base64
from collections import Counter
from pathlib import Path

from PIL import Image

from ..constant import ASSETS_DIR
from .utils import CompletionMessage, get_openai_client, run_sync

ASSETS_ROOT = ASSETS_DIR / "style_transfer"
UPLOADS_DIR = ASSETS_ROOT / "uploads"
GENERATED_DIR = ASSETS_ROOT / "generated"

UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
GENERATED_DIR.mkdir(parents=True, exist_ok=True)


def is_valid_image(file_path: Path) -> bool:
    """验证文件是否为有效图片"""
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False


def extract_dominant_colors(
    image_path: Path, num_colors: int = 5
) -> list[dict[str, float | str]]:
    """提取图片中的主要颜色及其占比"""
    try:
        # 打开图片并转换为RGB模式
        img = Image.open(image_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        # 缩小图片以加快处理速度，同时保留细节
        img = img.resize((150, 150))
        pixels = list(img.getdata())
        # 将RGB转换为HEX格式并计数
        hex_colors = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in pixels]
        color_counter = Counter(hex_colors)
        total_pixels = len(pixels)
        dominant_colors: list[dict[str, float | str]] = []
        for color, count in color_counter.most_common(num_colors * 2):
            percentage = round((count / total_pixels) * 100, 1)
            if percentage >= 1:
                dominant_colors.append({"hex": color, "percentage": percentage})
            if len(dominant_colors) >= num_colors:
                break
        if not dominant_colors and color_counter:
            color, count = color_counter.most_common(1)[0]
            percentage = round((count / total_pixels) * 100, 1)
            dominant_colors.append({"hex": color, "percentage": percentage})
        return dominant_colors
    except Exception:
        return []


@run_sync
def analyze_image_emotion(
    image_path: Path, colors: list[dict[str, float | str]], word_count: int
) -> str:
    """使用OpenAI API分析图片情感"""
    try:
        client, model_name = get_openai_client()
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        color_info = "\n".join(
            [f"- {color['hex']} 占比{color['percentage']}%" for color in colors]
        )
        prompt = (
            f"请分析这张图片的色彩情感，生成约{word_count}字的分析文本。\n"
            f"图片中的主要颜色及占比如下：\n"
            f"{color_info}\n\n"
            "请从色彩心理学角度分析这些颜色传递的情感和氛围，并描述它们在整体画面中的作用。\n"
            "回答格式要求：直接输出分析文本，不要包含任何前缀或标题。"
        )

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                CompletionMessage()
                .text(prompt)
                .image(f"data:image/jpeg;base64,{base64_image}")
                .build()
            ],
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        return f"分析过程中出现错误: {e}"
