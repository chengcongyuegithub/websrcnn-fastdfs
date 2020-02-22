import os
import tensorflow as tf
from srcnn.utils import *

# 定义SRCNN类
class SRCNN(object):
    def __init__(self, sess, checkpoint_dir):
        self.sess = sess
        self.checkpoint_dir = checkpoint_dir
        self.build_model()

    # 搭建网络
    def build_model(self):
        self.images = tf.placeholder(tf.float32, [None, 33, 33, 1], name='images')
        self.labels = tf.placeholder(tf.float32, [None, 21, 21, 1], name='labels')
        # 第一层CNN：对输入图片的特征提取。（9 x 9 x 64卷积核）
        # 第二层CNN：对第一层提取的特征的非线性映射（1 x 1 x 32卷积核）
        # 第三层CNN：对映射后的特征进行重建，生成高分辨率图像（5 x 5 x 1卷积核）
        # 权重
        self.weights = {
            # 论文中为提高训练速度的设置 n1=32 n2=16
            'w1': tf.Variable(tf.random_normal([9, 9, 1, 64], stddev=1e-3), name='w1'),
            'w2': tf.Variable(tf.random_normal([1, 1, 64, 32], stddev=1e-3), name='w2'),
            'w3': tf.Variable(tf.random_normal([5, 5, 32, 1], stddev=1e-3), name='w3')
        }
        # 偏置
        self.biases = {
            'b1': tf.Variable(tf.zeros([64]), name='b1'),
            'b2': tf.Variable(tf.zeros([32]), name='b2'),
            'b3': tf.Variable(tf.zeros([1]), name='b3')
        }
        self.pred = self.model()
        # 以MSE作为损耗函数
        self.loss = tf.reduce_mean(tf.square(self.labels - self.pred))
        self.saver = tf.train.Saver()

    def superresolution(self, img):
        tf.global_variables_initializer().run()
        if self.load(self.checkpoint_dir):
            print(" [*] Load SUCCESS")
        else:
            print(" [!] Load failed...")
        data, color, nx, ny = parpare_for_superresolution(self.sess, img)
        conv_out = self.pred.eval({self.images: data})
        conv_out = merge(conv_out, [nx, ny])
        conv_out = conv_out.squeeze()
        result_bw = revert(conv_out)
        result = np.zeros([result_bw.shape[0], result_bw.shape[1], 3], dtype=np.uint8)
        result[:, :, 0] = result_bw
        result[:, :, 1:3] = color
        result = cv.cvtColor(result, cv.COLOR_YCrCb2RGB)
        return result

    def upscaling(self, img, scale, flag):
        tf.global_variables_initializer().run()
        if self.load(self.checkpoint_dir):
            print(" [*] Load SUCCESS")
        else:
            print(" [!] Load failed...")
        data, label, color, nx, ny = parpare_for_upscaling(self.sess, img, scale)
        if flag:
            conv_out = self.pred.eval({self.images: data})
            conv_out = merge(conv_out, [nx, ny])
            result_bw = conv_out.squeeze()
            result_bw = revert(result_bw)
        else:
            conv_out = merge(label, [nx, ny])
            result_bw = conv_out.squeeze()
            result_bw = revert(result_bw)
        result = np.zeros([result_bw.shape[0], result_bw.shape[1], 3], dtype=np.uint8)
        result[:, :, 0] = result_bw
        result[:, :, 1:3] = color
        result = cv.cvtColor(result, cv.COLOR_YCrCb2RGB)
        return result

    def model(self):
        conv1 = tf.nn.relu(
            tf.nn.conv2d(self.images, self.weights['w1'], strides=[1, 1, 1, 1], padding='VALID') + self.biases['b1'])
        conv2 = tf.nn.relu(
            tf.nn.conv2d(conv1, self.weights['w2'], strides=[1, 1, 1, 1], padding='VALID') + self.biases['b2'])
        conv3 = tf.nn.conv2d(conv2, self.weights['w3'], strides=[1, 1, 1, 1], padding='VALID') + self.biases['b3']
        return conv3

    def load(self, checkpoint_dir):
        print(" [*] Reading checkpoints...")
        model_dir = "%s_%s" % ("srcnn", 21)
        checkpoint_dir = os.path.join(checkpoint_dir, model_dir)
        ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
        if ckpt and ckpt.model_checkpoint_path:
            ckpt_name = os.path.basename(ckpt.model_checkpoint_path)
            s = os.path.join(checkpoint_dir, ckpt_name)
            print(s)
            self.saver.restore(self.sess, s)
            return True, ckpt_name[12:]
        else:
            return False
