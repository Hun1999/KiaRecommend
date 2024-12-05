function getRecommendations() {
    const userId = document.getElementById('userId').value;
    if (!userId) {
        alert('사용자 ID를 입력하세요.');
        return;
    }

    fetch(`http://localhost:5000/get_recommendations?userId=${userId}`)
        .then(response => response.json())
        .then(data => {
            const recommendationsDiv = document.getElementById('recommendations');
            recommendationsDiv.innerHTML = '';  // 기존 추천 목록 초기화

            if (data.length === 0) {
                recommendationsDiv.innerHTML = '추천할 차량이 없습니다.';
                return;
            }

            data.forEach(car => {
                const carDiv = document.createElement('div');
                carDiv.classList.add('car');
                carDiv.innerHTML = `
                    <h3>${car.trimName}</h3>
                    <p>차량 ID: ${car.carId}</p>
                `;
                recommendationsDiv.appendChild(carDiv);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('추천 정보를 불러오는 데 실패했습니다.');
        });
}
