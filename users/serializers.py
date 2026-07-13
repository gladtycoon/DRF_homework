from rest_framework.serializers import ModelSerializer

from users.models import Payments, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"
