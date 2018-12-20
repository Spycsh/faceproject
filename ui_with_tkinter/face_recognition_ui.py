from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mb
from face_recognition import test_images
from face_recognition import identification
from PIL import Image
from PIL import ImageTk


class FaceRecognition:
    def __init__(self):
        self.root = Tk()
        self.root.title('Face Recognition System')
        self.root.maxsize(width=1000, height=600)
        self.root.minsize(width=1000, height=600)
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.menuBar = Menu(self.root)
        self.root.config(menu=self.menuBar)  # 创建前先要实例化菜单
        self.help_menu = Menu(self.menuBar)

        self.menuBar.add_command(label='Predict', font=('Times New Roman', 8), command=self.enable_test_ui)
        self.menuBar.add_command(label='Identification', font=('Time New Roman', 8), command=self.enable_identification_ui)
# 变量设置

        self.enable_test = False
        self.enable_identification = False

        self.image_size = 100

        self.test_parameters = None
        self.test_par_x_scrollbar = None
        self.test_par_y_scrollbar = None

        self.test_image_path = None
        self.image_path_var = StringVar()

        #
        self.test_folder_path = None
        self.image_folder_path_var = StringVar()

        self.test_state = 'recognition'
        self.test_state_var = StringVar()

        #
        self.identification_state = 'eye identification'
        self.identification_state_var = StringVar()

        self.choose_ui_widgets = []
        self.choose_path_widgets = []

        self.chooses_box = None
        self.chooses_box_x_scrollbar = None
        self.chooses_box_y_scrollbar = None

        self.answer = []
        self.predict_image_data = None

        self.answer_box = None
        self.answer_x_scrollbar = None
        self.answer_y_scrollbar = None

        self.identification_answer_box = None
        self.identification_x_scrollbar = None
        self.identification_y_scrollbar = None


        # images list
        self.display = []



#主界面插入图片

        if self.enable_test is False and self.enable_identification is False:
            self.canvas = Canvas(self.root, width=1000, height=600)                     # 设置canvas
            self.image = Image.open('../resources/MainBG.jpg').resize((1000, 600))      # 打开图片调整大小
            self.canvas.image = ImageTk.PhotoImage(self.image)                          # 图片附着到canvas的图片上
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
            self.canvas.place(x=0, y=0)

        self.root.mainloop()


    def enable_test_ui(self):
        if self.enable_test:
            mb.showwarning('Warnining', 'The current ui is predict interface!')

        else:
            self.destroy_current_ui()
            self.enable_test = True
            self.create_test_ui()

    def enable_identification_ui(self):
        if self.enable_identification:
            mb.showwarning('Warnining', 'The current ui is identification interface!')
        else:
            self.destroy_current_ui()
            self.enable_identification = True
            self.create_identification_ui()

# 进入test ui
    def create_test_ui(self):
        self.enable_identification = False
        if self.image_path_var.get() == '':
            self.image_path_var.set('')
# image 路径
        self.choose_path_widgets.append(Label(self.root, text='path of the image', font=('Times New Roman',12), fg='blue'))
        self.choose_path_widgets[-1].place(x=10, y=55)

        self.choose_path_widgets.append(Button(self.root, text='Choose', font=('Times New Roman', 12), command=self.choose_file))
        self.choose_path_widgets[-1].place(x=400, y=51)

        self.choose_path_widgets.append(
            Entry(self.root, width=56, textvariable=self.image_path_var, font=('Times New Roman', 12)))
        self.choose_path_widgets[-1].place(x=10, y=85)
        # print(self.choose_path_widgets)
        if self.test_state_var.get() == '':
            self.test_state_var.set('recognition')
        # if self.test_state_var.get() != 'recognition':
        #     self.create_choose_label_ui()
# 选择功能
        Label(self.root, text='模式', font=('楷体', 12), fg='blue').place(x=10, y=10)
        # Checkbutton(self.root, text='人脸验证', font=('楷体', 12), variable=self.test_state_var,
        #             onvalue='verification', offvalue=0, command=self.choose_state).place(x=10, y=115)
        Checkbutton(self.root, text='recognition', font=('楷体', 12), variable=self.test_state_var,
                    onvalue='recognition', offvalue=0, command=self.choose_state).place(x=10, y=30)
        Checkbutton(self.root, text='camera recognition', font=('楷体', 12), variable=self.test_state_var,
                    onvalue='camera_recognition', offvalue=0, command=self.choose_state).place(x=300, y=30)

        if self.image_path_var.get() != '':
            self.display = []
            if self.test_state_var.get() == 'recognition':
                self.show_image(self.test_image_path, size=(500, 500), x=500, y=40)
            else:
                self.show_image(self.test_image_path, size=(500, 500), x=500, y=40)


        # if self.fit_data_var.get() == '':
        #     self.fit_data_var.set(FALSE)

        # Label(self.root, text='Use model that trained by all data',
        #           font=('Times New Roman', 12), fg='blue').place(x=10, y=245)
        # Radiobutton(self.root, text='Yes', font=('Times New Roman', 12), variable=self.fit_data_var, value=TRUE,
        #             command=self.choose_fit_data_var).place(x=340, y=245)
        # Radiobutton(self.root, text='No', font=('Times New Roman', 12), variable=self.fit_data_var, value=FALSE,
        #             command=self.choose_fit_data_var).place(x=400, y=245)

# 图片库 路径
        Label(self.root, text='path of the data folder', font=('Times New Roman', 12), fg='blue').place(x=10, y=125)
        Button(self.root, text='Choose', font=('Times New Roman', 12), command=self.choose_folder).place(x=400, y=120)

        Entry(self.root, width=56, textvariable=self.image_folder_path_var, font=('Times New Roman', 12)).place(x=10, y=155)

# parameters box
        Label(self.root, text='Check model\'s parameters', font=('Times New Roman', 12),
              fg='blue').place(x=150, y=240)
        self.test_parameters = Listbox(self.root, font=('Times New Roman', 12), width=56, height=6)

        self.test_parameters.place(x=10, y=290)
        self.test_par_x_scrollbar = Scrollbar(self.root, orient=HORIZONTAL)
        self.test_par_y_scrollbar = Scrollbar(self.root)
        self.test_par_x_scrollbar.place(x=10, y=270, width=458)
        self.test_par_y_scrollbar.place(x=462, y=285, height=130)
        self.test_parameters.config(xscrollcommand=self.test_par_x_scrollbar.set,
                                    yscrollcommand=self.test_par_y_scrollbar.set)
        self.test_par_x_scrollbar.config(command=self.test_parameters.xview)
        self.test_par_y_scrollbar.config(command=self.test_parameters.yview)

# start_test button
        Button(self.root, text='Start', font=('Times New Roman', 12), fg='DarkMagenta',
               command=self.start_test).place(x=200, y=200)
        # Button(self.root, text='Stop', font=('Times New Roman', 12), fg='blue',
        #        command=self.stop_test).place(x=270, y=490)

# answer box
        Label(self.root, text='Prediction', font=('Times New Roman', 12), fg='blue').place(x=200, y=417)

        self.answer_box = Listbox(self.root, font=('Times New Roman', 12), width=56, height=6)
        self.answer_box.place(x=10, y=467)
        self.answer_x_scrollbar = Scrollbar(self.root, orient=HORIZONTAL)
        self.answer_y_scrollbar = Scrollbar(self.root)
        self.answer_x_scrollbar.place(x=10, y=445, width=458)
        self.answer_y_scrollbar.place(x=462, y=470, height=120)
        self.answer_box.config(xscrollcommand=self.answer_x_scrollbar.set, yscrollcommand=self.answer_y_scrollbar.set)
        self.answer_x_scrollbar.config(command=self.answer_box.xview)
        self.answer_y_scrollbar.config(command=self.answer_box.yview)

        # parameter box添加参数描述
        self.insert_all_test_parameters()

    def create_identification_ui(self):
        self.enable_test = False

        if self.identification_state_var.get() == '':
            self.identification_state_var.set(' ')

        Label(self.root, text='模式', font=('楷体', 12), fg='blue').place(x=10, y=10)
        Checkbutton(self.root, text='眨眼验证', font=('楷体', 12), variable=self.identification_state_var,
                    onvalue='eye identification', offvalue=0, command=self.choose_state_identify).place(x=10, y=40)
        Checkbutton(self.root, text='微笑验证', font=('楷体', 12), variable=self.identification_state_var,
                    onvalue='smile identification', offvalue=0, command=self.choose_state_identify).place(x=400, y=40)

        Button(self.root, text='Start', font=('Times New Roman', 12), fg='DarkMagenta',
               command=self.start_identify).place(x=200, y=100)

        Label(self.root, text='Identification', font=('Times New Roman', 12), fg='blue').place(x=180, y=167)

        self.identification_answer_box = Listbox(self.root, font=('Times New Roman', 12), width=56, height=6)
        self.identification_answer_box.place(x=10, y=217)
        self.identification_x_scrollbar = Scrollbar(self.root, orient=HORIZONTAL)
        self.identification_y_scrollbar = Scrollbar(self.root)
        self.identification_x_scrollbar.place(x=10, y=195, width=458)
        self.identification_y_scrollbar.place(x=462, y=220, height=120)
        self.identification_answer_box.config(xscrollcommand=self.identification_x_scrollbar.set,
                                              yscrollcommand=self.identification_y_scrollbar.set)

        self.identification_x_scrollbar.config(command=self.identification_answer_box.xview)
        self.identification_y_scrollbar.config(command=self.identification_answer_box.yview)




    def choose_state(self):
        self.test_state = self.test_state_var.get()
        # if self.test_state == 'recognition':
        #     self.destroy_choose_label_ui()
        # else:
        #     self.create_choose_label_ui()

        # if self.test_image_path != '' and self.test_image_path is not None:
        self.display = []
        if self.test_state_var.get() == 'recognition':
            # print('aaa')
            self.create_choose_image_path_ui()
            # self.show_image(self.test_image_path, size=(500, 500), x=500, y=40)
        elif self.test_state_var.get() == 'camera_recognition':
            print(1)
            print(self.choose_path_widgets)
            self.destroy_choose_image_path_ui()

            # self.show_image(self.test_image_path, size=(500, 500), x=500, y=40)

# verification, search待实现
        self.insert_all_test_parameters()

    def create_choose_image_path_ui(self):
        self.choose_path_widgets = []
        self.choose_path_widgets.append(
            Label(self.root, text='path of the image', font=('Times New Roman', 12), fg='blue'))
        self.choose_path_widgets[-1].place(x=10, y=55)

        self.choose_path_widgets.append(
            Button(self.root, text='Choose', font=('Times New Roman', 12), command=self.choose_file))
        self.choose_path_widgets[-1].place(x=400, y=51)

        self.choose_path_widgets.append(
            Entry(self.root, width=56, textvariable=self.image_path_var, font=('Times New Roman', 12)))
        self.choose_path_widgets[-1].place(x=10, y=85)

    def destroy_choose_image_path_ui(self):
        for widget in self.choose_path_widgets:
            widget.destroy()


    def choose_state_identify(self):
        self.identification_state = self.identification_state_var.get()


    def choose_file(self):
        temp_path = askopenfilename()
        if temp_path is not None and temp_path != '':
            if temp_path[-4:] in ['.jpg', '.JPG', '.PNG', '.png']:
                self.test_image_path = temp_path
                self.image_path_var.set(self.test_image_path)
                if self.test_image_path !='':
                    self.display = []

                    if self.test_state_var.get() == 'recognition':
                        self.show_image(self.test_image_path, size=(500, 500), x=500, y=40)
                    else:
                        self.show_image(self.test_image_path, size=(500, 500), x=500, y=40)
                self.insert_all_test_parameters()   # 所有参数（路径、模式等）
            else:
                mb.showerror('Error', 'Please choose an image file!')

    def choose_folder(self):
        temp_path = askdirectory()
        if temp_path is not None and temp_path != '':
            self.test_folder_path = temp_path
            self.image_folder_path_var.set(self.test_folder_path)

            self.insert_all_test_parameters()

# 存放在listbox中的所有参数，更清晰地地体现各种图片的信息
    def insert_all_test_parameters(self):

        self.test_parameters.delete(0, END)

        self.test_parameters.insert(0, 'Prediction parameters are as follows:')
        self.test_parameters.itemconfig(0, fg='red')
        self.test_parameters.insert(1, '')

        self.test_parameters.insert(2, 'Image path:')
        self.test_parameters.itemconfig(2, fg='blue')
        self.test_parameters.insert(3, '{}'.format(self.test_image_path))

        self.test_parameters.insert(4, 'Mode: ')
        self.test_parameters.itemconfig(4, fg='blue')

        self.test_parameters.insert(5, '{}'.format(self.test_state))

        self.test_parameters.insert(6, 'database path:')
        self.test_parameters.itemconfig(6, fg='blue')
        self.test_parameters.insert(7, '{}'.format(self.test_folder_path))
        # self.test_parameters.insert(6, 'Image size:')
        # self.test_parameters.itemconfig(6, fg='blue')
        # self.test_parameters.insert(7, '{}'.format(self.image_size))

        # self.test_parameters.insert(8, 'Use model that trained by all data:')
        # self.test_parameters.itemconfig(8, fg='blue')
        # self.test_parameters.insert(9, '{}'.format(self.fit_all_data))

        self.test_parameters.insert(8, '')

        self.test_parameters.insert(9, 'Please check the model\'s parameters!')
        self.test_parameters.insert(10, 'If the parameters are correct, click the \'Start\' button!')
        self.test_parameters.itemconfig(9, fg='red')
        self.test_parameters.itemconfig(10, fg='red')


    def show_image(self, image_path, size, x, y):
        image = Image.open(image_path)
        image = image.resize(size)
        self.display.append(ImageTk.PhotoImage(image))
        Label(self.root, image=self.display[-1]).place(x=x, y=y)

    def destroy_current_ui(self):
        for widget in self.root.winfo_children():
            if widget is not self.menuBar:
                # print(widget)
                widget.destroy()


    def on_exit(self):
        if mb.askyesno("Exit", 'Are you sure to exit?'):
            self.root.destroy()


    def choose_image_size(self, image_size):
        self.image_size = image_size
        # if self.enable_train:
        #     self.insert_all_train_parameters()
        # else:
        self.insert_all_test_parameters()

    def start_test(self):
        if self.check_error():
            if mb.askyesno("Predict", 'Do you want to start?'):
                self.answer_box.delete(0, END)
                if self.test_state == "recognition":
                    self.answer = test_images.recognition(self.test_image_path, self.test_folder_path,
                                                          threshold=0.5, answer_pic=True)
                elif self.test_state == "camera recognition":
                    self.answer = test_images.camera_recognition(self.test_folder_path)
# verification 待实现
                self.answer_box.insert(0, self.answer)

    def start_identify(self):
        if self.identification_state == "eye identification":
            if mb.askyesno("Identification", 'Do you want to use eye identification?'):
                self.identification_answer = identification.identify(self.identification_state)
                print(self.identification_answer)
                self.identification_answer_box.insert(0, self.identification_answer)
        elif self.identification_state == "smile identification":
            if mb.askyesno("Identification", 'Do you want to use smile identification?'):
                self.identification_answer = identification.identify(self.identification_state)
                print(self.identification_answer)
                self.identification_answer_box.insert(0, self.identification_answer)

    def check_error(self):
        if self.test_state == "recognition":
            if self.test_image_path is None or self.test_image_path == '' or self.test_folder_path is None:
                mb.showerror("Error", 'The path is invalid!')
                return False
        elif self.test_state == "camera recognition":
            if self.test_folder_path is None:
                mb.showerror("Error", "No folder path")
                return False
        return True



def main():
    FaceRecognition()


if __name__ == '__main__':
    main()
