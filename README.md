# **Face Recognition Software**

## **GUI implementation**

> Author: Sihan Chen

---
## **Project structure**

```
+--face_recognition
|    +--identification.py
|    +--README.md
|    +--search.py
|    +--test_images.py
|    +--__init__.py
+--ui_with_tkinter
|    +--face_recognition_ui.py
|    +--__init__.py
+--resources
|    +--dlib_face_recognition_resnet_model_v1.dat
|    +--Entrance.png
|    +--Entrance_EnglishVersion.jpg
|    +--shape_predictor_68_face_landmarks.dat
+--camera_photo
|    +--README.md
+--camera_photo_identification
|    +--README.md
+--default_label_identificationcd 
|    +--chensihan.JPG
|    +--README.md
+--default_picture_labels
|    +--ChenSihan.jpg
|    +--kobe.jpg
|    +--README.md
+--default_search_labels
|    +--AndreIguodala.jpg
|    +--ChenSihan.JPG
|    +--Curry.jpg
|    +--kobe.jpg
|    +--LiZongdi.jpg
|    +--NickYoung.jpg
|    +--Obama.jpg
|    +--README.md
|    +--ShaoYifan.jpg
|    +--TangYixin.jpg
|    +--thompson.jpg
|    +--ZhangRuoyun.jpg
+--README.md
```

## **Entrance interface**

> Entrance picture designer: ShiYing Hou

![entrance](README_resource/entrance.png)

## **Core Functions Introduction**

### **face predict**
#### *Image predict*

![ans2](README_resource/ans2.png)

#### *Camaera predict*

> My friend and me

![C&W](README_resource/answer_camera_faces.png)

### **face identification**

#### *Identification by emotions (current blinking/smiling in use)*

![emotions](README_resource/emotions.png)
* Choose the action you need to do to show you are a live body rather than a picture
* First the `Identification` function will call the camera to identify the user
* Them when you do certain actions ( Blink or Smile)
* You will be accepted

![ans_identification](README_resource/identification_ans.png)

### **Face Search**

#### *Search Curry, Obama and Iguodala*
![p3](README_resource/search_p3.png)

![ans3](README_resource/search_ans3.png)
#### *Search my classmate and me*

![p2](README_resource/search_p2.png)

![ans2](README_resource/search_ans2.png)

#### *More...*
![ans3](README_resource/search_answer.png)

---

> #  *Thanks for reading!*