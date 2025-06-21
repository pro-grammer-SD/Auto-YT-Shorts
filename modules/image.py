import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

load_dotenv()

def make_image(prompt, index):
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"]
        )
    )

    if not response or not response.candidates:
        print(f"[Image Error #{index}] No response/candidates for prompt: {prompt}")
        return

    candidate = response.candidates[0]
    if not candidate.content or not hasattr(candidate.content, "parts"):
        print(f"[Image Error #{index}] No content parts returned for prompt: {prompt}")
        return

    for part in candidate.content.parts:
        if part.inline_data:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(f"image_{index}.png")
        elif part.text:
            print(f"[Image Info #{index}]: {part.text}")
            