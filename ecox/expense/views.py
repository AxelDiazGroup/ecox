from .models import Debt
from .serializers import DebtSerializer

from rest_framework import viewsets


class DebtViewSet(viewsets.ModelViewSet):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
