import re


def extract_otp_from_text(raw_text: str) -> dict:
  """SMS ya Clipboard text se OTP detect aur extract karta hai."""
  if not raw_text or not isinstance(raw_text, str):
    return {"status": "FAILED", "otp": None, "message": "Empty or invalid text"}

  # Pattern: 4 se 8 digits ka number jo standalone word ho
  pattern = r"\b\d{4,8}\b"
  matches = re.findall(pattern, raw_text)

  if matches:
    # Most likely OTP standard lengths: 6 digits ya 4 digits
    candidate = matches[0]
    for m in matches:
      if len(m) == 6:
        candidate = m
        break

    return {
        "status": "SUCCESS",
        "otp": candidate,
        "length": len(candidate),
        "source_snippet": raw_text[:40] + "...",
    }

  return {
      "status": "NOT_FOUND",
      "otp": None,
      "message": "No numeric OTP detected in text",
  }


# --- Test Cases ---
if __name__ == "__main__":
  test_sms_1 = "Your PayPal security code is 849201. It expires in 10 minutes. Do not share this code."
  test_sms_2 = "Bank alert: OTP for txn of USD 45.00 is 3921. Valid for 5 mins."
  test_sms_3 = "Hey bro, send me the money on PayPal."

  print("Test 1 Result:", extract_otp_from_text(test_sms_1))
  print("Test 2 Result:", extract_otp_from_text(test_sms_2))
  print("Test 3 Result:", extract_otp_from_text(test_sms_3))