from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from ai_engine import process_user_intent
from otp_engine import extract_otp_from_text
from paypal_client import PayPalClient

app = FastAPI(title="AgentPay AI Backend", version="1.0.0")

# Frontend connection allow karne ke liye CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

paypal = PayPalClient()

class IntentRequest(BaseModel):
    prompt: str

class OTPRequest(BaseModel):
    message: str

class OrderRequest(BaseModel):
    amount: float
    currency: Optional[str] = "USD"

class CaptureRequest(BaseModel):
    order_id: str

@app.get("/")
def home():
    return {"status": "running", "service": "AgentPay AI API"}

@app.post("/api/ai/intent")
def get_intent(payload: IntentRequest):
    result = process_user_intent(payload.prompt)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@app.post("/api/ai/extract-otp")
def get_otp(payload: OTPRequest):
    result = extract_otp_from_text(payload.message)
    return result

@app.post("/api/paypal/create-order")
def create_payment(payload: OrderRequest):
    order = paypal.create_order(amount=payload.amount, currency=payload.currency)
    return order

@app.post("/api/paypal/capture-order")
def capture_payment(payload: CaptureRequest):
    capture = paypal.capture_order(order_id=payload.order_id)
    return capture