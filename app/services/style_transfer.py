import os
import uuid
from io import BytesIO
from pathlib import Path

from fastapi import HTTPException
from google import genai
from google.genai import types
from PIL import Image

from ..constant import CACHE_DIR
from .utils import run_sync

GEMINI_MODEL = "gemini-2.0-flash-exp-image-generation"
STYLED_CACHE_DIR = CACHE_DIR / "styled"
STYLED_CACHE_DIR.mkdir(parents=True, exist_ok=True)


class StyleTransferService:
    def __init__(self) -> None:
        # 初始化Gemini客户端
        try:
            self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        except Exception as e:
            raise RuntimeError(f"Gemini API初始化失败: {e}") from e

    async def generate_styled_image(
        self,
        image: bytes,
        style_prompt: str,
    ) -> Path:
        """处理图片风格转换请求"""

        # 调用Gemini API生成风格化图片
        response = await run_sync(self.client.models.generate_content)(
            model=GEMINI_MODEL,
            contents=[
                f"请将这张图片转换为以下风格: \n{style_prompt}",
                Image.open(BytesIO(image)),
            ],
            config=types.GenerateContentConfig(response_modalities=["Text", "Image"]),
        )

        if (
            not response.candidates
            or not (content := response.candidates[0].content)
            or not content.parts
        ):
            raise HTTPException(status_code=500, detail="AI 响应内容无效")

        # 处理响应
        for part in content.parts:
            if part.inline_data is not None and part.inline_data.data is not None:
                generated = Image.open(BytesIO(part.inline_data.data))
                output_path = STYLED_CACHE_DIR / f"{uuid.uuid4()}.png"
                generated.save(output_path, format="PNG")
                return output_path
        else:
            raise HTTPException(status_code=500, detail="AI 生成图片失败")
