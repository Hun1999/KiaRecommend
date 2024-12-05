$(document).ready(function() {
    loadQuestion(1);  // 첫 번째 질문 ID로 시작
});

function loadQuestion(questionId) {
    $.getJSON('/get-question/' + questionId, function(data) {
        $('#question').text(data.question);
        $('#answers').empty();
        data.choices.forEach(function(choice) {
            var listItem = $('<li>' + choice.choice_text + '</li>');
            listItem.on('click', function() {
                submitAnswer(choice.id);
            });
            $('#answers').append(listItem);
        });
    });
}

function submitAnswer(choiceId) {
    $.post('/submit-answer', { choice_id: choiceId }, function(data) {
        if (data.success && data.next_question_id) {
            loadQuestion(data.next_question_id);
        } else if (data.success && !data.next_question_id) {
            showResults();
        }
    });
}

function showResults() {
    $.getJSON('/calculate-averages', function(data) {
        var resultHtml = '연비 평균 점수: ' + data.avgMpg.toFixed(2) + '<br>' +
                         '출력 평균 점수: ' + data.avgPs.toFixed(2) + '<br>' +
                         '가격 평균 점수: ' + data.avgPrice.toFixed(2) + '<br>' +
                         '크기 평균 점수: ' + data.avgSize.toFixed(2);
        $('#resultText').html(resultHtml);
        window.location.href = '/result-page';
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.log("AJAX call failed: " + textStatus + ", " + errorThrown);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const loadMoreButton = document.getElementById('load-more');
    if (loadMoreButton) {
        loadMoreButton.addEventListener('click', function() {
            const moreCarsContainer = document.getElementById('more-cars-container');
            if (moreCarsContainer.style.display === 'none') {
                moreCarsContainer.style.display = 'block';
            } else {
                moreCarsContainer.style.display = 'none';
            }
        });
    }
});
