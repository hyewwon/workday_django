from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction
from website.utils import validate_username, validate_email, validate_password
from website.models import Department, Company


from api.serializers.auth.auth_serializers import RegisterSerializer, UsernameSerializer, EmailSerializer, LoginSerializer, UserSerializer
from api.serializers.auth.token_serializers import MyTokenObtainPairSerializer, RefreshTokenIDSerializer, MyTokenRefreshSerializer, RefreshTokenSerializer

class RegisterView(GenericAPIView):
    '''
        회원가입 api
    '''
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            membername = serializer.validated_data["membername"]
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            check_password = serializer.validated_data["check_password"]
            email = serializer.validated_data["email"]
            phone_no = serializer.validated_data["phone_no"]
            department_id = serializer.validated_data["department_id"]

            if not validate_username(username):
                return Response(
                    {"message": "유효하지 않은 아이디 입니다."},
                    status=status.HTTP_400_BAD_REQUEST)

            if not validate_password(password):
                return Response(
                    {"message": "비밀번호는 숫자와 영문자 조합으로 8~16자리를 사용해야 합니다."}, 
                    status=status.HTTP_400_BAD_REQUEST)

            if not validate_email(email):
                return Response(
                    {"message": "유효하지 않은 이메일 주소 입니다."}, 
                    status=status.HTTP_400_BAD_REQUEST)

            if password != check_password:
                return Response(
                    {"message": "비밀번호가 다릅니다."}, 
                    status=status.HTTP_400_BAD_REQUEST)

            try:
                User.objects.get(username=username)
                return Response({"message": "아이디가 이미 존재합니다."},
                status=status.HTTP_400_BAD_REQUEST)
            except:
                pass

            try:
                User.objects.get(email=email)
                return Response({"message": "이미 가입한 이메일 입니다."},
                status=status.HTTP_400_BAD_REQUEST)
            except:
                pass
            
            if len(membername) > 20:
                return Response(
                    {"message": "이름은 20자 이하로 사용해주세요."}, 
                    status=status.HTTP_400_BAD_REQUEST) 
            try:
                with transaction.atomic():
                    department = Department.objects.get(id = department_id)
                    user = User.objects.create_user(
                        username,
                        email,
                        password
                    )
                    user.last_name = membername
                    user.profile.department = department
                    user.profile.phone_no = phone_no
                    user.profile.reg_root = "workday"
                    user.save()
                    user.profile.save()

            except Exception as e:
                print(e)
                return Response({"message": "오류 발생."}, status=status.HTTP_400_BAD_REQUEST)
        
            return Response({"message": "가입 신청되었습니다."}, status=status.HTTP_201_CREATED)
            



class CheckUsernameView(GenericAPIView):
    '''
        아이디 중복 검사 api
    '''
    permission_classes = [AllowAny]
    serializer_class = UsernameSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data["username"]
        
        if not validate_username(username):
            return Response({"message": "유효하지 않은 아이디 입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            User.objects.get(username=username)
            return Response({"message":"중복된 아이디 입니다."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"사용 가능한 아이디 입니다.", "username" : username}, status=status.HTTP_200_OK)
        

class CheckEmailView(GenericAPIView):
    '''
        이메일 중복 검사 api
    '''
    permission_classes = [AllowAny]
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]
        
        if not validate_email(email):
            return Response({"message":"유효하지 않은 이메일 주소 입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            User.objects.get(email=email)
            return Response({"message": "중복된 이메일 입니다."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message" : "사용 가능한 이메일 입니다.", "email": email}, status=status.HTTP_200_OK)


class LoginView(GenericAPIView):
    '''
        로그인 api
    '''
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            login_type = serializer.validated_data["login_type"]

            if login_type == "workday":
                user = authenticate(username=username, password=password)
                if user is None:
                    return Response({"message":"아이디 혹은 비밀번호가 틀립니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            if login_type == "google":
                try:
                    user = User.objects.get(username = username)
                except:
                    return Response({"message":"존재하지 않는 회원입니다."}, status=status.HTTP_400_BAD_REQUEST)
                
                if user.has_usable_password():
                    return Response({"message":"workday 계정으로 가입되어있습니다."}, status=status.HTTP_400_BAD_REQUEST)


            if user.profile.check_flag == "0":
                return Response({"message":"신청 내역 확인 중 입니다."}, status=status.HTTP_403_FORBIDDEN)

            # 토근 발급
            token = MyTokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            outstandingToken = OutstandingToken.objects.get(token = refresh_token)
            response = Response(
                {   
                    "user" : UserSerializer(user).data,
                    "message":"로그인 되었습니다.",
                    "jwt_token" :{
                        "access_token" : access_token,
                        "refresh_token_index_id": outstandingToken.id,
                        "refresh_token_exp" : outstandingToken.expires_at.timestamp()
                    }
                },
                status=status.HTTP_200_OK                
            )
            return response


class ReissueTokenView(GenericAPIView):
    '''
        refresh 토근 재발급 api
    '''
    permission_classes = [AllowAny]
    serializer_class = RefreshTokenIDSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception = True):
            refresh_token_index_id = serializer.validated_data["refresh_token_index_id"]
            try:
                refresh = OutstandingToken.objects.get(pk = refresh_token_index_id)
            except:
                return Response(
                    {"message": "refresh token does not exist."}, status=status.HTTP_400_BAD_REQUEST
                )

            serializer = MyTokenRefreshSerializer(data={"refresh": refresh.token})
            serializer.is_valid(raise_exception=True)
            refresh_token = serializer.validated_data["refresh"]
            access_token = serializer.validated_data["access"]
            outstandingToken = OutstandingToken.objects.get(token=refresh_token)
            response = Response(
                {
                    "user" : UserSerializer(refresh.user).data,
                    "message": "refresh token reissue",
                    "jwt token" : {
                        "access_token" : access_token,
                        "refresh_token_index_id" : outstandingToken.id,
                        "refresh_token_exp" : outstandingToken.expires_at.timestamp()
                    }
                },
                status=status.HTTP_200_OK
            )

            return response


class LogoutView(GenericAPIView):
    '''
        로그아웃 API
    '''
    permission_classes = [IsAuthenticated]
    serializer_class = RefreshTokenIDSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception = True):
            refresh_token_index_id = serializer.validated_data["refresh_token_index_id"]
            try:
                refresh = OutstandingToken.objects.get(pk = refresh_token_index_id)
            except:
                return Response({"message":"refresh token does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = RefreshTokenSerializer(data={'refresh':refresh.token})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(status=status.HTTP_204_NO_CONTENT)


class CompanyListView(GenericAPIView):
    '''
        회사 리스트 API 
    '''
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        company = Company.objects.all().values("name", "id")
        return Response({"company": company}, status=status.HTTP_200_OK)
    

class DepartmentListView(GenericAPIView):
    '''
        부서 리스트 API
    '''
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        department = Department.objects.filter(company___id = 1).values("name", "id")
        return Response({"deparment": department}, status=status.HTTP_200_OK)