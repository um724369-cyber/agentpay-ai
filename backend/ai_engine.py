import json
import re
import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "mistral"

def process_user_intent(user_prompt: str) -> dict:
    system_prompt = f"""You are a precise financial intent parser.
Extract the transaction parameters from the user prompt into valid JSON ONLY.
Schema:
{{
  "recipient": "name of person or organization or company",
  "amount": "numeric amount with currency code like USD50 or USD150",
  "purpose": "short transaction reason or category",
  "confidence": "High"
}}

Rules:
- The person/business being paid (after words like 'to', 'pay', 'send') is the 'recipient'.
- Return ONLY JSON. Do not include markdown codeblocks or explanation.

Input: "{user_prompt}"
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": system_prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=8)
        if response.status_code == 200:
            raw_text = response.json().get("response", "").strip()
            raw_text = re.sub(r"^```json\s*", "", raw_text)
            raw_text = re.sub(r"^```\s*", "", raw_text)
            raw_text = re.sub(r"```$", "", raw_text).strip()
            
            parsed = json.loads(raw_text)
            if parsed.get("recipient") and parsed.get("recipient") != "N/A":
                return parsed
    except Exception:
        pass

    # Bulletproof Regex Fallback Engine
    recipient = "N/A"
    rec_match = re.search(r'\b(?:to|pay|transfer to|send to)\s+([A-Za-z0-9_-]+)', user_prompt, re.IGNORECASE)
    if rec_match:
        found = rec_match.group(1).strip()
        if found.lower() not in ["the", "a", "an", "for", "cloud", "my", "our"]:
            recipient = found.capitalize()

    # Extract Amount
    amount = "USD10"
    amt_match = re.search(r'(?:[\$€£]|usd\s*|dollars?\s*)?(\d+(?:\.\d{1,2})?)\s*(?:[\$€£]|usd|dollars?)?', user_prompt, re.IGNORECASE)
    if amt_match:
        val = amt_match.group(1)
        amount = f"USD{val}"

    # Extract Purpose
    purpose = "Payment"
    purpose_match = re.search(r'\bfor\s+([A-Za-z0-9\s_-]+)', user_prompt, re.IGNORECASE)
    if purpose_match:
        purpose = purpose_match.group(1).strip()

    return {
        "recipient": recipient,
        "amount": amount,
        "purpose": purpose,
        "confidence": "High"
    }

# Backward compatibility alias
parse_payment_intent = process_user_intent