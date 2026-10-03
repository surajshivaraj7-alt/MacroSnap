from google import genai
from google.genai import types
import streamlit as st
import time
from prompts import SYSTEM_PROMPT

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])


def analyze_food(text=None, image=None):

    if image:
        image_bytes = image.getvalue()

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=image.type
        )

        contents = [
            SYSTEM_PROMPT,
            image_part,
            "Analyze this food photo and estimate the calories and macros."
        ]

    else:
        contents = f"{SYSTEM_PROMPT}\n\nUser's meal:\n{text}"

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=contents
            )

            return response.text

        except Exception as e:
            if "503" in str(e) and attempt < 2:
                time.sleep(3)
            else:
                raise