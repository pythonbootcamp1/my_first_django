# photo_gallery/models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image
import os
from datetime import date

class DailyPhoto(models.Model):
    """하루 한 장 사진 모델"""

    CATEGORY_CHOICES = [
        ('daily', '일상'),
        ('food', '음식'),
        ('travel', '여행'),
        ('people', '사람'),
        ('nature', '자연'),
        ('other', '기타'),
    ]

    # 기본 필드
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    photo = models.ImageField(
        '사진',
        upload_to='photos/%Y/%m/%d/'
    )
    thumbnail = models.ImageField(
        '썸네일',
        upload_to='thumbnails/%Y/%m/%d/',
        blank=True,
        editable=False  # 자동 생성되므로 수정 불가
    )

    # 사진 정보
    title = models.CharField('제목', max_length=100)
    description = models.TextField('설명', max_length=500, blank=True)
    photo_date = models.DateField('촬영일', default=date.today)
    category = models.CharField(
        '카테고리',
        max_length=10,
        choices=CATEGORY_CHOICES,
        default='daily'
    )

    # 공개 설정
    is_public = models.BooleanField('공개', default=True)

    # 좋아요 (1단계: 폼으로 처리)
    likes = models.ManyToManyField(
        User,
        related_name='liked_photos',
        blank=True
    )

    # 메타 정보
    created_at = models.DateTimeField('업로드일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '일일 사진'
        verbose_name_plural = '일일 사진들'
        ordering = ['-photo_date', '-created_at']

    def __str__(self):
        return f'[{self.author.username}] {self.title} ({self.photo_date})'

    def save(self, *args, **kwargs):
        """저장 시 썸네일 자동 생성"""
        super().save(*args, **kwargs)
        if self.photo and not self.thumbnail:
            self.create_thumbnail()

    def create_thumbnail(self):
        """Pillow를 사용한 썸네일 생성"""
        # 원본 이미지 열기
        img = Image.open(self.photo.path)

        # RGB로 변환 (투명 배경 처리)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        # 썸네일 크기 (300x300)
        img.thumbnail((300, 300), Image.Resampling.LANCZOS)

        # 썸네일 저장 경로 생성
        thumb_name = os.path.basename(self.photo.name)
        thumb_name = f'thumb_{thumb_name}'
        thumb_path = os.path.join('thumbnails',
                                  self.photo_date.strftime('%Y/%m/%d'),
                                  thumb_name)

        # 전체 경로
        full_thumb_path = os.path.join(settings.MEDIA_ROOT, thumb_path)

        # 디렉토리 생성
        os.makedirs(os.path.dirname(full_thumb_path), exist_ok=True)

        # 썸네일 저장
        img.save(full_thumb_path, 'JPEG', quality=85)

        # 모델 필드 업데이트
        self.thumbnail = thumb_path
        super().save(update_fields=['thumbnail'])

    def delete(self, *args, **kwargs):
        """삭제 시 파일도 함께 삭제"""
        # 파일 경로 저장
        photo_path = self.photo.path if self.photo else None
        thumb_path = self.thumbnail.path if self.thumbnail else None

        # 모델 삭제
        super().delete(*args, **kwargs)

        # 파일 삭제
        if photo_path and os.path.exists(photo_path):
            os.remove(photo_path)
        if thumb_path and os.path.exists(thumb_path):
            os.remove(thumb_path)