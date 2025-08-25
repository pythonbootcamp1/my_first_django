from django.urls import path
# from . import views
# 원하는 뷰를 가져오는 형태
from .views import lion, dubug_request, memo_list, one_memo, index, search
# from polls import views
# from polls.views import lion, dubug_request

urlpatterns = [   
    path('tiger/<str:name>/', lion),
    path('', index),
    # path('bad/', blog_list),
    path('memo/', memo_list),
    path('memo/<int:memo_id>/', one_memo),
    path('search/', search)
    # 127.0.0.1/dubug/  => path('dubug/', dubug_request)
]
# url이 어떻게 뷰로 연결되는지 원리를 이해.
