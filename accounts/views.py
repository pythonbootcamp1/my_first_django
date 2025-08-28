from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
# Create your views here.

# 2시 40분까지 실습하겠습니다!
# 로그인 전후의 request.user 내용을 확인해 보겠습니다!
def login_view(request): # request.user
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # 인증
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"로그인 성공")
            return redirect('polls:index')
        else:
            messages.error(request,"아이디나 패스워드가 올바르지 않습니다.")
            return redirect('accounts:login')
    else:
        return render(request, 'accounts/login.html')

def logout_view(request):
    username = request.user.username
    logout(request)
    messages.success(request, f"{username}이 로그아웃했습니다.")
    return redirect('polls:index')



def signup_view(request):
    """회원가입 처리 함수형 뷰"""
    if request.user.is_authenticated:
        return redirect('polls:index')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # 유효성 검사
        errors = []

        if not username or not password1:
            errors.append('아이디와 비밀번호는 필수입니다.')

        if password1 != password2:
            errors.append('비밀번호가 일치하지 않습니다.')

        if len(password1) < 8:
            errors.append('비밀번호는 8자 이상이어야 합니다.')

        if User.objects.filter(username=username).exists():
            errors.append('이미 사용중인 아이디입니다.')

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            try:
                # 사용자 생성
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1
                )

                # 자동 로그인
                login(request, user)
                messages.success(request, f'{user.username}님 가입을 환영합니다!')
                return redirect('polls:index')

            except IntegrityError:
                messages.error(request, '회원가입 중 오류가 발생했습니다.')

    return render(request, 'accounts/signup.html')