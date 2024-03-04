import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QVBoxLayout, QSizePolicy, QPushButton, QDialog, QHBoxLayout, QLineEdit, QTextEdit, QScrollArea, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from animeinfos import get_animeinfo_by_title, get_cover_path_by_anime_title, delete_animeinfo_by_title, add_animeinfo_by_title_cover


class DetailedInfoDialog(QDialog):
    def __init__(self, main_window, info = None):
        super().__init__()

        self.setWindowTitle('Custom Dialog')
        self.setGeometry(100, 100, 800, 400)

        self.layout = QVBoxLayout()

        # Buttons row
        btn_layout = QHBoxLayout()
        save_btn = QPushButton('保存')
        load_btn = QPushButton('导入')
        delete_btn = QPushButton('删除本配置并返回')
        back_btn = QPushButton('返回')
        save_btn.clicked.connect(lambda: self.save_btn_clicked(main_window))
        delete_btn.clicked.connect(lambda: self.delete_btn_clicked(main_window,self.title_edit.text()))
        back_btn.clicked.connect(self.accept)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(load_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(back_btn)
        self.layout.addLayout(btn_layout)

        # title_layout
        title_layout = QHBoxLayout()
        title_label = QLabel('title :')
        self.title_edit = QLineEdit()
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_edit)
        self.layout.addLayout(title_layout)

        # cover_layout row
        cover_layout = QHBoxLayout()
        cover_label = QLabel('cover :')
        self.cover_path_label = QLabel('')
        cover_button = QPushButton('选择')
        cover_button.clicked.connect(lambda: self.select_cover(self.cover_path_label))
        cover_layout.addWidget(cover_label)
        cover_layout.addWidget(self.cover_path_label)
        cover_layout.addWidget(cover_button)
        self.layout.addLayout(cover_layout)

        # Scroll area
        scroll = QScrollArea()
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        self.layout.addWidget(scroll)

        self.original_title = ''
        # Add initial row to scroll area
        if info:
            title = info['title']
            self.original_title = title
            self.title_edit.setText(title)
            cover = get_cover_path_by_anime_title(title)
            self.cover_path_label.setText(cover)
            episode_list = info['episode_list']
            for episode in episode_list:
                self.addScrollRow(self.scroll_layout,episode['episode_title'],episode['episode_path_textbox'])


        self.addScrollRow(self.scroll_layout)


        self.setLayout(self.layout)

        back_btn.clicked.connect(lambda: self.back_btn_clicked(main_window))

    def back_btn_clicked(self,main_window):
        self.accept()
        main_window.createGrid()

    # 打开文件夹添加章节
    def select_cover(self, cover_path_label):        
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, '选择文件', '', "All Files (*);;Python Files (*.py)")
        
      
        if file_path:
            cover_path_label.setText(file_path)

    # 打开文件夹添加章节
    def openFileNameDialog(self, layout, new_episode_path_label):        
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, '选择文件', '', "All Files (*);;Python Files (*.py)")
        
      
        if file_path:
            new_episode_path_label.setText(file_path)
            self.addScrollRow(layout)


    def check_info_valued(self):
        if not self.title_edit.text():
            return False
        if not self.cover_path_label.text():
            return False
        return True
    def delete_btn_clicked(self, main_window, title):
        # print(title)
        delete_animeinfo_by_title(title)
        self.back_btn_clicked(main_window)
        

    def save_btn_clicked(self,main_window):
        
        title = self.title_edit.text()
        
        cover = self.cover_path_label.text()
        if not self.check_info_valued():
            self.back_btn_clicked(main_window)

        episode_list = []
        for i in range (self.scroll_layout.count()):
            # print(f'{i}---')
            row_layout = self.scroll_layout.itemAt(i)
            episode_title = row_layout.itemAt(0).widget()
            episode_path_label = row_layout.itemAt(1).widget()
            if not episode_title.text():
                continue
            if not episode_path_label.text():
                continue
            episode_list.append(  {
                "episode_title": episode_title.text(),
                "episode_path_textbox": episode_path_label.text()
             })
            # print(f'{i}---')

        info = {
            'title': title,
            'episode_list': episode_list
        }
        if self.original_title or self.original_title == title:
            delete_animeinfo_by_title(self.original_title)
        msg = add_animeinfo_by_title_cover(title, cover, info)
        # print(msg)
      
        self.back_btn_clicked(main_window)

    def addScrollRow(self, layout, episode_title = '', episode_path = ''):
        new_row_layout = QHBoxLayout()
        new_episode_title_eidit = QLineEdit()
        new_episode_title_eidit.setFixedWidth(100)
        new_episode_title_eidit.setText(episode_title)
        new_episode_path_label = QLabel()
        new_episode_path_label.setFixedWidth(300)
        new_episode_path_label.setText(episode_path)
        new_add_button = QPushButton('选择')
        new_del_button = QPushButton('删除本行')
        new_add_button.clicked.connect(lambda: self.openFileNameDialog(layout, new_episode_path_label))
        new_del_button.clicked.connect(lambda: self.delScrollRow(layout, new_row_layout))
        new_row_layout.addWidget(new_episode_title_eidit)
        new_row_layout.addWidget(new_episode_path_label)
        new_row_layout.addWidget(new_add_button)
        new_row_layout.addWidget(new_del_button)
        layout.addLayout(new_row_layout)

    

    def delScrollRow(self, layout, row_layout=None):
        if layout.count() > 1:
            if row_layout:
                while row_layout.count():
                    item = row_layout.takeAt(0)
                    widget = item.widget()
                    layout.removeItem(row_layout)
                    if widget:
                        widget.deleteLater()