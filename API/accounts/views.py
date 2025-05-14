from .imports import *

class AuthenticateCheckAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        return Response(data={'response':'is_Authenticated'}, status=status.HTTP_200_OK)

class LoginAPIView(APIView):

    def post(self, request):
        data = request.data
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user is not None:
            jwt_token = AccessToken.for_user(user)
            return Response(data=dict({
                'jwt_token': str(jwt_token)
            }), status=status.HTTP_200_OK)
        else:
            username = data.get('username')
            if User.objects.filter(
                Q(username__exact=username) |
                Q(phone__exact=username)    |
                Q(email__exact=username)
            ).exists():
                return Response(data={'response': 'incorrect password'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={'response': 'please enter a valid username, phone or email'},
                            status=status.HTTP_400_BAD_REQUEST)

class RegisterAPIView(APIView):

    def post(self, request):
        data = request.data
        if not User.objects.filter(phone__exact=data['phone']).exists():
            _otp_object = Otp.objects.filter(phone=data['phone'])
            if _otp_object.exists():
                _otp_object.delete()
            token, code = get_random_string(length=255), rnd(1221, 9889)
            Otp.objects.create(token=token, code=code, phone=data['phone'])
            return Response(data={
                'token': token,
            }, status=status.HTTP_200_OK)
        else:
            return Response(data={'response': 'this Phone is already exists'},
                            status=status.HTTP_400_BAD_REQUEST)

class CheckOtpTokenAPIView(APIView):

    def post(self, request):
        Otp.otp_clean()
        data = request.data
        if Otp.objects.filter(
            Q(token__exact=data['token']) &
            Q(phone=data['phone'])
        ).exists():
            return Response(data=dict({'is_true':True}), status=status.HTTP_200_OK)
        else:
            return Response(data=dict({'is_true':False}), status=status.HTTP_406_NOT_ACCEPTABLE)

class CreateAccountAPIView(APIView):

    def post(self, request):
        Otp.otp_clean()
        data = request.data
        _otp = Otp.objects.filter(
            Q(code=data['code'])   &
            Q(phone=data['phone']) &
            Q(token=data['token'])
        )
        otp = _otp.first()
        if _otp.exists() and int(otp.phone) == int(data['phone']):
            review_objects = User.objects.filter(
                Q(username=data['username']) |
                Q(email=data['email'])
            )
            if not review_objects.exists():
                if data['password1'] == data['password2']:
                    User.objects.create_user(
                        phone=otp.phone,
                        username=data['username'],
                        email=data['email'],
                        password=data['password1']
                    )
                    _otp.delete()
                    return Response(data={
                        'response': 'created account'
                    }, status=status.HTTP_200_OK)
                else:
                    _response = {'response':'password does not match'}
            else:
                _review_objects = review_objects.first()
                if _review_objects.email == data['email']:
                    _response = {'response': 'this email is already exists'}
                elif _review_objects.username == data['username']:
                    _response = {'response':'this username is already exists'}
            return Response(data=dict(_response), status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            _response = {'response':'invalid code'}
            return Response(data=dict(_response), status=status.HTTP_406_NOT_ACCEPTABLE)


class ChangePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = User.objects.get(phone=request.user)
        if user.check_password(data['current_password']):
            if not data['current_password'] == data['password1']:
                user.set_password(data['password1'])
                user.save()
                return Response(data=dict({
                    'response': 'password successfully updated'
                }), status=status.HTTP_200_OK)
            else:
                _response = {'response': 'new password can not be your current password'}
        else:
            _response = {'response': 'your current password is wrong'}
        return Response(data=_response, status=status.HTTP_406_NOT_ACCEPTABLE)