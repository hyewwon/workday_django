from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# 소속 부서
class Department(models.Model):
    name = models.CharField(db_column="name", null=False, max_length=255)
    class Meta:
        db_table = "department"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name="profile", null=True)
    phone_no = models.CharField(db_column="phone_no", null=True, max_length=15, default="")
    image = models.ImageField(db_column="image", upload_to="profile_images")
    note = models.TextField(db_column="note",null=True)
    check_flag = models.CharField(db_column="check_flag", max_length=10, default="0")

    class Meta:
        db_table = "profile"

# 휴가 
class Vacation(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="vacation")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vacation")
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        db_table = "vacation"


# 출결
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendance")
    attend_time = models.CharField(db_column="attend_time", default=datetime.now().time(),max_length=250)
    leave_time = models.CharField(db_column="leave_time", null=True, default="", max_length=250)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        db_table="attendance"

class FreeBoardType(models.Model):
    type_name = models.CharField(db_column="type_name", null=False, max_length=255)

    class Meta:
        db_table = "freeboard_type"

# 자유 게시판
class FreeBoard(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="freeboard", default=None)
    board_type = models.ForeignKey(FreeBoardType, on_delete=models.CASCADE, related_name="freeboard_type", default=8)
    title = models.CharField(db_column="title", null=False, max_length=255)
    content = models.TextField(db_column="content", null=False)
    anonymous_flag = models.CharField(db_column="anonymous_flag", max_length=10, default="0")
    created_at = models.DateTimeField(db_column="created_at", auto_now_add=True)
    updated_at = models.DateTimeField(db_column="updated_at", auto_now=True)

    class Meta:
        db_table = "freeboard"


# 자유 게시판 댓글
class BoradReply(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    freeboard = models.ForeignKey(FreeBoard,on_delete=models.CASCADE)
    reply = models.TextField(db_column="reply",default="",null=True)
    hidden = models.CharField(db_column="hidden", default="0", max_length=10)
    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updated_at', auto_now=True)

    class Meta:
        db_table = "board_reply"


class Notice(models.Model):
    title = models.CharField(db_column="title", null=False, max_length=255)
    content = models.TextField(db_column="content", null=False)
    top_flag = models.CharField(db_column="top_flag", max_length=10, default="0")
    created_at = models.DateTimeField(db_column="created_at", auto_now_add=True)
    updated_at = models.DateTimeField(db_column="updated_at", null=False, auto_now=True)

    class Meta:
        db_table = "notice"