"""Quick import test for required packages."""

def test_imports():
    failures = []
    try:
        import google.generativeai as genai
    except Exception as e:
        failures.append(f"google.generativeai: {e}")
    try:
        from dotenv import load_dotenv
    except Exception as e:
        failures.append(f"python-dotenv: {e}")
    try:
        import chromadb
    except Exception as e:
        failures.append(f"chromadb: {e}")
    try:
        from sentence_transformers import SentenceTransformer
    except Exception as e:
        failures.append(f"sentence-transformers: {e}")
    try:
        import numpy as np
    except Exception as e:
        failures.append(f"numpy: {e}")
    try:
        import torch
    except Exception as e:
        failures.append(f"torch: {e}")

    if failures:
        print("Import failures:")
        for f in failures:
            print(" -", f)
        return 1

    print("All imports ok")
    return 0

if __name__ == "__main__":
    raise SystemExit(test_imports())
