import dlib                     # 人脸识别的库dlib
import numpy as np              # 数据处理的库numpy
import cv2                      # 图像处理的库OpenCv
from skimage import io
import os, dlib, glob, numpy
from tkinter import messagebox as mb


def identify(identification_state):
    # 使用特征提取器get_frontal_face_detector
    detector = dlib.get_frontal_face_detector()
    # dlib的68点模型，使用作者训练好的特征预测器
    predictor = dlib.shape_predictor(r"..\resources\shape_predictor_68_face_landmarks.dat")

    facerec = dlib.face_recognition_model_v1(r"..\resources\dlib_face_recognition_resnet_model_v1.dat")

    # 建cv2摄像头对象，这里使用电脑自带摄像头，如果接了外部摄像头，则自动切换到外部摄像头
    cap = cv2.VideoCapture(0)
    # 设置视频参数，propId设置的视频参数，value设置的参数值
    cap.set(3, 480)
    # 截图screenshoot的计数器
    # cnt = 0

    # 眉毛直线拟合数据缓冲
    # line_brow_x = []
    # line_brow_y = []

    # cap.isOpened（） 返回true/false 检查初始化是否成功
    while cap.isOpened():
        # cap.read()
        # 返回两个值：
        #    一个布尔值true/false，用来判断读取视频是否成功/是否到视频末尾
        #    图像对象，图像的三维矩阵
        flag, im_rd = cap.read()

        # 每帧数据延时1ms，延时为0读取的是静态帧
        k = cv2.waitKey(1)

        # 取灰度
        img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)

        # 使用人脸检测器检测每一帧图像中的人脸。并返回人脸数rects
        faces = detector(img_gray, 0)

        # 待会要显示在屏幕上的字体
        font = cv2.FONT_HERSHEY_SIMPLEX

        # 如果检测到人脸
        if len(faces) != 0:
            # 对每个人脸都标出68个特征点
            for i in range(len(faces)):
                # enumerate方法同时返回数据对象的索引和数据，k为索引，d为faces中的对象
                for k, d in enumerate(faces):
                    # 计算大小，并划出人脸矩形，保存到后端进行加工
                    pos_start = tuple([d.left(), d.top()])
                    pos_end = tuple([d.right(), d.bottom()])

                    # 计算矩形框大小
                    height = d.bottom() - d.top()
                    width = d.right() - d.left()
                    im_blank = np.zeros((height, width, 3), np.uint8)
                    for ii in range(height):
                        for jj in range(width):
                            im_blank[ii][jj] = im_rd[d.top() + ii][d.left() + jj]
                    # 存储人脸图像文件
                    path_save = r"../camera_photo_identification/" + "img_face_" + ".jpg"

                    cv2.imwrite(path_save, im_blank)
                    # 有匹配显示人脸名，没匹配就返回空
                    # faces_folder_path='../default_picture_labels'
                    flag = compare(path_save, predictor , detector, facerec, faces_folder_path='../default_label_identification/' )
                    if not flag:
                        print(flag)
                        cap.release()
                        cv2.destroyAllWindows()
                        return {'name': 'No match', 'identification': "fail"}
                    # flag[0]代表人名
                    cv2.putText(im_rd, flag[0], (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (0, 0, 255), 2, 4)


                    # 用红色矩形框出人脸
                    cv2.rectangle(im_rd, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255))
                    # 计算人脸热别框边长
                    face_width = d.right() - d.left()

                    # 使用预测器得到68点数据的坐标
                    shape = predictor(im_rd, d)
                    # 圆圈显示每个特征点
                    for i in range(68):
                        cv2.circle(im_rd, (shape.part(i).x, shape.part(i).y), 2, (0, 255, 0), -1, 8)
                        #cv2.putText(im_rd, str(i), (shape.part(i).x, shape.part(i).y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        #            (255, 255, 255))

                    # 分析任意n点的位置关系来作为表情识别的依据
                    # mouth_width = (shape.part(54).x - shape.part(48).x) / face_width  # 嘴巴咧开程度
                    # mouth_higth = (shape.part(66).y - shape.part(62).y) / face_width  # 嘴巴张开程度
                    # print("嘴巴宽度与识别框宽度之比：",mouth_width_arv)
                    # print("嘴巴高度与识别框高度之比：",mouth_higth_arv)

                    # 眼睛睁开程度

                    # eye_hight = (eye_sum / 4) / face_width
                    # print("眼睛睁开距离与识别框高度之比：",round(eye_open/face_width,3))
                    if identification_state == "eye identification":
                        eye_sum = (shape.part(41).y - shape.part(36).y + shape.part(40).y - shape.part(37).y +
                                   shape.part(39).y - shape.part(38).y +
                                   shape.part(47).y - shape.part(42).y + shape.part(46).y - shape.part(43).y +
                                   shape.part(45).y - shape.part(44).y)
    # return
                        if eye_sum < 30:
                            cap.release()
                            cv2.destroyAllWindows()
                            return {'name': flag[0], 'identification': "success"}

                    elif identification_state == "smile identification":
                        mouth_width = (shape.part(54).x - shape.part(48).x) / face_width  # 嘴巴咧开程度
                        mouth_higth = (shape.part(66).y - shape.part(62).y) / face_width  # 嘴巴张开程度

                        if mouth_width > 0.4:
                            cap.release()
                            cv2.destroyAllWindows()
                            return{'name': flag[0], 'identification': "success"}



                    # 分情况讨论
                    # 张嘴，可能是开心或者惊讶
                    # if round(mouth_higth >= 0.03):
                    #     if eye_hight >= 0.056:
                    #         cv2.putText(im_rd, "amazing", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    #                     (0, 0, 255), 2, 4)
                    #     else:
                    #         cv2.putText(im_rd, "happy", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    #                     (0, 0, 255), 2, 4)

            # 标出人脸数
            cv2.putText(im_rd, "Faces: "+str(len(faces)), (20,50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
        else:
            # 没有检测到人脸
            cv2.putText(im_rd, "No Face", (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

        # 添加说明
        # im_rd = cv2.putText(im_rd, "S: screenshot", (20, 400), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
        # im_rd = cv2.putText(im_rd, "Q: quit", (20, 450), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

        # # 按下s键截图保存
        # if (k == ord('s')):
        #     cnt+=1
        #     cv2.imwrite("screenshoot"+str(cnt)+".jpg", im_rd)
        #
        # # 按下q键退出
        # if(k == ord('q')):
        #     break

        # 窗口显示
        cv2.imshow("camera", im_rd)

    # 释放摄像头
    cap.release()

    # 删除建立的窗口
    cv2.destroyAllWindows()



def compare(path_save,predictor,detector, facerec, faces_folder_path):
    descriptors = []
    # 加载标签图片
    for f in glob.glob(os.path.join(faces_folder_path + '\/*')):
        print("Processing file:{}".format(f))
        img = io.imread(f)
        # The 1 in the second argument indicates that we should upsample the image
        # 1 time.  This will make everything bigger and allow us to detect more
        # faces.
        # 检测人脸数
        dets = detector(img, 1)
        # print("Number of faces detected: {}".format(len(dets)))

        for k, d, in enumerate(dets):
            # 人脸关键点检测器sp
            shape = predictor(img, d)
            # 画出人脸区域和关键点
            # win.clear_overlay()
            # win.add_overlay(d)
            # win.add_overlay(shape)
            # 3.描述子提取，128D向量
            face_descriptor = facerec.compute_face_descriptor(img, shape)
            # 转换为numpy array
            v = numpy.array(face_descriptor)
            descriptors.append(v)
            # print(descriptors)

    # 加载camera图片
    img = io.imread(path_save)
    dets = detector(img, 1)

    dist = []
    for k, d, in enumerate(dets):
        shape = predictor(img, d)

        face_descriptor = facerec.compute_face_descriptor(img, shape)

        d_test = numpy.array(face_descriptor)
        # 计算欧式距离
        for i in descriptors:
            dist_ = numpy.linalg.norm(i - d_test)
            dist.append(dist_)
    # print(dist_)

        # 标签库加工，把参数标签文件夹路径中的几个jpg的人名拿出来组成标签列表
        # print(1)
        list_picture_labels = os.listdir(faces_folder_path)
        candidate = []
        for i in list_picture_labels:
            if i[-4:] in ['.jpg', '.JPG', '.PNG', '.png']:
                candidate.append(i[:-4])
            else:
                mb.showwarning('warning', "file invalid!")
        # candidate=['xinyuanjieyi','qiaobenhuannai','shiyuanlimei','fengtimo']
        # c_d = [{}] * len(dets)
        answer = []
        print(dist)

    # c_d记录人脸的标签与可能性值的信息
        c_d = dict(zip(candidate, dist))

        cd_sorted = sorted(c_d.items(), key=lambda d: d[1])
        print(cd_sorted)
    # 返回信息
    # 若dist小于0.4则识别成功，大于则查无此人
        if cd_sorted[0][1] < 0.4:
            answer.append(cd_sorted[0][0])  # 查到的人名
            print("find!")
            return answer
        else:
            print("cannot find!")
            return answer
