from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

from django.db import transaction
from django.urls import reverse
from django.contrib.auth.models import User

from api.serializers.fee_board.free_board_serializers import FreeBoardSerializer 
from website.models import FreeBoard, FreeBoardType
from website.utils import getTokenUser

class FreeBoardCreateView(GenericAPIView):
    '''
        자유 게시판 등록 api
    '''
    permission_classes = [IsAuthenticated]
    serializer_class = FreeBoardSerializer

    def post(self, request, *args, **kwargs):
        user = getTokenUser(token=str(request.auth))
        if not user:
            return Response(
                {"message": "토큰 정보 오류"}, status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data["title"]
            content = serializer.validated_data["content"]
            board_type = serializer.validated_data["board_type"]
            anonymous_flag = serializer.validated_data["anonymous_flag"]

            try:
                board_type = FreeBoardType.objects.get(id = board_type)
                with transaction.atomic():
                    FreeBoard.objects.create(
                        user = user,
                        title = title,
                        content = content,
                        board_type = board_type,
                        anonymous_flag = anonymous_flag
                    )
            except Exception as e:
                print(e)
                return Response({"message":"작성 실패..."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "작성되었습니다.", "next" : reverse("website:mypage")}, status=status.HTTP_202_ACCEPTED)

