# photo_gallery/forms.py
from django import forms
from .models import DailyPhoto

class PhotoForm(forms.ModelForm):
    """사진 업로드 폼"""

    class Meta:
        model = DailyPhoto
        fields = ['photo', 'title', 'description', 'photo_date', 'category', 'is_public']
        widgets = {
            'photo': forms.FileInput(attrs={
                'class': 'form-control d-none',
                'accept': 'image/*'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '사진 제목을 입력하세요'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '사진에 대한 설명을 입력하세요'
            }),
            'photo_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_photo(self):
        """이미지 파일 검증"""
        photo = self.cleaned_data.get('photo')

        if photo:
            # 파일 크기 체크 (5MB)
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError('파일 크기는 5MB를 초과할 수 없습니다.')

            # 이미지 파일인지 확인
            valid_types = ['image/jpeg', 'image/png', 'image/gif']
            if photo.content_type not in valid_types:
                raise forms.ValidationError('JPEG, PNG, GIF 파일만 업로드 가능합니다.')

        return photo
