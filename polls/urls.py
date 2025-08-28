from django.urls import path
# from . import views
# 원하는 뷰를 가져오는 형태
from .views import lion, dubug_request, memo_list, memo_detail, index,memo_create,test1,test2
# from polls import views
# from polls.views import lion, dubug_request
from . import views
# app_name 부여하고, urlpattern에 이름 넣고
# html에서 a태그(링크)부분에
# {% url '앱네임:url이름' %} 넣어서
# 잘 동작하는지 확인해보겠습니다!
app_name = 'polls'

urlpatterns = [   
    path('',index, name='index'),
    path('memo/', memo_list, name='memo_list'),
    path('memo/mine/',views.my_memo_list,name="my_memo_list"),
    path('memo/<int:pk>/', memo_detail, name='memo_detail'),
    path('memo/create/',memo_create, name='memo_create'),
    path('test1/', test1, name='test1'),
    path('test2/',test2,name='test2'),
    path('memo/update/<int:pk>/', views.memo_update, name='memo_update'),
    path('memo/delete/<int:pk>/', views.memo_delete, name='memo_delete')
    # path('tiger/<str:name>/', lion),
    # path('', index),
    # path('bad/', blog_list),
    # 127.0.0.1/dubug/  => path('dubug/', dubug_request)
]
# url이 어떻게 뷰로 연결되는지 원리를 이해.
