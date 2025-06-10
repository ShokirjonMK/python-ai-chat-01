import requests


def generate_llm_response(prompt: str) -> str:
    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": "Faqat o'zbek tilida javob ber. Savol: " + prompt,
                "stream": False
            },
            timeout=300
        )
        data = res.json()
        return data.get("response", "Kechirasiz, LLM javob bera olmadi.")
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"
