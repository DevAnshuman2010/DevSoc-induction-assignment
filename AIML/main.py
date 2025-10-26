import os
import json
import requests
import sys
from dotenv import load_dotenv

HF_TOKEN = "your key here" 
API_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL = "meta-llama/Meta-Llama-3-8B-Instruct" 
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}
INPUT_FILE = "input.txt"
OUTPUT_FILE = "output.json"

def query(prompt):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]

    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    
    if response.status_code != 200:
        return f"Error {response.status_code}: {response.text}"

    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Unexpected response format: {response.text}"

def main():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            prompts = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ ERROR: Input file '{INPUT_FILE}' not found. Create it with prompts inside.")
        sys.exit(1)

    results = []
    for i, prompt in enumerate(prompts, start=1):
        print(f"[{i}/{len(prompts)}] Querying model for: {prompt}")
        llm_output = query_llm(prompt)
        results.append({
            "prompt_text": prompt,
            "llm_output": llm_output
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n✅ All responses saved to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()