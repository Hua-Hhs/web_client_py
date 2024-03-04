import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QVBoxLayout, QSizePolicy, QPushButton, QDialog, QHBoxLayout, QLineEdit, QTextEdit, QScrollArea, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from animeinfos import get_animeinfo_by_title, get_all_infos_list
from detailed_Info_Dialog import DetailedInfoDialog

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        with open('animeinfos/all_infos.json', 'r') as file:
            data = json.load(file)
        data = data['all_info_list']
        self.data = data
        self.current_page = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Grid')
        self.setGeometry(100, 100, 800, 800)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        

        self.createGrid()

        self.show()

    def createGrid(self):
        # data = []
        # with open('animeinfos/all_infos.json', 'r') as file:
        #     data = json.load(file)
        # data = data['all_info_list']
        self.data = get_all_infos_list()

        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().deleteLater()

        start_index = self.current_page * 16
        end_index = min(start_index + 16, len(self.data))

        row = 0
        col = 0
        for item in self.data[start_index:end_index]:
            # Load image
            pixmap = QPixmap(item["cover"])
            if not pixmap.isNull():
                # Resize image
                pixmap = pixmap.scaledToHeight(150)
                # Create label with image
                label = QLabel(self)
                label.setPixmap(pixmap)
                label.setAlignment(Qt.AlignCenter)
                label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                # Connect label clicked event
                label.mousePressEvent = lambda event, name=item["anime_title"]: self.onLabelClicked(name)
                self.layout.addWidget(label, row, col)

                # Create label with image name
                name_label = QLabel(item["anime_title"], self)
                name_label.setAlignment(Qt.AlignCenter)
                self.layout.addWidget(name_label, row + 1, col)

                col += 1
                if col >= 4:
                    col = 0
                    row += 2
            

        # if len(self.data) > 16:
        self.createNavigationButtons()
        
    def createNavigationButtons(self):
        next_button = QPushButton("Next")
        prev_button = QPushButton("Previous")
        add_button = QPushButton("Add")

        next_button.clicked.connect(self.onNextClicked)
        prev_button.clicked.connect(self.on_prev_clicked)
        add_button.clicked.connect(self.on_add_clicked)

        self.layout.addWidget(prev_button, 8, 1, 1, 1)
        self.layout.addWidget(next_button, 8, 2, 1, 1)
        self.layout.addWidget(add_button, 8, 3, 1, 1)

        self.page_label = QLabel()
        self.reflesh_page_label()
        self.layout.addWidget(self.page_label, 8, 0, 1, 1)


    # 向后翻页
    def onNextClicked(self):
        remain = len(self.data)%16
        if remain > 0:
            max_page = len(self.data)/16+1
        else:
            max_page = len(self.data)/16
        max_page = int(max_page)

        if self.current_page + 1 >= max_page:
            return
        self.current_page += 1
        
        self.createGrid()
    # 向前翻页
    def on_prev_clicked(self):
        if self.current_page-1<0:
            return
        self.current_page -= 1  
        self.createGrid()
        self.reflesh_page_label()

    def reflesh_page_label(self,):
        remain = len(self.data)%16
        if remain > 0:
            max_page = len(self.data)/16+1
        else:
            max_page = len(self.data)/16
        max_page = int(max_page)
        self.page_label.setText(f"Page {self.current_page + 1}/{max_page}")
        pass

    def on_add_clicked(self):
        dialog = DetailedInfoDialog(self)
        dialog.exec_()

    def onLabelClicked(self, title):
        info = get_animeinfo_by_title(title)
        # print(info)
        dialog = DetailedInfoDialog(self,info)
        dialog.exec_()




if __name__ == '__main__': 

    app = QApplication(sys.argv)
    grid = MainWindow()
    sys.exit(app.exec_())
