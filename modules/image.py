from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from rich.console import Console
from utils.roqe import retry_on_quota_error

load_dotenv()
console = Console()

@retry_on_quota_error
def make_image(prompt, index):
    client = genai.Client()

    console.print(f"🧠 [cyan]Generating image for prompt #{index}[/cyan]: [italic]\"{prompt}\"[/italic]")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"]
            )
        )
    except Exception as e:
        console.print(f"[red]❌ API error while generating image #{index}[/red]: {e}")
        return

    if not response or not response.candidates:
        console.print(f"[red]🚫 No response/candidates for image #{index}[/red]")
        return

    candidate = response.candidates[0]
    if not candidate.content or not hasattr(candidate.content, "parts"):
        console.print(f"[red]🚫 No valid content parts in image #{index}[/red]")
        return

    found_image = False
    for part in candidate.content.parts:
        if part.inline_data:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(f"image_{index}.png")
            console.print(f"[green]✅ Saved image_{index}.png[/green]")
            found_image = True
        elif part.text:
            console.print(f"[yellow]💬 Response Text #{index}:[/yellow] {part.text}")

    if not found_image:
        console.print(f"[red]❗ No image data returned for #{index}[/red]")
