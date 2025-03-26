import base64
import io
import json
import random

import fleep
import jinja2

from ..constant import ASSETS_DIR
from .utils import CompletionMessage, get_openai_client, run_sync

ASSETS_ROOT = ASSETS_DIR / "teaching_plan"
PROMPT_GENERATE = ASSETS_ROOT / "generate.md"
PROMPT_CONVERT = ASSETS_ROOT / "convert.md"
DOCUMENT_XML_TEMPLATE = ASSETS_ROOT / "document.xml.jinja2"
DOCUMENT_TEMPLATE_DIR = ASSETS_ROOT / "template"


def _convert_images(images: list[str]) -> list[str]:
    result: list[str] = []
    for raw in images:
        info = fleep.get(base64.b64decode(raw[:344]))
        if not info.mime or not any("image" in mime for mime in info.mime):
            raise ValueError("Invalid image format")
        result.append(f"data:image/png;base64,{raw}")
    return result


class TeachingPlanGenerator:
    def __init__(self) -> None:
        self.client, self.model_name = get_openai_client()

    @run_sync
    def generate(self, grade: str, images: list[str]) -> str:
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
        return response.choices[0].message.content or ""

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
        import zipfile

        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as docx:
            docx.writestr("word/document.xml", document)
            for file in DOCUMENT_TEMPLATE_DIR.glob("**/*"):
                if file.is_file() and file.name != "document.xml":
                    docx.write(file, file.relative_to(DOCUMENT_TEMPLATE_DIR))

        buffer.seek(0)
        return buffer.read()

    @run_sync
    def convert(self, teaching_plan: str):
        converted_json = self._convert_json(teaching_plan)
        if not converted_json:
            raise ValueError(
                "API returned empty content when converting teaching plan to JSON"
            )

        try:
            data = json.loads(converted_json)
        except json.JSONDecodeError:
            raise ValueError("Failed to parse JSON content from API response")

        document = self._render_document(data)
        return self._pack_docx(document)
