import json
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
import MySQLdb.cursors
from appmain import mysql
import requests

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('index.html')

@main.route('/cars')
def cars():
    return render_template('generic.html')

@main.route('/login')
def login_page():
    return render_template('login.html')

@main.route('/survey')
def survey_page():
    return render_template('survey.html')

@main.route('/analyze')
def analyze_page():
    return render_template('analyze.html')

@main.route('/get-car-models', methods=['GET'])
def get_car_models():
    # 실제 API 서버로부터 차량 모델 목록을 가져옵니다.
    car_models = ['Carnival', 'K3', 'K5', 'K7/K8', 'K9', 'Mohave', 'Morning', 'Ray', 'Sorento', 'Sportage']
    return jsonify(car_models)

@main.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        try:
            api_url = "http://127.0.0.1:5000/predict"
            files = {'file': (file.filename, file.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            response = requests.post(api_url, files=files)
            response.raise_for_status()
            return jsonify(response.json())
        except requests.RequestException as e:
            return jsonify({'error': 'Network error', 'message': str(e)}), 500
        except json.JSONDecodeError as e:
            return jsonify({'error': 'JSON Decode Error', 'message': str(e)}), 500
    return jsonify({'error': 'No file provided'}), 400

@main.route('/signup')
def signup_page():
    return render_template('signup.html')

@main.route('/get-question/<int:question_id>', methods=['GET'])
def get_question(question_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM questions WHERE id = %s', (question_id,))
    question = cursor.fetchone()
    cursor.execute('SELECT id, choice_text FROM choices WHERE question_id = %s', (question_id,))
    choices = cursor.fetchall()
    return jsonify(question=question['question_text'], choices=[{'id': choice['id'], 'choice_text': choice['choice_text']} for choice in choices])

@main.route('/submit-answer', methods=['POST'])
def submit_answer():
    choice_id = int(request.form['choice_id'])
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT mpgRate, psRate, priceRate, sizeRate, weight_Id FROM choiceRate WHERE id = %s', (choice_id,))
    rates = cursor.fetchone()

    if not rates:
        return jsonify(success=False, message="Invalid choice"), 404

    session['total_mpg'] = session.get('total_mpg', 0) + rates['mpgRate']
    session['total_ps'] = session.get('total_ps', 0) + rates['psRate']
    session['total_price'] = session.get('total_price', 0) + rates['priceRate']
    session['total_size'] = session.get('total_size', 0) + rates['sizeRate']
    session['count'] = session.get('count', 0) + 1

    if rates['weight_Id']:
        session['weight_id'] = rates['weight_Id']

    cursor.execute('SELECT next_question_id FROM choices WHERE id = %s', (choice_id,))
    next_question = cursor.fetchone()
    if next_question and next_question['next_question_id']:
        return jsonify(success=True, next_question_id=next_question['next_question_id'])
    else:
        return jsonify(success=True, end_of_survey=True)

@main.route('/result-page')
def result_page():
    count = session.get('count', 0)
    weight_id = session.get('weight_id')

    if count == 0:
        return redirect(url_for('main.survey'))

    avg_scores = {
        'mpg': round(session['total_mpg'] / count),
        'ps': round(session['total_ps'] / count),
        'price': round(session['total_price'] / count),
        'size': round(session['total_size'] / count)
    }

    session.clear()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    weight = get_weight(cursor, weight_id)
    cars = find_cars(cursor, avg_scores, weight, ignore=weight['first_ignore'])

    if not cars:
        cars = find_cars(cursor, avg_scores, weight, ignore=weight['second_ignore'])
        if not cars:
            cars = find_cars(cursor, avg_scores, weight, ignore=weight['third_ignore'])

    first_car = cars[0] if cars else None
    other_cars = cars[1:4] if len(cars) > 1 else []
    more_cars = cars[4:] if len(cars) > 4 else []

    return render_template('result_page.html', first_car=first_car, other_cars=other_cars, more_cars=more_cars, averages=avg_scores)

def get_weight(cursor, weight_id):
    cursor.execute("SELECT * FROM weight WHERE id = %s", (weight_id,))
    return cursor.fetchone()

def find_cars(cursor, avg_scores, weight, ignore=None):
    fields = ['mpgRate', 'psRate', 'priceRate', 'sizeRate']
    conditions = []
    params = {}

    for field in fields:
        field_name = field[:-4]
        if ignore and field == ignore:
            continue

        if field == 'priceRate':
            min_val = avg_scores[field_name] - 3
            max_val = avg_scores[field_name] + 1
        else:
            min_val = avg_scores[field_name] - 1
            max_val = avg_scores[field_name] + 1

        conditions.append(f"{field} BETWEEN %({field}_min)s AND %({field}_max)s")
        params[f"{field}_min"] = min_val
        params[f"{field}_max"] = max_val

    if not conditions:
        return []

    query = f"SELECT * FROM carRate WHERE {' AND '.join(conditions)}"
    if weight['order_by']:
        query += f" ORDER BY {weight['order_by']} {weight['order_by_type']}"

    cursor.execute(query, params)
    return cursor.fetchall()

@main.route('/calculate-averages', methods=['GET'])
def calculate_averages():
    required_fields = ['total_mpg', 'total_ps', 'total_price', 'total_size', 'count']
    if not all(field in session for field in required_fields):
        return jsonify(success=False, message="Session data incomplete"), 400

    try:
        count = session.get('count', 0)
        if count == 0:
            raise ValueError("Count is zero, cannot calculate averages")

        avg_scores = {
            'avgMpg': round(session.get('total_mpg', 0) / count, 2),
            'avgPs': round(session.get('total_ps', 0) / count, 2),
            'avgPrice': round(session.get('total_price', 0) / count, 2),
            'avgSize': round(session.get('total_size', 0) / count, 2)
        }
        return jsonify(avg_scores)
    except Exception as e:
        return jsonify(success=False, message=str(e)), 400