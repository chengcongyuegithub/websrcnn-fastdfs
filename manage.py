from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db, app

manager = Manager(app)
Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)  # 创建数据库映射命令


if __name__ == '__main__':
	manager.run()
