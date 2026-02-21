import fastapi
from pydantic import BaseModel
from typing import Optional


app = fastapi.FastAPI()

class CreditCard(BaseModel):
    card_number: str
    expiry_date: str

class UserAccount(BaseModel):
    user_id: int
    balance: float
    credit_card: Optional[CreditCard] = None

class PaymentRequest(BaseModel):
    userA: UserAccount
    userB: UserAccount
    payment_value: float


@app.post("/process_payment/")
async def process_payment(request: PaymentRequest):
    
    user_a = request.userA
    user_b = request.userB
    amount = request.payment_value

    if user_a.balance >= amount:
        return {
            "status": "success",
            "method": "balance",
            "new_balanceA": user_a.balance - amount,
            "new_balanceB": user_b.balance + amount,
            "message": "Paid with balance",
            "transaction_id": "BAL-12345"
        }
    
    result = pay_with_credit_card(user_a, user_b, amount)
    
    if result:
        return {
            "status": "success",
            **result
        }

    raise fastapi.HTTPException(
        status_code=400, 
        detail="Insufficient funds and payment failed."
    )
   
def pay_with_credit_card(user_a: UserAccount, user_b: UserAccount, amount: float):
    if not user_a.credit_card:
        return None

    external_resp = processer_external_server_cc_payment(user_a.credit_card, amount)
    
    if external_resp["approved"]:
        return {
            "method": "credit_card",
            "new_balanceA": user_a.balance,
            "new_balanceB": user_b.balance + amount,
            "message": "Paid with credit card",
            "transaction_id": external_resp["transaction_id"]
        }
    return None
        

def processer_external_server_cc_payment(card: CreditCard, amount: float):
    if len(card.card_number) < 13:
        return {"approved": False, "message": "Invalid card number"}    
    return {"approved": True, "transaction_id": "EXT-12345"}