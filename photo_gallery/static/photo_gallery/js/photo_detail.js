
// 1. CSRF 토큰 가져오기 (Django 보안)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// 2. Axios 기본 설정
axios.defaults.headers.common['X-CSRFToken'] = getCookie('csrftoken');

// 3. HTML 요소 가져오기
const likeBtn = document.getElementById('likeBtn');
const likeCount = document.getElementById('likeCount');
const messageDiv = document.getElementById('message');

// 4. 현재 상태 확인
let isLiked = likeBtn.dataset.liked === 'true';
const photoId = likeBtn.dataset.photoId;

// 5. 좋아요 버튼 클릭 이벤트
likeBtn.addEventListener('click', function() {
    // 중복 클릭 방지
    likeBtn.disabled = true;
    likeBtn.textContent = '처리중...';

    // Axios로 서버에 요청
    axios.post(`/photo/${photoId}/like_ajax/`)
        .then(response => {
            // 성공! 서버에서 받은 데이터
            const data = response.data;

            // 상태 업데이트
            isLiked = data.liked;

            // 버튼 텍스트 변경
            if (isLiked) {
                likeBtn.textContent = '❤️ 좋아요 취소';
            } else {
                likeBtn.textContent = '🤍 좋아요';
            }

            // 좋아요 수 업데이트
            likeCount.textContent = data.like_count;

            // 메시지 표시 (3초 후 사라짐)
            messageDiv.textContent = data.message;
            setTimeout(() => {
                messageDiv.textContent = '';
            }, 3000);
        })
        .catch(error => {
            // 에러 처리
            console.error('Error:', error);
            messageDiv.textContent = '오류가 발생했습니다.';

            // 버튼 원상복구
            if (isLiked) {
                likeBtn.textContent = '❤️ 좋아요 취소';
            } else {
                likeBtn.textContent = '🤍 좋아요';
            }
        })
        .finally(() => {
            // 성공/실패 관계없이 버튼 다시 활성화
            likeBtn.disabled = false;
        });
});
