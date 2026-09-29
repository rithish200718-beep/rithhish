import os

from dotenv import load_dotenv
from google import genai


# Load .env file
load_dotenv()


# Read environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)


# --------------------------------------------------
# Create Gemini client
# --------------------------------------------------

client = None

if GEMINI_API_KEY:

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


# --------------------------------------------------
# Check Gemini availability
# --------------------------------------------------

def gemini_available():

    return client is not None


# --------------------------------------------------
# Generate text
# --------------------------------------------------

def generate_text(
    prompt: str,
    temperature: float = 0.4
) -> str:

    if client is None:

        raise RuntimeError(
            "Gemini API is not configured. "
            "Please add GEMINI_API_KEY to your .env file."
        )

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={
                "temperature": temperature
            }
        )

        text = getattr(
            response,
            "text",
            None
        )

        if not text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text.strip()

    except Exception as error:

        raise RuntimeError(
            f"Gemini API error: {error}"
        ) from error