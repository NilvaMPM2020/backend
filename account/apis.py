# Create your views here.
import random

from kavenegar import KavenegarAPI
from pytz.exceptions import Error
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from MPM2020 import settings
from MPM2020.settings import redis_instance, KAVENEGAR_API
from MPM2020.utils import get_error_obj
from account.models import User
from account.serializers import UserSerializer


class LoginAPI(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    @staticmethod
    def generate_verification_code():
        return random.randint(10 ** 6, 10 ** 7)

    @staticmethod
    def send_sms(phone, code):
        api = KavenegarAPI(KAVENEGAR_API)
        # api.host="79.175.172.10"
        # for OTP account
        params = {'receptor': phone,
                  'token': '%d' % code,
                  'type': 'sms', 'template': 'verifyasoude'}
        api.verify_lookup(params)

    def get(self, request, phone):
        try:
            code = LoginAPI.generate_verification_code()
            redis_instance.setex(phone, 90, code)
            LoginAPI.send_sms(phone, code)
            return Response({'code': code})
        except Error as _:
            return Response(get_error_obj(settings.error_status['store_failure']),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, phone):
        if 'code' not in request.data or 'type' not in request.data:
            return Response(get_error_obj(settings.error_status['auth_fields_defect']),
                            status=status.HTTP_400_BAD_REQUEST)
        stored_code = redis_instance.get(phone)

        if stored_code and int(stored_code) == request.data['code']:
            user = User.objects.filter(phone=phone).first()
            if not user:
                user = User(username=phone, phone=phone, user_type=request.data['type'])
                user.save()
            token, _ = Token.objects.get_or_create(user=user)
            user_serialized = UserSerializer(user)
            return Response({'token': token.key, 'user': user_serialized.data})
        else:
            return Response(get_error_obj(settings.error_status['verification_failure']),
                            status=status.HTTP_400_BAD_REQUEST)
