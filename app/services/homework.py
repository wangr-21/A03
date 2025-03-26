import base64
import json
from pathlib import Path

from ..constant import ASSETS_DIR
from .utils import CompletionMessage, get_openai_client, run_sync

ASSETS_ROOT = ASSETS_DIR / "homework"
PROMPT = ASSETS_ROOT / "prompt.md"


@run_sync
def generate_homework_feedback(image_path: Path):
    prompt = PROMPT.read_text("utf-8")
    client, model_name = get_openai_client()
    image = base64.b64encode(image_path.read_bytes()).decode()

    response = client.chat.completions.create(
        model=model_name,
        messages=[CompletionMessage().text(prompt).image(image).build()],
    )
    output = response.choices[0].message.content or ""

    raw_json = output[output.find("{") : output.rfind("}") + 1]
    if not raw_json:
        raise ValueError("Failed to generate feedback")

    try:
        feedback = json.loads(raw_json)
        return float(feedback["score"]), str(feedback["comment"])
    except Exception as err:
        raise ValueError("Failed to parse feedback") from err
