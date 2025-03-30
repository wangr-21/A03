import os
import uuid
from datetime import datetime
from io import BytesIO
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image
from pydantic import BaseModel


class StyleTransferResponse(BaseModel):
    code: int
    msg: str
    data: dict


class StyleTransferService:
    def __init__(self):
        self.assets_dir = Path("app/assets/style_transfer")
        self.uploads_dir = self.assets_dir / "uploads"
        self.generated_dir = self.assets_dir / "generated"

        # 创建必要的目录
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        self.generated_dir.mkdir(parents=True, exist_ok=True)

        # 初始化Gemini客户端
        try:
            self.client = genai.Client(api_key=os.environ["OPENAI_API_KEY"])
            self.GEMINI_MODEL = "gemini-2.0-flash-exp-image-generation"
        except Exception as e:
            raise RuntimeError(f"Gemini API初始化失败: {str(e)}")

    def is_valid_image(self, file_path: Path) -> bool:
        """验证文件是否为有效图片"""
        try:
            with Image.open(file_path) as img:
                img.verify()
            return True
        except Exception:
            return False

    async def generate_styled_image(
        self, image_file, style_prompt: str
    ) -> StyleTransferResponse:
        """处理图片风格转换请求"""
        try:
            # 生成唯一文件名
            unique_id = str(uuid.uuid4())
            ext = image_file.filename.rsplit(".", 1)[1].lower()
            upload_filename = f"{unique_id}.{ext}"
            upload_path = self.uploads_dir / upload_filename

            # 保存上传文件
            with upload_path.open("wb") as f:
                f.write(image_file.file.read())

            # 验证图片有效性
            if not self.is_valid_image(upload_path):
                upload_path.unlink()  # 删除无效文件
                return StyleTransferResponse(
                    code=0, msg="上传的图片文件已损坏", data={"status": "failed"}
                )

            # 调用Gemini API生成风格化图片
            try:
                # 打开图片
                image = Image.open(upload_path)

                # 构建提示词
                text_input = f"请将这张图片转换为以下风格: {style_prompt}"

                # 调用Gemini API
                response = self.client.models.generate_content(
                    model=self.GEMINI_MODEL,
                    contents=[text_input, image],
                    config=types.GenerateContentConfig(
                        response_modalities=["Text", "Image"]
                    ),
                )

                # 处理响应
                generated_image = None
                for part in response.candidates[0].content.parts:
                    if part.inline_data is not None:
                        generated_image = Image.open(BytesIO(part.inline_data.data))
                        break

                if generated_image is None:
                    return StyleTransferResponse(
                        code=0, msg="AI生成图片失败", data={"status": "failed"}
                    )

                # 保存生成的图片
                output_filename = f"styled_{unique_id}.png"
                output_path = self.generated_dir / output_filename
                generated_image.save(output_path, format="PNG")

                return StyleTransferResponse(
                    code=1,
                    msg="生成成功",
                    data={
                        "status": "completed",
                        "resultUrl": f"/api/style-transfer/generated/{output_filename}",
                    },
                )

            except Exception as e:
                error_str = str(e).lower()
                if "timeout" in error_str:
                    return StyleTransferResponse(
                        code=1001, msg="AI生成超时", data={"status": "failed"}
                    )
                elif "style" in error_str or "prompt" in error_str:
                    return StyleTransferResponse(
                        code=1002,
                        msg="风格不支持或提示词无效",
                        data={"status": "failed"},
                    )
                else:
                    return StyleTransferResponse(
                        code=0, msg=f"AI处理失败: {str(e)}", data={"status": "failed"}
                    )

        except Exception as e:
            return StyleTransferResponse(
                code=0, msg=f"处理请求失败: {str(e)}", data={"status": "failed"}
            )
