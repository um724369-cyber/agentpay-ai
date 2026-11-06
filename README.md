# AgentPay AI ⚡
> Autonomous Natural Language Payments & 2FA Verification Agent

AgentPay AI is an autonomous payment workflow that translates unstructured natural language prompts into verified payment orders. It integrates local Large Language Models (Mistral via Ollama) with PayPal REST order creation, automated SMS OTP extraction, and instantaneous settlement.

---

## 🌟 Key Features
- **Local AI Intent Parsing:** Extracts transaction amounts, recipient identities, and operational purpose locally using Ollama/Mistral with strict JSON schemas.
- **PayPal Sandbox Engine:** Full lifecycle support for standard PayPal REST v2 endpoints (`create-order`, `capture-order`).
- **Autonomous OTP Extraction:** Standalone regex engine designed to parse 6-digit 2FA verification tokens directly from raw SMS payloads.
- **Unified Web Interface:** Tailwind CSS dashboard showing end-to-end telemetry from natural language input to final settlement receipt.

---

## 🏗️ System Architecture

```text
[User Natural Prompt] 
          │
          ▼
   [FastAPI Gateway]
          │
   ┌──────┴─────────────────────────────┐
   ▼                                    ▼
[Local LLM / Ollama]          [PayPal REST Engine]
(Extracts Amount/Recipient)   (Creates PAYID Order)
   │                                    │
   └───────────────┬────────────────────┘
                   ▼
         [OTP Regex Engine]
         (Parses 2FA Token)
                   │
                   ▼
         [Settlement Engine]
      (Status: COMPLETED / 200 OK)