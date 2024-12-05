import mysql.connector
import random
from faker import Faker

# MySQL 연결
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="KIADB"
)
cursor = conn.cursor()

# 가상 데이터 생성 도구
faker = Faker()

# 차량 정보 (전체 목록)
cars = [
    ("carnival 1.6TH", "H", 14, 180, 39250000, 4, ['SUV', 'Large', 'Family', 'CargoSpace', 'Hybrid']),
    ("carnival 2.2", "D", 13.1, 194, 36650000, 4, ['SUV', 'Large', 'Family', 'CargoSpace']),
    ("carnival 3.5", "G", 9, 294, 34700000, 4, ['SUV', 'Large', 'Family', 'CargoSpace']),
    ("carnival-hi-limousine 1.6TH", "H", 12.4, 180, 69450000, 5, ['SUV', 'Large', 'Family', 'CargoSpace', 'Hybrid', 'Luxury']),
    ("carnival-hi-limousine 2.2", "D", 11.7, 194, 66850000, 5, ['SUV', 'Large', 'Family', 'CargoSpace', 'Luxury']),
    ("carnival-hi-limousine 3.5", "G", 8.5, 294, 64900000, 5, ['SUV', 'Large', 'Family', 'CargoSpace', 'Luxury']),
    ("ev6", "E", 5.6, 125, 51300000, 5, ['SUV', 'Large', 'Family', 'Electric']),
    ("ev6-gt", "E", 3.9, 430, 76050000, 5, ['SUV', 'Large', 'Sporty', 'Electric', 'Powerful']),
    ("ev9", "E", 4.2, 150, 77280000, 5, ['SUV', 'Large', 'Family', 'Electric', 'Luxury']),
    ("k3 1.6", "G", 15.2, 123, 18250000, 2, ['Sedan', 'Small', 'FuelEfficient']),
    ("k3-GT 1.6T", "G", 12.1, 204, 27840000, 3, ['Sedan', 'Small', 'Powerful', 'Sporty']),
    ("k5 1.6T", "G", 13.7, 180, 28680000, 3, ['Sedan', 'Family']),
    ("k5 2.0", "G", 12.6, 160, 27840000, 3, ['Sedan', 'Family']),
    ("k5 2.0H", "H", 19.8, 152, 33260000, 3, ['Sedan', 'Hybrid', 'Family', 'FuelEfficient']),
    ("k8 1.6TH", "H", 18, 180, 39250000, 4, ['Sedan', 'Hybrid', 'Family', 'FuelEfficient']),
    ("k8 2.5", "G", 12, 198, 33580000, 4, ['Sedan', 'Small', 'Family', 'CargoSpace']),
    ("k8 3.5", "G", 10.6, 300, 36990000, 4, ['Sedan', 'Small', 'Family', 'CargoSpace']),
    ("k9 3.3T", "G", 8.7, 370, 65880000, 5, ['Sedan', 'Large', 'Family', 'Luxury']),
    ("k9 3.8", "G", 9, 315, 59330000, 5, ['Sedan', 'Large', 'Family', 'Luxury']),
    ("mohave 3.0", "D", 9.1, 257, 50540000, 5, ['SUV', 'Large', 'Family', 'Luxury']),
    ("morning 1.0", "G", 15.1, 76, 13150000, 1, ['Small', 'FuelEfficient']),
    ("niro 1.6H", "H", 20.8, 105, 28560000, 2, ['Hybrid', 'FuelEfficient']),
    ("niro-ev", "E", 5.3, 150, 51140000, 2, ['Electric', 'EcoFriendly']),
    ("niro-pius", "E", 5.3, 150, 46000000, 2, ['Electric', 'EcoFriendly']),
    ("ray 1.0", "G", 13, 76, 13900000, 1, ['Small', 'CargoSpace']),
    ("ray-ev", "E", 5.1, 64.3, 27750000, 1, ['Small', 'CargoSpace', 'EcoFriendly']),
    ("seltos 1.6T", "G", 12.8, 198, 21860000, 3, ['SUV', 'Small']),
    ("seltos 2.0", "G", 12.9, 149, 20870000, 3, ['SUV', 'Small']),
    ("sorento 1.6TH", "H", 15.7, 180, 39290000, 4, ['SUV', 'Large', 'Family', 'CargoSpace', 'Hybrid']),
    ("sorento 2.2", "D", 14.3, 194, 35060000, 4, ['SUV', 'Large', 'Family', 'CargoSpace']),
    ("sorento 2.5T", "G", 10.8, 281, 35060000, 4, ['SUV', 'Large', 'Family', 'CargoSpace']),
    ("sportage 1.6T", "G", 12.3, 180, 25370000, 3, ['SUV', 'Large', 'Family', 'CargoSpace']),
    ("sportage 1.6TH", "H", 16.7, 180, 33560000, 3, ['SUV', 'Hybrid', 'FuelEfficient', 'Family', 'CargoSpace']),
    ("sportage 2.0", "D", 14.5, 184, 25370000, 3, ['SUV', 'Large', 'Family', 'CargoSpace'])
]

# 선호 항목 목록 (단일 선택)
possible_preferences = [
    'Small', 'Large', 'FuelEfficient', 'Powerful', 'SUV', 'Sedan', 'EcoFriendly', 'Luxury',
    'Electric', 'Family', 'Sporty', 'Hybrid', 'CargoSpace'
]

# 직업 목록
possible_jobs = [
    'Student', 'Office Worker', 'Salesman', 'Manager', 'Freelancer', 'Engineer', 'Retired',
    'Entrepreneur', 'Part-time Worker', 'Chairman', 'Teacher', 'Doctor', 'Designer'
]

# 사용자 데이터 생성 함수
def generate_users(num_users):
    user_data = []
    for _ in range(num_users):
        age = random.randint(18, 75)

        # 나이별 연봉 설정
        if age < 30:
            income = random.randint(22000000, 40000000)
        elif 30 <= age < 40:
            income = random.randint(35000000, 60000000)
        elif 40 <= age < 50:
            income = random.randint(40000000, 70000000)
        elif 50 <= age < 60:
            income = random.randint(35000000, 60000000)
        elif 60 <= age < 70:
            income = random.randint(25000000, 60000000)
        else:
            income = random.randint(20000000, 30000000)

        # 직업 선택
        job = random.choice(possible_jobs)

        # 차량 사용 목적
        usage = random.choice(['Commute', 'Business Trips', 'Family', 'Leisure', 'Off-Road'])

        # 위치 (랜덤 도시)
        location = faker.city()

        # 선호 항목 1~2개 선택 (대부분 2개)
        preference_count = random.choices([1, 2], weights=[0.2, 0.8])[0]
        preferences = random.sample(possible_preferences, preference_count)

        user_data.append((age, job, income, usage, location, ','.join(preferences)))
    return user_data


# 사용자-차량 평점 데이터 생성 함수
def generate_ratings(num_ratings, num_users):
    rating_data = []
    for _ in range(num_ratings):
        user_id = random.randint(1, num_users)

        # 사용자의 연봉과 선호 항목 기반으로 선택 가능한 차량 필터링
        cursor.execute("SELECT age, income, preferences FROM RUsers WHERE userId = %s", (user_id,))
        user = cursor.fetchone()

        if user:
            _, income, preferences = user
            user_preferences = preferences.split(',')
            eligible_cars = [car for car in cars if car[4] <= income * 1.2]

            # 선호 조건을 포함하는 차량의 경우 더 높은 확률로 선택
            preferred_cars = [car for car in eligible_cars if any(pref in car[6] for pref in user_preferences)]
            if preferred_cars:
                car = random.choice(preferred_cars)
                # 선호 조건과 일치하는 차량에 대해 높은 평점을 부여할 확률 증가
                rating = random.choices([5, 4, 3, 2, 1], weights=[40, 45, 10, 4, 1])[0]
            else:
                car = random.choice(eligible_cars)
                # 선호 조건과 일치하지 않는 차량에도 중간 평점을 줄 확률 증가
                rating = random.choices([3, 4, 2, 1], weights=[40, 30, 20, 10])[0]

            feedback = faker.sentence()
            rating_data.append((user_id, cars.index(car) + 1, rating, feedback))
    return rating_data


# 데이터 삽입 함수
def insert_data(num_users=1000000, num_ratings=2000000):
    # 사용자 데이터 삽입
    cursor.executemany(
        "INSERT INTO RUsers (age, job, income, carUsage, location, preferences) VALUES (%s, %s, %s, %s, %s, %s)",
        generate_users(num_users)
    )
    conn.commit()

    # 차량 데이터 삽입
    cursor.executemany(
        "INSERT INTO RCars (trimName, fuelType, mpgRate, psRate, priceRate, sizeRate) VALUES (%s, %s, %s, %s, %s, %s)",
        [(car[0], car[1], car[2], car[3], car[4], car[5]) for car in cars]
    )
    conn.commit()

    # 차량 태그 데이터 삽입
    for car_id, car in enumerate(cars, start=1):
        tags = car[6]  # 차량의 태그 리스트 가져오기
        for tag in tags:
            cursor.execute(
                "INSERT INTO RCarTags (carId, tagName) VALUES (%s, %s)",
                (car_id, tag)
            )
    conn.commit()

    # 사용자-차량 평점 데이터 삽입
    cursor.executemany(
        "INSERT INTO RUserCarRatings (userId, carId, rating, feedback) VALUES (%s, %s, %s, %s)",
        generate_ratings(num_ratings, num_users)
    )
    conn.commit()

try:
    insert_data()
    print("데이터 삽입 완료")
except mysql.connector.Error as err:
    print(f"데이터 삽입 중 오류: {err}")
finally:
    cursor.close()
    conn.close()
