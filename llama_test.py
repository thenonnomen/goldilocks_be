import requests
import base64

url_encoded = "aHR0cHM6Ly9vcGVucm91dGVyLmFpL2FwaS92MS9jaGF0L2NvbXBsZXRpb25z"
url = base64.b64decode(url_encoded).decode()

API_KEY = "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"

def query_openrouter(model_name, prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error with model {model_name}: {response.status_code} - {response.text}"


prompt = """Find mid-sized Indian food brands with >60% revenue from general trade and low digital penetration.
          After insights, provide the data in the following columns format :
          Company Name	Company Domain	headquarters	Description	Revenue CEO	founded	employees"""

models = ["mistralai/devstral-small:free", "deepseek/deepseek-chat:free", "meta-llama/llama-3.3-8b-instruct:free", "meta-llama/llama-4-maverick:free"]  # Add more if needed

for model in models:
    print(f"\n🔹 Response from {model}:\n")
    print(query_openrouter(model, prompt))