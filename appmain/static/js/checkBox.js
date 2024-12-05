document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('carSelection');
    const apiServerIp = 'http://10.80.1.217:5000';

    // Fetch historical data when the page loads
    fetch(`${apiServerIp}/historical-data`)
        .then(response => response.json())
        .then(data => {
            populateCarSelection(data);
            updateChart(data); // 모델 학습 데이터를 기반으로 그래프 업데이트
        })
        .catch(error => console.error('Error:', error));

    const fileInput = document.getElementById('fileInput');
    const uploadButton = document.getElementById('uploadButton');

    uploadButton.addEventListener('click', function() {
        const file = fileInput.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            fetch(`${apiServerIp}/upload`, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data && data['error']) {
                    console.error('Error from API:', data['error']);
                } else if (data && data[0] && data[0]['Predicted Sales']) {
                    updatePredictionTable(data); // 예측 테이블 업데이트
                } else {
                    console.error('Invalid data format received:', data);
                }
            })
            .catch(error => console.error('Error:', error));
        } else {
            alert("Please select a file to upload.");
        }
    });

function populateCarSelection(data) {
    const carModels = new Set();
    data.forEach(car => carModels.add(car.Car));

    carModels.forEach(carModel => {
        const label = document.createElement('label');
        label.style.display = 'flex';
        label.style.alignItems = 'center';
        label.style.marginRight = '10px'; // 각 체크박스의 간격을 줌
        label.style.marginBottom = '10px'; // 각 체크박스의 아래쪽 간격을 줌

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = carModel;
        checkbox.checked = true; // 초기 상태는 모든 차량 선택된 상태
        checkbox.style.marginRight = '5px'; // 텍스트와 체크박스 사이의 간격을 줌

        checkbox.addEventListener('change', function() {
            updateVisibility(this.value, this.checked);
        });

        label.appendChild(checkbox);
        label.appendChild(document.createTextNode(carModel));
        document.getElementById('carSelection').appendChild(label);
    });
}



    function updateVisibility(carModel, visible) {
        if (window.myChart) {
            window.myChart.data.datasets.forEach(dataset => {
                if (dataset.label.startsWith(carModel)) {
                    dataset.hidden = !visible;
                }
            });
            window.myChart.update();
        }
    }

    function updateChart(data) {
        const ctx = document.getElementById('salesChart').getContext('2d');

        if (window.myChart) {
            window.myChart.destroy();
        }

        if (data.length === 0) return;

        const datasets = data.flatMap(car => {
            const actualSalesData = car['Actual Sales'].map((sale, index) => ({ x: new Date(car['Year-Month'][index]), y: sale }));
            const predictedSalesData = car['Predicted Sales'].map((sale, index) => ({ x: new Date(car['Year-Month'][index]), y: sale }));

            return [
                {
                    label: car.Car + ' Actual',
                    data: actualSalesData,
                    borderColor: getRandomColor(),
                    fill: false,
                    hidden: false
                },
                {
                    label: car.Car + ' Prediction',
                    data: predictedSalesData,
                    borderColor: getRandomColor(),
                    borderDash: [5, 5],
                    fill: false,
                    hidden: false
                }
            ];
        });

        window.myChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: datasets
            },
            options: {
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'month',
                            tooltipFormat: 'yyyy-MM'
                        },
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Sales'
                        }
                    }
                }
            }
        });
    }

    function updatePredictionTable(data) {
        const tableBody = document.getElementById('predictionTable').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = ''; // 기존 행을 모두 제거

        data.forEach(item => {
            const row = tableBody.insertRow();
            row.insertCell(0).textContent = item['Year-Month'];
            row.insertCell(1).textContent = item['Car'];
            row.insertCell(2).textContent = item['Predicted Sales'].toFixed(0);
        });
    }

    function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }
});
