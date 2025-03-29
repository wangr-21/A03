import base64
import json
import random
import uuid
import zipfile

import jinja2

from ..constant import ASSETS_DIR, CACHE_DIR
from . import fleep
from .utils import CompletionMessage, get_openai_client, run_sync

ASSETS_ROOT = ASSETS_DIR / "teaching_plan"
PROMPT_GENERATE = ASSETS_ROOT / "generate.md"
PROMPT_CONVERT = ASSETS_ROOT / "convert.md"
DOCUMENT_XML_TEMPLATE = ASSETS_ROOT / "document.xml.jinja2"
DOCUMENT_TEMPLATE_DIR = ASSETS_ROOT / "template"


def _convert_images(images: list[bytes]) -> list[str]:
    result: list[str] = []
    for raw in images:
        info = fleep.get(raw[:256])
        if not info.mime or not any("image" in mime for mime in info.mime):
            raise ValueError("Invalid image format")
        encoded = base64.b64encode(raw).decode("utf-8")
        result.append(f"data:{info.mime[0]};base64,{encoded}")
    return result


class TeachingPlanGenerator:
    def __init__(self) -> None:
        self.client, self.model_name = get_openai_client()

    @run_sync
    def generate(self, grade: str, images: list[bytes]) -> str:
        prompt = PROMPT_GENERATE.read_text("utf-8")
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                CompletionMessage()
                .text(prompt.replace("{{grade}}", grade))
                .images(_convert_images(images))
                .build()
            ],
        )
        result = response.choices[0].message.content or ""
        return result[result.find("#") :]

    @run_sync
    def _convert_json(self, content: str):
        prompt = PROMPT_CONVERT.read_text("utf-8")
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                CompletionMessage().text(prompt.replace("{{content}}", content)).build()
            ],
        )
        output = response.choices[0].message.content or ""
        return output[output.find("{") : output.rfind("}") + 1]

    def _render_document(self, data: dict[str, object]):
        data["enumerate"] = lambda it: enumerate(it, 1)
        data["paraId"] = lambda: "".join(random.choices("0123456789ABCDEF", k=8))
        template: jinja2.Template = jinja2.Template(
            DOCUMENT_XML_TEMPLATE.read_text("utf-8")
        )
        return template.render(data)

    def _pack_docx(self, document: str):
        output_file = CACHE_DIR / f"{uuid.uuid4()}.docx"
        with zipfile.ZipFile(output_file, "w") as docx:
            docx.writestr("word/document.xml", document)
            for file in DOCUMENT_TEMPLATE_DIR.glob("**/*"):
                if file.is_file() and file.name != "document.xml":
                    docx.write(file, file.relative_to(DOCUMENT_TEMPLATE_DIR))
        return output_file

    async def convert(self, teaching_plan: str):
        converted_json = await self._convert_json(teaching_plan)
        if not converted_json:
            raise ValueError(
                "API returned empty content when converting teaching plan to JSON"
            )

        try:
            data = json.loads(converted_json)
        except json.JSONDecodeError as err:
            raise ValueError("Failed to parse JSON content from API response") from err

        document = self._render_document(data)
        return self._pack_docx(document)
