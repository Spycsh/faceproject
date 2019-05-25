import cv2                      # 图像处理的库OpenCv
from skimage import io
import dlib, numpy


def search(img_path, labels_list, threshold=0.5, answer_pic=False):
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

    # 只接受jpg文件
    for f in labels_list:
        path = '../default_search_labels/{}.jpg'.format(f)
        # print("Processing file:{}".format(path))
        # 加载标签图片
        try:
            img = io.imread(path)
        except FileNotFoundError as e:
            print('标签类型不是jpg,更换为png')
            path = '../default_search_labels/{}.png'.format(f)
            img = io.imread(path)

        # The 1 in the second argument indicates that we should upsample the image
        # 1 time.  This will make everything bigger and allow us to detect more
        # faces.

        # 检测人脸数
        dets = detector(img, 1)
        print("Number of faces detected: {}".format(len(dets)))

        for k, d, in enumerate(dets):
            # 人脸关键点检测器sp
            shape = sp(img, d)
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

    #  加载需测的图片
    img = io.imread(img_path)
    dets = detector(img, 1)
    print("Number of faces detected: {}".format(len(dets)))
    # 为len(dets)张人脸各建一个列表
    dist = []
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
    # list_picture_labels = os.listdir(test_folder_path)
    # candidate = []
    # for i in list_picture_labels:
    #     if i[-4:] in ['.jpg', '.JPG', '.PNG', '.png']:
    #         candidate.append(i[:-4])
    #     else:
    #         mb.showwarning('warning', "file invalid!")
    # candidate=['xinyuanjieyi','qiaobenhuannai','shiyuanlimei','fengtimo']

    candidate = labels_list
    c_d = [{}] * len(dets)
    answer = []
    print(dist)
    for i, d, in enumerate(dets):
        # c_d[i]记录第i张人脸的标签与可能性值的信息
        c_d[i] = dict(zip(candidate, dist[i]))

        cd_sorted = sorted(c_d[i].items(), key=lambda d:d[1])
        print(cd_sorted)
    # 返回信息
    # 若dist小于0.4则识别成功，大于则查无此人
    #     print(cd_sorted[0][1])
    #     print(threshold)
        if cd_sorted[0][1] < threshold:
            answer.append(cd_sorted[0][0])  # 查到的人名
            # print(d)
            # print(type(d))
            # 使用opencv在原图上画出人脸位置
            # 显示结果图
            if answer_pic == True:    # 得到结果图
                left_top = (dlib.rectangle.left(d), dlib.rectangle.top(d))
                right_bottom = (dlib.rectangle.right(d), dlib.rectangle.bottom(d))
                left_top_bottom = (dlib.rectangle.left(d), dlib.rectangle.bottom(d))  # 作为解释文字的左上坐标
                cv2.namedWindow("img", 0)
                cv2.rectangle(img, left_top, right_bottom, (0, 255, 0), 2, cv2.LINE_AA)

                # putText参数:照片 / 添加的文字 / 左上角坐标 / 字体 / 字体大小 / 颜色 / 字体粗细
                # putText(img, text, org, fontFace, fontScale, color, thickness=None, lineType=None,
                #         bottomLeftOrigin=None):
                cv2.putText(img, cd_sorted[0][0], left_top_bottom, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow("img", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))  # 转成ＢＧＲ显示

    # if cd_sorted[0][1] > 0.4:
    #     answer = "Cannot find a person in the label database!"
    # else:
    #     answer = "The person is:"+cd_sorted[0][0]
    #     print("\n The person is:", cd_sorted[0][0])
    # if answer is not None:
    #     answer.show_information()
    # dlib.hit_enter_to_continue()

    if len(answer) == 0:
        answer = "No Match"
    else:
        if len(answer) == 1:
            answer = '1 person found: ' + ''.join(answer)
        else:
            answer = str(len(answer)) + ' persons found: ' + ','.join(answer)
    print(answer)
    return answer
