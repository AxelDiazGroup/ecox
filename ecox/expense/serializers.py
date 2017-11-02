from rest_framework import serializers
from .models import Debt
from core.serializers import PersonSerializer


class DebtSerializer(serializers.HyperlinkedModelSerializer):
    to = PersonSerializer()

    class Meta:
        model = Debt
        fields = '__all__'


class ExpenseSerializer(serializers.Serializer):
    debts = serializers.DecimalField(max_digits=10, decimal_places=2)
