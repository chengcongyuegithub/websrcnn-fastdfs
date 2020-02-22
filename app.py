from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import configs

# 操作数据库的对象
db = SQLAlchemy()
# 操作flask的对象
app = Flask(__name__)
# 加载配置
app.config.from_object(configs)
# db绑定app
db.init_app(app)

from webAndModel.models import *
from webAndModel.views import *