import fastapi
from pydantic import BaseModel


app = fastapi.FastAPI()


@app.post("/process_payment/")
async def process_payment(payment_data: dict):

    try:
    
        userA = payment_data.get("userA")
        userA_balance = userA.get("balance", 0)

        userB = payment_data.get("userB")

        payment_value = payment_data.get("payment_value", 0)

        if userA_balance >= payment_value:
            new_balanceA = userA.get("balance", 0) - payment_value
            new_balanceB = userB.get("balance", 0) + payment_value

            return {"message": "Payment processed successfully", "new_balanceA": new_balanceA, "new_balanceB": new_balanceB}        


        else:

            userA.get("credit_card", "No credit card on file")
            if pay_with_credit_card(userA.get("credit_card", None), payment_value):
                return {"message": "Payment processed successfully using credit card"}
            
    except (ValueError, KeyError) as e:
        return {"message": "An error occurred while processing the payment", "error": str(e)}
   
def pay_with_credit_card(credit_card_info, amount):
    if credit_card_info is None:
        return False
    else:
        if processer_external_server_cc_payment(credit_card_info, amount):
            return True
        

def processer_external_server_cc_payment(credit_card_info, amount):
    print(f"Processing payment of {amount} using credit card {credit_card_info['card_number']} with expiry date {credit_card_info['expiry_date']}")
    return True    

    

    




    return {"message": "Payment processed successfully", "payment_data": payment_data}