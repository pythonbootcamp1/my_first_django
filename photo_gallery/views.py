# photo_gallery/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q, Count
from .models import DailyPhoto
from .forms import PhotoForm

def photo_list(request):
    """사진 갤러리 목록"""
    # 필터링
    photos = DailyPhoto.objects.all()

    # 공개 사진 + 내 사진만 보기
    if request.user.is_authenticated:
        photos = photos.filter(
            Q(is_public=True) | Q(author=request.user)
        )
    else:
        photos = photos.filter(is_public=True)

    # 카테고리 필터
    category = request.GET.get('category')
    if category:
        photos = photos.filter(category=category)

    # 좋아요 수 추가
    photos = photos.annotate(like_count=Count('likes'))

    # 페이지네이션
    paginator = Paginator(photos, 12)  # 12개씩 표시
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': DailyPhoto.CATEGORY_CHOICES,
        'current_category': category,
    }
    return render(request, 'photo_gallery/photo_list.html', context)


def photo_detail(request, pk):
    """사진 상세보기"""
    photo = get_object_or_404(DailyPhoto, pk=pk)

    # 비공개 사진 접근 권한 체크
    if not photo.is_public and photo.author != request.user:
        messages.error(request, '비공개 사진입니다.')
        return redirect('photo_gallery:photo_list')

    # 이전/다음 사진
    prev_photo = DailyPhoto.objects.filter(
            Q(is_public=True) | Q(author=request.user),
            pk__lt=photo.pk
        ).order_by('-pk').first()

    next_photo = DailyPhoto.objects.filter(
        Q(is_public=True) | Q(author=request.user),
        pk__gt=photo.pk
    ).order_by('pk').first()

    # 현재 사용자가 좋아요 했는지 확인
    user_liked = False
    if request.user.is_authenticated:
        user_liked = photo.likes.filter(pk=request.user.pk).exists()

    context = {
        'photo': photo,
        'prev_photo': prev_photo,
        'next_photo': next_photo,
        'user_liked': user_liked,
        'like_count': photo.likes.count(),
    }
    return render(request, 'photo_gallery/photo_detail.html', context)


@login_required
def photo_create(request):
    """사진 업로드"""
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.author = request.user
            photo.save()
            messages.success(request, '사진이 업로드되었습니다.')
            return redirect('photo_gallery:photo_detail', pk=photo.pk)
    else:
        form = PhotoForm()

    return render(request, 'photo_gallery/photo_form.html', {
        'form': form,
        'title': '사진 업로드'
    })


@login_required
def photo_update(request, pk):
    """사진 수정"""
    photo = get_object_or_404(DailyPhoto, pk=pk)

    # 작성자 확인
    if photo.author != request.user:
        messages.error(request, '자신의 사진만 수정할 수 있습니다.')
        return redirect('photo_gallery:photo_detail', pk=pk)

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request, '사진이 수정되었습니다.')
            return redirect('photo_gallery:photo_detail', pk=pk)
    else:
        form = PhotoForm(instance=photo)

    return render(request, 'photo_gallery/photo_form.html', {
        'form': form,
        'title': '사진 수정',
        'photo': photo
    })


@login_required
def photo_delete(request, pk):
    """사진 삭제"""
    photo = get_object_or_404(DailyPhoto, pk=pk)

    # 작성자 확인
    if photo.author != request.user:
        messages.error(request, '자신의 사진만 삭제할 수 있습니다.')
        return redirect('photo_gallery:photo_detail', pk=pk)

    if request.method == 'POST':
        photo.delete()
        messages.success(request, '사진이 삭제되었습니다.')
        return redirect('photo_gallery:photo_list')

    return render(request, 'photo_gallery/photo_confirm_delete.html', {'photo': photo})


@login_required
def photo_like(request, pk):
    """좋아요 처리 (1단계: 폼 방식)"""
    photo = get_object_or_404(DailyPhoto, pk=pk)

    if request.method == 'POST':
        if request.user in photo.likes.all():
            # 이미 좋아요 했으면 취소
            photo.likes.remove(request.user)
            messages.info(request, '좋아요를 취소했습니다.')
        else:
            # 좋아요 추가
            photo.likes.add(request.user)
            messages.success(request, '좋아요를 눌렀습니다.')

    # 원래 페이지로 돌아가기
    return redirect('photo_gallery:photo_detail', pk=pk)


@login_required
def my_photos(request):
    """내 사진 보기"""
    photos = DailyPhoto.objects.filter(author=request.user)
    photos = photos.annotate(like_count=Count('likes'))

    # 페이지네이션
    paginator = Paginator(photos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'title': '내 사진',
    }
    return render(request, 'photo_gallery/photo_list.html', context)
