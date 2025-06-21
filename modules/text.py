import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import ast

load_dotenv()

def make_text(topic):
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = (
        f"Create a line-by-line YouTube Shorts narration script about '{topic}'. "
        "Make it super engaging, fun, and snappy. Keep each line short and punchy. "
        "Return the full script as a valid Python list of strings like: "
        "['line1', 'line2', 'line3'] with no markdown or explanation. JUST the list."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(response_modalities=["TEXT"])
    )

    raw = response.text.strip()

    try:
        return ast.literal_eval(raw)
    except:
        # fallback: split manually if Gemini replies like a clown
        lines = [line.strip("-• \n") for line in raw.split("\n") if line.strip()]
        return lines
