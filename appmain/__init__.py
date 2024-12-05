from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)

# 앱 설정
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'KIADB'

app.config['SECRET_KEY'] = 'ZAQ1SW2XE3CD4VFR'  # 여기서 'your-secret-key'는 안전한 랜덤 값으로 바꿔야 합니다.

mysql = MySQL(app)
CORS(app)  # CORS 적용

from appmain.routes import main  # 라우트를 등록하는 코드는 설정 다음에 나와야 함
app.register_blueprint(main)
