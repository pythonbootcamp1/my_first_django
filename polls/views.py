# polls/views.py에 간단한 뷰 작성
from django.http import HttpResponse

# 장고 페이지 구성의 핵심
from django.shortcuts import render
from .models import Article, Memo

def search(request):
    query = request.GET['q']
    return HttpResponse(f"{query}가 검색되었습니다!!")


# index에서 context 만들어서 보내기기
def index(request):
    memos = Memo.objects.all()
    context = {
        "name":"lion",
        "title":"장고 학습",
        "memos":memos
    }
    return render(request=request,template_name="polls/index.html",context=context)
    
# def blog_list(request):
#     return render(request,"not_good.html")

def lion(request,name):
    return HttpResponse(f"""{name}가 장고를 배웁니다!!""")

# 내가 request라는 객체가 생소한데, 안에 어떤 내용들이 있는지 확인해 보고 싶어
# 이거를 하나의 뷰로 만들어서 웹에 표시해 볼까?
# 디버그 하는 역할 이네 -> dubug_request로 이름짓자
def dubug_request(request):
    # request 의 메서드와
    # request 의 path
    # request 의 META.REMOTE_ADDR를 화면에 표시하자!!
    content = f"""이것이 request가 가지고 있는 정보의 예시입니다.<br>
    request.path = {request.path}    <br>
    request.method = {request.method}    <br>
    request.META.REMOTE_ADDR = {request.META.get('REMOTE_ADDR', 'Unknown')}    <br>
    """
    return HttpResponse(content)

# 디버그 버튼누르시고, launch.json파일 만들기 선택(우리가 디버그 설정을 직접 관리하는 방법)
# 엉뚱한 디버그들 선택해 보기(실수를 해도 스트레스 받지 않기?!)
# 생성된 launch.json을 삭제하고 다시 장고 디버그 설정으로 수정하기
# 디버그 가동(F5 또는 디버그 버튼 클릭)
# 디버그 뷰에서 브레이크 포인트 잡기(코드 왼쪽 숫자의 왼쪽을 클릭, 또는 f9)
# 해당 포인트에 멈추게 해보기!!(서버를 가동하고 해당 뷰가 호출되도록 브라우저에서 주소 입력)
# 디버그 콘솔에서 이것저것 해보기기
# 9시 50분까지 하겠습니다!!!




# 여러개 여러분 마음대로 만들어 보세요!

# view 만들기
# polls에 urls.py 작성
# path("경로",뷰함수)

# config urls.py
# path("아무거나경로", inclued(polls.urls))

# 브라우저에서 확인


# 3시 20분까지
# 각 url로 접근하여 페이지가 나오도록 해보겠습니다.
# 1. /polls/hello/ -> "안녕하세요" 라고 페이지에 표시하기
# 2. /polls/good/ -> AI를 통해 작성된 다양한 페이지 표시하기

# 2시 40분까지 ORM 체험해 보겠습니다~!

# 메모리스트를 보여주는 뷰를 만들어 보겠습니다.
def memo_list(self):
    # 메모 전체 가져오기
    all_memo=Memo.objects.all()
    # content 구성하기
    content=""
    for memo in all_memo:
        content += "제목 : "+memo.title+"<br>"
        content += "내용 : "+memo.content+"<br>"
        content += "----"*10
        content += "<br>"
    return HttpResponse(content)

# content = "제목 : 타이틀
# 내용 : 콘텐트
# 제목 : 타이틀
# 내용 : 콘텐트
# 제목 : 타이틀
# 내용 : 콘텐트
# " 줄바꿈 -> <br>

def one_memo(request, memo_id):
    memo = Memo.objects.get(id=memo_id)
    content = f"""<h1>제목 : {memo.title}</h1> <br><br> 
    내용 : {memo.content}<br>
    {memo.is_important}<br>
    {memo.created_at}
    """
    return HttpResponse(content)