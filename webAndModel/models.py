from app import db
import time


class Picture(db.Model):
    __tablename__ = 'picture'
    # 图片的id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 图片的名称
    name = db.Column(db.String(100))
    # 后缀名
    suffix = db.Column(db.String(100))
    # 地址
    url = db.Column(db.String(100))
    # 上传或者重建的时间
    changetime = db.Column(db.String(20))
    # 行为:Bicubic,SRCNN,Origin,Upscale_X
    # Bicubic:模糊处理,双三次插值
    # SRCNN:卷积神经网络处理
    # Origin:原图或者没有处理
    # Upscale_X:放大多少倍数,如Upscale_3X表示放大3倍
    action = db.Column(db.String(20))
    # 原图id
    # 如果是原图的话,表示为-1
    orig_id = db.Column(db.Integer)

    def __init__(self, name, url, action, orig_id):
        self.name = name
        self.suffix = name[name.find('.') + 1:]
        self.url = url
        self.changetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.action = action
        self.orig_id = orig_id

    def __repr__(self):
        return '<Picture %s %s %s %s>' % (self.name, self.url, self.changetime, self.action)
