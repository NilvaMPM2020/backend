# Create your views here.
import random

from kavenegar import KavenegarAPI
from pytz.exceptions import Error
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from MPM2020 import settings
from MPM2020.settings import redis_instance, KAVENEGAR_API, ASOUDE_URL, REDIS_HOST, REDIS_PORT
from MPM2020.utils import get_error_obj, init_redis
from account.models import User, Service, Round, ConditionSchema
from account.serializers import UserSerializer, ServiceSerializer


class LoginAPI(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    @staticmethod
    def generate_verification_code():
        return random.randint(10 ** 5, 10 ** 6)

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

        if int(stored_code) == int(request.data['code']):
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


class ProfileAPI(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        if 'pk' not in self.kwargs:
            return self.request.user
        pk = self.kwargs['pk']
        return self.queryset.filter(pk=pk).first()


class ServiceListCreateAPI(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Service.objects.filter(business=self.request.user)

    def create(self, request, *args, **kwargs):
        validated_data = request.data
        got_stock = validated_data.pop('got_stock')
        duration = validated_data.pop('duration')
        conditions = validated_data.pop('conditions')

        instance = Service.objects.create(**validated_data, business=self.request.user)
        deep_link = ASOUDE_URL + '?business=' + str(instance.pk)
        instance.link = deep_link
        instance.save()
        round = Round.objects.create(got_stock=got_stock, duration=duration, name=validated_data['name'],
                                     service=instance)
        for c in conditions:
            ConditionSchema.objects.create(title=c['title'], description=c['title'], related_round=round)
        return Response({'status': 'ok', 'link': deep_link})


class ServiceRetrieveAPI(generics.RetrieveUpdateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

