from google.genai import types

MARK_DOWN_CONFIG = (
    "Отвечай обычным текстом.\n"
    "Не используй Markdown.\n"
    "Не используй заголовки.\n"
    "Не используй списки.\n"
    "Не используй ссылки в формате Markdown."
)

def create_config(
        max_tokens: int = 2500,
) -> types.GenerateContentConfig:
        return types.GenerateContentConfig(
            system_instruction=(
                MARK_DOWN_CONFIG
            ),
            max_output_tokens=max_tokens,
        )
