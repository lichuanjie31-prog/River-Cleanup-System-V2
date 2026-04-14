import sys
import cv2
import time
import numpy as np
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from ultralytics import YOLO

# --- 资源路径定位函数（打包核心） ---
def resource_path(relative_path):
    """ 获取程序运行时的资源绝对路径，兼容脚本与 PyInstaller 打包后的环境 """
    if hasattr(sys, '_MEIPASS'):
        # 打包后的路径：PyInstaller 会将文件解压到 sys._MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    # 开发环境路径：当前脚本所在目录
    return os.path.join(os.path.abspath("."), relative_path)

class RiverMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.cap = None
        self.timer = QTimer()
        self.data_points = [0] * 20
        self.has_model = False
        
        # --- 模型加载逻辑 ---
        # 对应打包命令中的 --add-data "xxx/best.pt;weights"
        model_path = resource_path(os.path.join("weights", "best.pt"))
        
        # 容错：如果 weights 文件夹没找着，尝试根目录
        if not os.path.exists(model_path):
            model_path = resource_path("best.pt")

        try:
            self.model = YOLO(model_path)
            self.has_model = True
            print(f">>> 成功加载 V2.0 精度增强模型: {model_path}")
        except Exception as e:
            print(f">>> 模型加载失败: {e}")
            self.has_model = False

        self.initUI()

    def initUI(self):
        self.setWindowTitle('常州大学 - 水面垃圾批处理分析系统 (AI V2.0 实战版)')
        self.setFixedSize(1150, 720) 
        self.setStyleSheet("background-color: #1e272e; color: white;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 15, 20, 15)

        # 1. Header
        header = QHBoxLayout()
        self.logo = QLabel()
        # 同样使用 resource_path 加载 logo 图标
        logo_path = resource_path('cczu_logo.png')
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path).scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio)
            self.logo.setPixmap(pix)
        
        header.addWidget(self.logo)
        
        self.title = QLabel('智慧河道：数据处理分析中心 (V2.0)')
        self.title.setStyleSheet("font-size: 26px; font-weight: bold; color: #3498db; margin-left: 15px;")
        header.addWidget(self.title, stretch=1)
        main_layout.addLayout(header)

        # 2. Body
        body = QHBoxLayout()
        self.preview_label = QLabel("等待任务启动...\n(V2.0 已优化反光与遮挡识别)")
        self.preview_label.setStyleSheet("border: 3px solid #3498db; border-radius: 15px; background: black; color: #555;")
        self.preview_label.setFixedSize(600, 400)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        body.addWidget(self.preview_label)

        chart_vbox = QVBoxLayout()
        self.fig, self.ax = plt.subplots(figsize=(3, 3))
        self.fig.patch.set_facecolor('#1e272e')
        self.ax.set_facecolor('#1e272e')
        self.ax.tick_params(colors='white', labelsize=8)
        self.canvas = FigureCanvas(self.fig)
        chart_vbox.addWidget(QLabel("实时垃圾数量波动", alignment=Qt.AlignmentFlag.AlignCenter))
        chart_vbox.addWidget(self.canvas)
        body.addLayout(chart_vbox)
        main_layout.addLayout(body)

        # 3. 日志区
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("background: #0c1117; color: #1dd1a1; font-family: 'Consolas'; border: 1px solid #3498db; padding: 10px;")
        self.console.setFixedHeight(100)
        main_layout.addWidget(self.console)

        # 4. 功能按键区
        btns = QHBoxLayout()
        btn_style = "QPushButton{background:%s; color:white; border-radius:8px; padding:12px; font-weight:bold; font-size:14px;}"
        self.btn_cam = QPushButton("模式A：开启实时监控")
        self.btn_cam.setStyleSheet(btn_style % "#3498db")
        self.btn_batch = QPushButton("模式B：批量分析文件夹")
        self.btn_batch.setStyleSheet(btn_style % "#9b59b6")
        self.btn_stop = QPushButton("停止任务")
        self.btn_stop.setStyleSheet(btn_style % "#e74c3c")

        btns.addWidget(self.btn_cam); btns.addWidget(self.btn_batch); btns.addWidget(self.btn_stop)
        main_layout.addLayout(btns)

        # 事件绑定
        self.btn_cam.clicked.connect(self.start_camera)
        self.btn_batch.clicked.connect(self.start_batch)
        self.btn_stop.clicked.connect(self.stop_all)
        self.timer.timeout.connect(self.update_frame)
        self.setLayout(main_layout)

    def start_camera(self):
        if not self.has_model:
            QMessageBox.critical(self, "错误", "未找到 V2.0 模型文件，无法启动！")
            return
        self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened():
            self.timer.start(30)
            self.console.append(f">>> [{time.strftime('%H:%M:%S')}] 切换至实时监控模式 (RTX 5060 加速中)...")
        else:
            self.console.append(">>> [ERROR] 无法启动摄像头")

    def start_batch(self):
        if not self.has_model:
            QMessageBox.critical(self, "错误", "未加载 best.pt 模型！")
            return
        folder_path = QFileDialog.getExistingDirectory(self, "选择包含水面垃圾图片的文件夹")
        if not folder_path: return
        
        output_path = os.path.join(folder_path, "Results_Output_V2")
        if not os.path.exists(output_path): os.makedirs(output_path)
        
        self.console.append(f">>> [BATCH] 开始分析: {folder_path}")
        files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        
        for filename in files:
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path)
            if img is None: continue
            
            # 使用 V2.0 模型推理
            results = self.model.predict(img, conf=0.5, verbose=False)
            count = len(results[0].boxes)
            annotated_img = results[0].plot()
            
            cv2.imwrite(os.path.join(output_path, filename), annotated_img)
            
            h, w, _ = annotated_img.shape
            q_img = QImage(cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB).data, w, h, w*3, QImage.Format.Format_RGB888)
            self.preview_label.setPixmap(QPixmap.fromImage(q_img).scaled(600, 400, Qt.AspectRatioMode.KeepAspectRatio))
            self.console.append(f"-> {filename} | 识别数量: {count} | 状态: OK")
            QApplication.processEvents()
            
        QMessageBox.information(self, "完成", f"V2.0 批量分析结束，结果已存至 Results_Output_V2")

    def stop_all(self):
        if self.cap: self.cap.release()
        self.timer.stop()
        self.preview_label.clear()
        self.preview_label.setText("任务已停止\n常州大学软件工程项目组")

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret and self.has_model:
            results = self.model.predict(frame, conf=0.3, verbose=False)
            count = len(results[0].boxes)
            display_f = results[0].plot()
            
            rgb = cv2.cvtColor(display_f, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            img = QImage(rgb.data, w, h, w*ch, QImage.Format.Format_RGB888)
            
            self.preview_label.setPixmap(QPixmap.fromImage(img).scaled(600, 400, Qt.AspectRatioMode.KeepAspectRatio))
            
            # 更新实时图表
            self.data_points.append(count)
            self.data_points.pop(0)
            self.ax.clear()
            self.ax.plot(self.data_points, color='#3498db', linewidth=2)
            self.ax.set_ylim(0, 15)
            self.ax.set_title("实时垃圾统计", color='white')
            self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RiverMonitor()
    win.show()
    sys.exit(app.exec())