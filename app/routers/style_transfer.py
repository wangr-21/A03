from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from ..services import fleep
from ..services.style_transfer import StyleTransferService

router = APIRouter(prefix="/style-transfer", tags=["style-transfer"])
service = StyleTransferService()


@router.post("/generate", response_class=FileResponse)
async def generate_styled_image(
    style_prompt: str = Form(...),
    file: UploadFile = File(...),
) -> FileResponse:
    """处理图片风格转换请求并直接返回生成的图片"""
    # 验证风格提示词
    if not style_prompt:
        raise HTTPException(status_code=400, detail="风格提示词不能为空")

    head = await file.read(256)
    info = fleep.get(head)
    if not info or not info.mime:
        raise HTTPException(status_code=400, detail="文件格式无效")
    content = head + await file.read()

    try:
        file_path = await service.generate_styled_image(content, style_prompt)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"处理请求失败: {e}",
        ) from e
    else:
        return FileResponse(file_path, media_type="image/png")
