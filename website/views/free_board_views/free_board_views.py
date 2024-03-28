from django.views.generic import View
from django.http import HttpRequest
from django.shortcuts import render,  redirect
from django.utils.decorators import method_decorator
from django.db.models import Q, Case, When, Value, F, Prefetch, Subquery, OuterRef
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from website.forms import FreeBoardForm
from website.utils import getTokenUser
from website.decorators import login_required
from website.models import FreeBoardType, FreeBoard

class FreeBoradView(View):
    @method_decorator(login_required(redirect_url="website:login"))
    def get(self, request,*args, **kwargs):
        context = {}
        access_token = request.COOKIES.get("access_token", None)
        user = getTokenUser(token = access_token)

        paginate_by = '20'
        page = request.GET.get('page', '1')
        search_type = self.request.GET.get('search_type', '')
        search_keyword = self.request.GET.get('search_keyword', '')
        filter_dict = {}

        if search_keyword:
            context['search_type'] = search_type
            context['search_keyword'] = search_keyword
            filter_dict[search_type + '__icontains'] = search_keyword

        free_board = FreeBoard.objects.filter(**filter_dict).values("id", "title", "user__username","anonymous_flag", "created_at", "board_type__type_name").order_by("-created_at")
        board_type = FreeBoardType.objects.all().values("id", "type_name")

        paginator = Paginator(free_board, paginate_by)

        try:
            page_obj = paginator.page(page)
        except (PageNotAnInteger, EmptyPage, InvalidPage):
            page = 1
            page_obj = paginator.page(page)

        pagelist = paginator.get_elided_page_range(page, on_each_side=3, on_ends=1)
        context['pagelist'] = pagelist
        context['group_list'] = page_obj
        context['page_obj'] = page_obj
        context["user"] = user
        context["board_type"] =board_type

        return render(request, "free_board/free_board.html", context)


class FreeBoardCreateView(View):
    @method_decorator(login_required(redirect_url="website:login"))
    def get(self, request, *args, **kwargs):
        context = {}
        access_token = request.COOKIES.get("access_token", None)
        user = getTokenUser(token = access_token)
        board_type = FreeBoardType.objects.all()
        context["user"] = user
        context["form"] = FreeBoardForm
        return render(request, "free_board/free_board_create.html", context)


class FreeBoardDetailView(View):
    @method_decorator(login_required(redirect_url="website:login"))
    def get(self, request, *args, **kwargs):
        context = {}
        access_token =  request.COOKIES.get("access_token", None)
        user = getTokenUser(token = access_token)
        context["user"] = user
        pk = kwargs.get("pk")
        try:
            board = FreeBoard.objects.get(pk = pk)
            context["board"] = board

        except:
            return redirect("/")

        return render(request, "free_board/free_board_detail.html", context)