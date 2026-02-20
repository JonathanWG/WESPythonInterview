from rest_framework import viewsets, status
from rest_framework.response import Response
from .services import PaymentService
from Users.models import User

class PaymentViewSet(viewsets.ViewSet):
    
    def create(self, request):
        sender_id = request.data.get('user_id')
        recipient_id = request.data.get('recipient_user_id')
        amount = request.data.get('amount')
        description = request.data.get('description', '')

        if not all([sender_id, recipient_id, amount]):
            return Response(
                {"error": "Fields user_id, recipient_user_id and amount are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            result = PaymentService.execute_payment(
                sender_id=sender_id,
                recipient_id=recipient_id,
                amount=float(amount),
                description=description
            )
            return Response({
                "payment_status": result["status"],
                "new_balanceA": result["sender_balance"],
                "new_balanceB": result["recipient_balance"]
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)