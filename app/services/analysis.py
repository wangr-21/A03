import io
import json
from collections import Counter

from fastapi import HTTPException
from PIL import Image

from ..constant import ASSETS_DIR
from .utils import CompletionMessage, get_openai_client, run_sync

ASSETS_ROOT = ASSETS_DIR / "analysis"
PROMPT_ANALYZE_COLOR = ASSETS_ROOT / "color.md"


def extract_dominant_colors(
    image: bytes, num_colors: int = 5
) -> list[dict[str, float | str]]:
    """提取图片中的主要颜色及其占比"""

    try:
        # 打开图片并转换为RGB模式
        img = Image.open(io.BytesIO(image))
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


async def analyze_image_emotion(
    image: bytes, colors: list[dict[str, float | str]]
) -> dict[str, object]:
    """使用OpenAI API分析图片情感"""

    color_info = "\n".join(
        f"- {color['hex']} 占比{color['percentage']}%" for color in colors
    )
    prompt = PROMPT_ANALYZE_COLOR.read_text(encoding="utf-8").replace(
        "{{color_info}}", color_info
    )

    client, model_name = get_openai_client()

    try:
        response = await run_sync(client.chat.completions.create)(
            model=model_name,
            messages=[CompletionMessage().text(prompt).image(image).build()],
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="分析图片情感失败，请稍后再试",
        ) from e

    content = response.choices[0].message.content or ""
    if not content:
        raise HTTPException(
            status_code=500,
            detail="分析结果为空，请稍后再试",
        )

    try:
        return json.loads(content[content.find("{") : content.rfind("}") + 1])
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail="分析结果格式错误，请稍后再试",
        ) from e
