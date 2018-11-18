import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import sys, os, dlib, glob, numpy
from skimage import io

from tkinter import messagebox as mb
# 传一个路径, 一个状态（待实现）
# 返回结果，处理后的图片


def recognition(img_path, test_folder_path='../default_picture_labels'):
    # if state not in {'recognition', 'search'}:
    #     raise ValueError('{} not valid'.format(state))
    # 候选人脸文件夹
    # face_folder_path
    # if state == 'recognition':
    # 1.加载正脸检测器
    detector = dlib.get_frontal_face_detector()

    # 2.加载人脸关键点检测器 shape_predictor_68_face_landmarks.dat
    sp = dlib.shape_predictor(r"..\resources\shape_predictor_68_face_landmarks.dat")

    # 3. 加载人脸识别模型
    facerec = dlib.face_recognition_model_v1(r"..\resources\dlib_face_recognition_resnet_model_v1.dat")

    # image_data = io.imread(image_path)

    win = dlib.image_window()

    descriptors = []

    for f in glob.glob(os.path.join(test_folder_path, "*.jpg")):
        print("Processing file:{}".format(f))
        # 加载标签图片
        img = io.imread(f)

        # The 1 in the second argument indicates that we should upsample the image
        # 1 time.  This will make everything bigger and allow us to detect more
        # faces.

        # 检测人脸数
        dets = detector(img, 1)
        print("Number of faces detected: {}".format(len(dets)))


        for k, d, in enumerate(dets):
            #人脸关键点检测器sp
            shape = sp(img,d)
            # 画出人脸区域和关键点
            win.clear_overlay()
            win.add_overlay(d)
            win.add_overlay(shape)
            # 3.描述子提取，128D向量
            face_descriptor = facerec.compute_face_descriptor(img, shape)
            # 转换为numpy array
            v = numpy.array(face_descriptor)
            descriptors.append(v)
            # print(descriptors)


    # 加载需测的图片
    img = io.imread(img_path)
    dets = detector(img, 1)
    print("Number of faces detected: {}".format(len(dets)))
    # 为len(dets)张人脸各建一个列表
    dist = []
    id = 0
    for k, d, in enumerate(dets):
        dist_all = []
        shape = sp(img, d)

        face_descriptor = facerec.compute_face_descriptor(img, shape)

        d_test = numpy.array(face_descriptor)
    # 计算欧式距离
        for i in descriptors:
            dist_ = numpy.linalg.norm(i-d_test)
            dist_all.append(dist_)  # 第k张人脸与第i个标签的比较数据存入列表
        dist.append(dist_all)

    print(dist)

    # 标签库加工，把参数标签文件夹路径中的几个jpg的人名拿出来组成标签列表
    print(1)
    list_picture_labels = os.listdir(test_folder_path)
    candidate = []
    for i in list_picture_labels:
        if i[-4:] in ['.jpg', '.JPG', '.PNG', '.png']:
            candidate.append(i[:-4])
        else:
            mb.showwarning('warning', "file invalid!")
    # candidate=['xinyuanjieyi','qiaobenhuannai','shiyuanlimei','fengtimo']
    c_d = [{}] * len(dets)
    answer = []
    print(dist)
    for i in range(len(dets)):
        # c_d[i]记录第i张人脸的标签与可能性值的信息
        c_d[i] = dict(zip(candidate, dist[i]))

        cd_sorted = sorted(c_d[i].items(), key=lambda d:d[1])
        print(cd_sorted)
    # 返回信息
    # 若dist小于0.4则识别成功，大于则查无此人
        if cd_sorted[0][1] < 0.4:
            answer.append(cd_sorted[0][0])  # 查到的人名
    # if cd_sorted[0][1] > 0.4:
    #     answer = "Cannot find a person in the label database!"
    # else:
    #     answer = "The person is:"+cd_sorted[0][0]
    #     print("\n The person is:", cd_sorted[0][0])

    # if answer is not None:
    #     answer.show_information()

    # dlib.hit_enter_to_continue()
    return answer


#return answer
#get face from camera

def camera_recognition(test_folder_path='../default_picture_labels'):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('../resources/shape_predictor_68_face_landmarks.dat')

    # 创建cv2摄像头对象
    cap = cv2.VideoCapture(0)

    # cap.set(proID,value)
    # 设置视频参数，propId设置的视频参数，value设置的参数值
    cap.set(3, 480)

    # 截图screenshoot的计数器
    cnt_ss = 0

    # 人脸截图的计数器
    cnt_p = 0

    # 保存
    path_save = r"../camera_photo/"

    # cap.isOpened() 返回true/false检查初始化是否成功
    while cap.isOpened():
        # cap.read()
        # 返回两个值:
        #    一个布尔值true/false，用来判断读取视频是否成功/是否到视频末尾
        #    图像对象，图像的三维矩阵q
        flag, im_rd = cap.read()

        # 每帧数据延时1ms，延时为0读取的是静态帧
        kk = cv2.waitKey(1)

        # 取灰度
        img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)

        # 人脸数rects
        rects = detector(img_gray, 0)

        # print(len(rects))

        # 设置接下来的字体
        font = cv2.FONT_HERSHEY_SIMPLEX

        if len(rects) != 0:
            # 检测到人脸

            # 矩形框
            for k, d in enumerate(rects):
                # 计算矩形大小
                pos_start = tuple([d.left(), d.top()])
                pos_end = tuple([d.right(), d.bottom()])

                # 计算矩形框大小
                height = d.bottom() - d.top()
                width = d.right() - d.left()

                # 根据人脸大小生成空的图像
                cv2.rectangle(im_rd, tuple([d.left(), d.top()]), tuple([d.right(), d.bottom()]), (0, 255, 255), 2)
                im_blank = np.zeros((height, width, 3), np.uint8)

                # 按下's'保存摄像头中的人脸到本地
                if kk == ord('s'):
                    cnt_p += 1
                    for ii in range(height):
                        for jj in range(width):
                            im_blank[ii][jj] = im_rd[d.top() + ii][d.left() + jj]
                    # 存储人脸图像文件
                    cv2.imwrite(path_save + "img_face_" + str(cnt_p) + ".jpg", im_blank)
                    print("写入本地：", path_save + "img_face_" + str(cnt_p) + ".jpg")

            # 显示人脸数
            cv2.putText(im_rd, "faces:" + str(len(rects)), (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

        else:
            # 没有检测到人脸
            cv2.putText(im_rd, "no face", (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

        # 添加说明
        im_rd = cv2.putText(im_rd, "s: save face", (20, 400), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
        im_rd = cv2.putText(im_rd, "q:quit", (20, 450), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)

        # 按下q键退出
        if kk == ord('q'):
            break
        cv2.startWindowThread()
        cv2.imshow("camera", im_rd)

    # 窗口显示
    # cv2.namedWindow("camera", 0)   # 摄像头窗口大小可调

    # 释放摄像
    cap.release()
    cv2.destroyWindow('camera')
    # 删除窗口


    # 这里用数据库识别
    answer = recognition(path_save + "img_face_" + str(cnt_p) + ".jpg",
                         test_folder_path=test_folder_path)
    # cv2.waitKey(0)
    # cv2.destroyALLWindows()

    return answer


# 是否要返回处理后的图片？待实现
# 高级模式：通过矩阵比较两个人之间的相似度，需要写入csv文件，undone