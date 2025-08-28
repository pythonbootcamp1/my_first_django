# photo_gallery/forms.py
from django import forms
from .models import DailyPhoto

class PhotoForm(forms.ModelForm):
    """사진 업로드 폼"""

    class Meta:
        model = DailyPhoto
        fields = ['photo', 'title', 'description', 'photo_date', 'category', 'is_public']
        widgets = {
            'photo_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
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
