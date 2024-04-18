from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QFileDialog




class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("大容量图像隐写系统")
        self.setGeometry(100, 100, 1000, 500)

        self.title_label = QLabel("大容量图像隐写系统", self)
        self.title_label.setGeometry(280, 80, 500, 200)
        self.title_label.setAlignment(Qt.AlignCenter)
        font = self.title_label.font()
        font.setPointSize(38)  # 调整字体大小
        self.title_label.setFont(font)
        self.title_label.setFixedWidth(400)  # 设置标签的固定宽度


        # 设置标题样式
        title_style = """
            QLabel {
                font-size: 34px;
                font-weight: bold;
                text-align: center;
            }
        """
        self.title_label.setStyleSheet(title_style)

        self.enter_system_button = QPushButton("进入系统", self)
        self.enter_system_button.setGeometry(400, 300, 150, 40)
        self.enter_system_button.clicked.connect(self.enter_system)

    def enter_system(self):
        self.hide()
        self.main_window = MainWindow()
        self.main_window.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("大容量图像隐写")
        self.setGeometry(100, 100, 1000, 500)

        self.stego_method_label = QLabel("隐写术：", self)
        self.stego_method_label.move(30, 50)
        self.stego_method_label.setFixedWidth(80)
        self.stego_method_combobox = QComboBox(self)
        self.stego_method_combobox.addItems(["Basic",  "Residual", "Dense"])
        self.stego_method_combobox.move(200, 50)
        self.stego_method_combobox.setFixedWidth(200)

        self.embed_rate_label = QLabel("嵌入率(bpp)：", self)
        self.embed_rate_label.move(30, 150)
        self.embed_rate_label.setFixedWidth(150)
        self.embed_rate_combobox = QComboBox(self)
        self.embed_rate_combobox.addItems(["1", "2", "3"])
        self.embed_rate_combobox.move(200, 150)
        self.embed_rate_combobox.setFixedWidth(200)

        self.choose_image_button = QPushButton("选择嵌入图像", self)
        self.choose_image_button.move(200, 250)
        self.choose_image_button.setFixedWidth(200)
        self.choose_image_button.clicked.connect(self.choose_image)

        self.start_embedding_button = QPushButton("开始隐写", self)
        self.start_embedding_button.move(200, 350)
        self.start_embedding_button.setFixedWidth(200)
        self.start_embedding_button.clicked.connect(self.start_embedding)

        self.image_label = QLabel(self)
        self.image_label.setGeometry(400, 0, 500, 400)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.steganogan = None
        self.input_image_path = ""

    def choose_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "选择嵌入图像")
        if image_path:
            self.input_image_path = image_path
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap)

    def start_embedding(self):
        stego_method = self.stego_method_combobox.currentText()
        embed_rate = self.embed_rate_combobox.currentText()

        # 根据隐写术和嵌入率组合选择对应的模型
        model_path = f"model/{stego_method.lower()}_{embed_rate.lower()}.steg"

        # 载入SteganoGAN模型
        self.steganogan = SteganoGAN.load(path=model_path, cuda=True, verbose=True)

        output_image_path = 'output.png'
        if output_image_path:
            # 进行图像隐写并获取性能指标
            metrics = self.steganogan.evaluate_image(self.input_image_path, output_image_path)

            # 创建并显示ResultWindow
            result_window = ResultWindow(self, self.input_image_path, output_image_path, metrics)
            result_window.show()

class ResultWindow(QMainWindow):
    def __init__(self, parent, image_path, embedded_image_path, metrics):
        super().__init__(parent)
        self.setWindowTitle("隐写结果")
        self.setGeometry(100, 100, 1000, 500)

        self.original_image_label = QLabel("载体图像", self)
        self.original_image_label.move(50, 50)
        self.original_image = QLabel(self)
        self.original_image.setPixmap(QPixmap(image_path))
        self.original_image.setScaledContents(True)
        self.original_image.setGeometry(50, 80, 200, 200)

        self.embedded_image_label = QLabel("隐写图像", self)
        self.embedded_image_label.move(350, 50)
        self.embedded_image = QLabel(self)
        self.embedded_image.setPixmap(QPixmap(embedded_image_path))
        self.embedded_image.setScaledContents(True)
        self.embedded_image.setGeometry(350, 80, 200, 200)

        self.metrics_label = QLabel("性能指标", self)
        self.metrics_label.move(50, 330)

        y_pos = 360
        for key, value in metrics.items():
            label_text = f"{key}: {value}"
            metric_label = QLabel(label_text, self)
            metric_label.move(50, y_pos)
            metric_label.setFixedWidth(500)
            y_pos += 30

if __name__ == "__main__":
    app = QApplication([])
    main_screen = MainScreen()
    main_screen.show()
    app.exec_()

