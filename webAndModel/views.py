import json
import os
from io import BytesIO

import tensorflow as tf
from PIL import Image
from flask import render_template, request, jsonify

from app import app, db
from fastdfs.fastdfsUtil import *
from srcnn.model import *
from webAndModel.models import Picture

# fastdfs配置
fastdfs_client = os.path.join(os.getcwd(), "fastdfs", 'client.conf')
fdfs_client = Fdfs(fastdfs_client)
fdfs_addr = 'http://192.168.158.20:88/'


@app.route('/')
def index():
    pics = Picture.query.filter_by(action='Thumbnail_50x50').order_by(Picture.changetime.desc()).limit(10).all()
    picList = []
    picTemp = []
    counter = 0
    for pic in pics:
        if counter == 5:
            picList.append(picTemp)
            counter = 0
            picTemp = []
        picTemp.append(pic)
        counter += 1
    if counter != 0:
        picList.append(picTemp)
    return render_template('index.html', picList=picList)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = f.filename
        suffix = filename[filename.find('.') + 1:]
        f = f.read()
        url = fdfs_addr + fdfs_client.uploadbyBuffer(f, suffix)
        name = url[url.rfind('/') + 1:]
        pic = Picture(name, url, 'Origin', -1)
        db.session.add(pic)
        db.session.flush()
        db.session.commit()
        url = convertToThumbnail(f, name, suffix)
    return jsonify(code=200, message="success upload", url=url, id=pic.id)


def convertToThumbnail(f, orig_name, suffix):
    bytes_stream = BytesIO(f)
    img = Image.open(bytes_stream)
    img = img.resize((50, 50), Image.BILINEAR)
    f = BytesIO()
    img.save(f, format='PNG')
    f = f.getvalue()
    url = fdfs_addr + fdfs_client.uploadbyBuffer(f, suffix)
    name = url[url.rfind('/') + 1:]
    orig_pic = Picture.query.filter_by(name=orig_name).first()
    pic = Picture(name, url, 'Thumbnail_50x50', orig_pic.id)
    db.session.add(pic)
    db.session.commit()
    return url


@app.route('/detail/<picid>', methods=['GET', 'POST'])
def detail(picid):
    pictures = Picture.query.filter_by(orig_id=picid).all()
    pictures.insert(0, Picture.query.filter_by(id=picid).first())
    flag = True
    picDictList = []
    picActionList = []
    for pic in pictures:
        picContent = fdfs_client.downloadbyBuffer(pic.url[len(fdfs_addr):])
        bytes_stream = BytesIO(picContent)
        img = Image.open(bytes_stream)
        size = img.size
        if pic.action == 'Origin' and (size[0] > 800 or size[1] > 800):
            flag = False
        dict = {'pic': pic, 'width': size[0], 'height': size[1]}
        picDictList.append(dict)
        picActionList.append(pic.action)
    return render_template('detail.html', picDictList=picDictList, picActionList=picActionList, flag=flag)


@app.route("/superresolution", methods=["POST", "GET"])
def superresolution():
    # 查询是否已经存在超分辨率处理的图片
    data = json.loads(request.get_data(as_text=True))
    picid = data['picid']
    return srcnn_process(picid, 'SRCNN')


@app.route('/upscaling', methods=['GET', 'POST'])
def upscaling():
    data = json.loads(request.get_data(as_text=True))
    times = data['times']
    picid = data['picid']
    return srcnn_process(picid, 'Upscale_' + times + 'X', times)


def srcnn_process(picid, action, times=1):
    srcnnpic = Picture.query.filter_by(action=action, orig_id=picid).first()
    if srcnnpic != None:
        return jsonify(code=400, message="The picture has been processed")
    pic = Picture.query.filter_by(id=picid).first()
    picContent = fdfs_client.downloadbyBuffer(pic.url[len(fdfs_addr):])
    img = cv.imdecode(np.frombuffer(picContent, np.uint8), cv.IMREAD_COLOR)
    with tf.Session() as sess:
        srcnn = SRCNN(sess, "checkpoint")
        if action == 'SRCNN':
            img = srcnn.superresolution(img)
        else:
            img = srcnn.upscaling(img, int(times), True)
    size = img.shape
    img = Image.fromarray(img)
    f = BytesIO()
    img.save(f, format='PNG')
    f = f.getvalue()
    # 保存并上传数据库
    url = fdfs_addr + fdfs_client.uploadbyBuffer(f, pic.suffix)
    picname = url[url.rfind('/') + 1:]
    newpic = Picture(picname, url, action, pic.id)
    db.session.add(newpic)
    db.session.flush()
    db.session.commit()
    return jsonify(code=200, message="success " + action, name=picname, id=newpic.id, url=url, action=action,
                   width=size[0], height=size[1])


@app.route("/delete", methods=["POST", "GET"])
def delete():
    data = json.loads(request.get_data(as_text=True))
    pictureId = data['pictureId']
    pictureAction = data['pictureAction']
    pic = Picture.query.filter_by(id=pictureId).first()
    fdfs_client.delete(pic.url[len(fdfs_addr):])
    db.session.delete(pic)
    db.session.commit()
    # 如果是原图,则删除全部
    if pictureAction == 'Origin':
        pictures = Picture.query.filter_by(orig_id=pictureId).all();
        for pic in pictures:
            fdfs_client.delete(pic.url[len(fdfs_addr):])
            db.session.delete(pic)
        db.session.commit()
        return jsonify(code=200, message="The original and related pictures have been deleted ")
    else:
        return jsonify(code=201, message="This picture has been deleted ", pictureId=data['pictureId'],
                       pictureAction=data['pictureAction'])

@app.route("/compare/<id>", methods=["POST", "GET"])
def compare(id):
    times = id[id.rfind("_") + 1:id.rfind("X")]
    id = id[0:id.find("_")]
    cur_picture = Picture.query.filter_by(id=id).first()
    # 原图
    pic = Picture.query.filter_by(id=cur_picture.orig_id).first()
    # bicubicUpscale_3x
    bicubicpic = Picture.query.filter_by(action='bicubicUpscale_'+times+'x', orig_id=pic.id).first()
    if bicubicpic != None:
        return render_template('compare.html', url=cur_picture.url, newurl=bicubicpic.url, newId=bicubicpic.id)
    picContent = fdfs_client.downloadbyBuffer(pic.url[len(fdfs_addr):])
    img = cv.imdecode(np.frombuffer(picContent, np.uint8), cv.IMREAD_COLOR)
    with tf.Session() as sess:
        srcnn = SRCNN(sess,"checkpoint")
        img = srcnn.upscaling(img, int(times), False)
    img = Image.fromarray(img)
    f = BytesIO()
    img.save(f, format='PNG')
    f = f.getvalue()
    url = fdfs_addr + fdfs_client.uploadbyBuffer(f, pic.suffix)
    picname = url[url.rfind('/') + 1:]
    newpic = Picture(picname, url, 'bicubicUpscale_'+times+'x', pic.id)
    db.session.add(newpic)
    db.session.flush()
    db.session.commit()
    return render_template('compare.html', url=cur_picture.url, newurl=url, newId=newpic.id)

@app.route("/closecompare", methods=["POST", "GET"])
def closecompare():
    data = json.loads(request.get_data(as_text=True))
    id = data['pictureId']
    pic = Picture.query.filter_by(id=id).first()
    fdfs_client.delete(pic.url[len(fdfs_addr):])
    db.session.delete(pic)
    db.session.commit()
    return jsonify(code=200, message="close success")