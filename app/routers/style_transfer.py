from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import FileResponse

from ..services.style_transfer import StyleTransferResponse, StyleTransferService

router = APIRouter(prefix="/style-transfer", tags=["style-transfer"])
service = StyleTransferService()


@router.post("/generate")
async def generate_styled_image(
    file: UploadFile = File(...), style_prompt: str = Form(...)
):
    """处理图片风格转换请求并直接返回生成的图片"""
    # 验证文件格式
    if not file.filename or "." not in file.filename:
        return StyleTransferResponse(
            code=0, msg="文件格式无效", data={"status": "failed"}
        )

    ext = file.filename.rsplit(".", 1)[1].lower()
    if ext not in {"png", "jpg", "jpeg"}:
        return StyleTransferResponse(
            code=0, msg="仅支持PNG/JPG格式", data={"status": "failed"}
        )

    # 验证风格提示词
    if not style_prompt:
        return StyleTransferResponse(
            code=0, msg="风格提示词不能为空", data={"status": "failed"}
        )

    result = await service.generate_styled_image(file, style_prompt)

    # 如果生成失败，返回错误响应
    if result.code != 1:
        return result

    # 生成成功，直接返回图片文件
    file_path = service.generated_dir / result.data["resultUrl"].split("/")[-1]
    return FileResponse(file_path, media_type="image/png")
