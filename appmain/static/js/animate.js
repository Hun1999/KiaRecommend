// 애니메이션을 적용할 텍스트와 속도, 지연시간 설정
var typingText = '당신에게 맞는 최적의 차량을 찾아보세요.';
var typingSpeed = 50; // 밀리초 단위
var typingDelay = 500; //

// 타이핑 효과 함수
function typeEffect(element, text, speed) {
  var textArray = text.split('');
  var currentIndex = 0;
  element.innerHTML = '';

  var typeWriter = setInterval(function() {
    if (currentIndex < textArray.length) {
      element.innerHTML += textArray[currentIndex++];
    } else {
      clearInterval(typeWriter);
    }
  }, speed);
}

// DOM이 로드된 후 애니메이션 실행
document.addEventListener('DOMContentLoaded', function() {
  var typingElement = document.querySelector('.typing');
  if (typingElement) {
    // 타이핑 효과 전에 지연을 추가
    setTimeout(function() {
      typeEffect(typingElement, typingText, typingSpeed);
    }, typingDelay);
  }
});
