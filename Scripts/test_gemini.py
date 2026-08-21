import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


BASE_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

print("API KEY FOUND:", bool(api_key))

if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found")


client = genai.Client(
    api_key=api_key
)


response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Answer in one sentence: What is ischemic stroke?"
)


print("\nGemini response:")
print(response.text)