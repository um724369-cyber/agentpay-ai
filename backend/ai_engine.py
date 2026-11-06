import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """
You are an AI Commerce & Payment Engine for PayPal.
Analyze user intent and return ONLY raw valid JSON. No markdown, no explanations.

If user wants to buy something:
{
  "action": "CREATE_PAYPAL_ORDER",
  "item": "string",
  "quantity": number,
  "amount": number,
  "currency": "USD"
}

If user wants to split a bill/expense:
{
  "action": "SPLIT_BILL",
  "total_amount": number,
  "currency": "USD",
  "split_between": ["name1", "name2"]
}
"""


def process_user_intent(user_text: str) -> dict:
  payload = {
      "model": "mistral",
      "prompt": f"{SYSTEM_PROMPT}\nUser input: {user_text}\nJSON:",
      "stream": False,
      "format": "json",
  }
  try:
    # Timeout 120 seconds kar diya hai taaki CPU par model load hone ka poora waqt mile
    res = requests.post(OLLAMA_URL, json=payload, timeout=120)
    raw_response = res.json().get("response", "{}")
    data = json.loads(raw_response)

    # Arithmetic calculation for Bill Split
    if data.get("action") == "SPLIT_BILL":
      total = float(data.get("total_amount", 0))
      people = data.get("split_between", [])
      data["amount_per_person"] = (
          round(total / len(people), 2) if len(people) > 0 else total
      )

    return data
  except requests.exceptions.Timeout:
    return {
        "status": "error",
        "message": (
            "Model response timed out (120s). Background mein 'ollama run"
            " mistral' active rakhein."
        ),
    }
  except Exception as e:
    return {"status": "error", "message": str(e)}


if __name__ == "__main__":
  t1 = "Mujhe 1 mechanical keyboard chahiye $60 ka"
  print("Test 1 Result:", process_user_intent(t1))
  