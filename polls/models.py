from tabnanny import verbose
from turtle import title
from django.db import models

# Create your models here.
"""
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    investment_style VARCHAR(20) DEFAULT '보수적'
        CHECK (investment_style IN ('보수적', '적극적', '공격적')),
    vip_flag BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
class Article(models.Model):
    title = models.CharField('이게요렇게나옵니다',max_length=200)
    content = models.TextField("content")
    created_at = models.DateTimeField('작성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    def __str__(self):
        return "__str__통해서이렇게나옵니다"+ self.title

    class Meta:
        verbose_name = "아티클"
        verbose_name_plural = "아티클들"

# models.py에 Table을 파이썬 코드로 작성합니다!
# 설계도 작성 : python manage.py makemigrations
# 실제 DB에 반영 : python manage.py migrate

# 여러분의 DB에 테이블을 생성해 보겠습니다!
from django.contrib.auth.models import User

# author 추가
# 디버그에서 view에 index에서 브레이크 포인트로 멈추기
# 디버그 콘솔에서 Memo 내용을 조회
# from django.contrib.auth.models import User
# user = User.objects.get(pk=1)
# user.memos.all()
class Memo(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='memos',
        verbose_name='작성자'
    )
    title = models.CharField('제목', max_length=100)
    content = models.TextField('내용')
    is_important = models.BooleanField('중요', default=False)
    created_at = models.DateTimeField('생성일', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '메모'
        verbose_name_plural = '메모 목록'
        ordering = ['-created_at']  # 최신순 정렬

# -> Admin 페이지 등록
# 2시 50분까지


# 3시 부터는 뷰를 같이 만들어 보기기