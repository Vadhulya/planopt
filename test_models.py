import google.generativeai as genai

API_KEY = "AIzaSyB_pnIk_Njc1cXLUbrrmXmpDmwvWjGVtqI"  

genai.configure(api_key=API_KEY)

models = genai.list_models()

for m in models:
    print(m.name)
