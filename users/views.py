from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserSerializer
from users.services import (convert_rub_to_dollars,
                            create_stripe_course_for_payment,
                            create_stripe_price, create_stripe_session,
                            get_stripe_session_status)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveApiView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyApiView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentsCreateAPIView(CreateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(payment_user=self.request.user)
        amount_to_dollars = convert_rub_to_dollars(payment.amount)
        product_id = create_stripe_course_for_payment(amount_to_dollars)
        price_id = create_stripe_price(amount_to_dollars, product_id)
        session_id, payment_link = create_stripe_session(price_id)

        print(f"session_id: {session_id}")  # ← отладка
        print(f"payment_link: {payment_link}")  # ← отладка

        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class CheckPaymentStatusView(APIView):
    def get(self, request, session_id):
        data = get_stripe_session_status(session_id)
        return Response(data)
