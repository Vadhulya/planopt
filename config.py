from google import generativeai as genai

# ----------------------------------------
#  HARD-CODED API KEY (works instantly)
# ----------------------------------------
API_KEY = ""

if not API_KEY or API_KEY.strip() == "":
    raise ValueError("ERROR: API KEY is empty. Please insert your Gemini API key in config.py")

# Configure Gemini
genai.configure(api_key=API_KEY)

