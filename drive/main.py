import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import glob

from drive.drive_utils import *
from drive.main_utils import *

import shutil
MAIN_PATH = os.getcwd()
class NewDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.main()
   
    
    def main(self):
        main_layout = QHBoxLayout()
        layout = QVBoxLayout()
        layout2 = QVBoxLayout()

        button1 = QPushButton('Dowload')
        button2 = QPushButton('hey')

        button1.clicked.connect(self.download_button)
        button2.clicked.connect(self.upload_button)

        self.baslangic()

        self.Upload()
        self.Download()

        layout.addWidget(self.tree_upload)
        layout2.addWidget(self.tree_dowload)

        layout.addWidget(button1)
        layout2.addWidget(button2)

        check_layout = QVBoxLayout()

        self.checkBox()
        for i in self.check_name_list.values():
            check_layout.addWidget(i)

        main_layout.addLayout(check_layout)
        main_layout.addLayout(layout)
        main_layout.addLayout(layout2)
        self.setLayout(main_layout)
        self.resize(800,500)
        self.show()

    def baslangic(self):
        pass


    def Upload(self):
        self.upload_images_items = dict()
        self.upload_masks_items = dict()

        self.tree_upload = QTreeWidget(self)
        self.tree_upload.setGeometry(20,20,300,450)
        self.tree_upload.setHeaderLabel("Header")

        self.upload_item1 = QTreeWidgetItem()
        self.upload_item1.setText(0,"Images")
        self.upload_item2 = QTreeWidgetItem()
        self.upload_item2.setText(0,"Mask")
        self.tree_upload.addTopLevelItems([self.upload_item1,self.upload_item2])

        self.upload_item1.addChildren(self.upload_images_items.values())
        self.upload_item2.addChildren(self.upload_masks_items.values())

        self.tree_upload.setColumnCount(3)
        self.tree_upload.setHeaderLabels(["Klasör/Dosya","Etiketleyen","Yüklenme Durumu"])


    def Download(self):
        self.dowload_images_items = dict()
        self.dowload_masks_items = dict()

        self.tree_dowload = QTreeWidget(self)
        self.tree_dowload.setGeometry(20,20,300,450)
        self.tree_dowload.setHeaderLabel("Header")
        
        self.dowload_item1 = QTreeWidgetItem()
        self.dowload_item1.setText(0,"Images")
        self.dowload_item2 = QTreeWidgetItem()
        self.dowload_item2.setText(0,"Mask")
        self.tree_dowload.addTopLevelItems([self.dowload_item1,self.dowload_item2])

        self.dowload_item1.addChildren(self.dowload_images_items.values())
        self.dowload_item2.addChildren(self.dowload_masks_items.values())

        self.tree_dowload.setColumnCount(3)
        self.tree_dowload.setHeaderLabels(["Klasör/Dosya","Etiketleyen","Güncelleme Durumu"])

    def checkBox(self):
        with open("name.txt","r") as f:
            names = f.read()
        names = names.split("\n")
        self.check_name_list = {}
        calisma = 0
        for i in total_folder_read():
            check = QCheckBox(i)
            if i in names:
                calisma = 1
                check.setChecked(True)
            check.toggled.connect(self.check)
            self.check_name_list[i] = check
        
        if calisma:
            self.check(par=1)

    def upload_button(self):  
         
        for USER_ID in self.check_names:
            
            images_df,mask_df,images_id_ex,masks_id_ex = folder_read(USER_ID)
            image_id_data, mask_id_data = data_drive_read(USER_ID)  
            no_images = []
            yes_images = []
            drive_delete(USER_ID)
            for key in list(self.dowload_images_items.keys()):
                if (self.dowload_images_items[key].text(1) == USER_ID) & (self.dowload_images_items[key].text(2) == "Güncel Değil!"):
                    no_images.append(key)
                elif (self.dowload_images_items[key].text(1) == USER_ID) & (self.dowload_images_items[key].text(2) == "Güncel"):
                    yes_images.append(key)

            if len(no_images)>0:
                images_id = images_df[images_df["name"].isin(list(no_images))]["id"].to_list()
                images_name = images_df[images_df["name"].isin(list(no_images))]["name"].to_list()
                image_mime_type = ["image/jpeg" for typ in range(len(no_images))]

                folder_upload(images_name,image_mime_type,"images",images_id_ex,UserId=USER_ID)

                # folder_update(images_name,image_mime_type,images_id,"images",images_df,UserId=USER_ID)
                upload_time_update(no_images,"images",USER_ID)
                for path in no_images:
                    self.dowload_images_items[path].setText(2,"Güncel")
            
            if len(yes_images)>0:
                print(yes_images)
                images_name = images_df[images_df["name"].isin(list(yes_images))]["name"].to_list()
                image_mime_type = ["image/jpeg" for typ in range(len(yes_images))]

                data_drive_upload(images_name,image_mime_type,"images",image_id_data,UserId=USER_ID)
            
            no_masks = []
            yes_masks = []
            for key in list(self.dowload_masks_items.keys()):
                if (self.dowload_masks_items[key].text(1) == USER_ID) & (self.dowload_masks_items[key].text(2) == "Güncel Değil!"):
                    no_masks.append(key)
                elif (self.dowload_masks_items[key].text(1) == USER_ID) & (self.dowload_masks_items[key].text(2) == "Güncel"):
                    yes_masks.append(key)
            if len(no_masks)>0:
                masks_id = mask_df[mask_df["name"].isin(list(no_masks))]["id"].to_list()
                masks_name = mask_df[mask_df["name"].isin(list(no_masks))]["name"].to_list()
                masks_mime_type =  ["text/plain" for typ in range(len(no_masks))]
                folder_upload(masks_name,masks_mime_type,"mask",masks_id_ex,UserId=USER_ID)

                # folder_update(masks_name,image_mime_type,masks_id,"mask",mask_df,UserId=USER_ID)
                upload_time_update(no_masks,"mask",USER_ID)
                for path in no_masks:
                    self.dowload_masks_items[path].setText(2,"Güncel")
            
            if len(yes_masks)>0:
                print(yes_masks)
                images_name = images_df[images_df["name"].isin(list(yes_masks))]["name"].to_list()
                image_mime_type = ["text/plain" for typ in range(len(yes_masks))]

                  
                data_drive_upload(images_name,image_mime_type,"mask",mask_id_data,UserId=USER_ID)

    def download_button(self):
        no_images_dict,no_masks_dict = self.yes_no
        for USER_ID in list(no_images_dict.keys()):
            no_images = no_images_dict[USER_ID]
            if len(no_images[0])>0:
                folder_dowload(no_images[1],no_images[2],"images",USER_ID)

        for USER_ID in list(no_masks_dict.keys()):
            no_masks = no_masks_dict[USER_ID]
            if len(no_masks[0])>0:
                folder_dowload(no_masks[1],no_masks[2],"mask",USER_ID)
            
            json_re(no_masks[0],USER_ID)

        for path in no_images[0]:
            self.upload_images_items[path].setText(2,"Yüklendi")

        for path in no_masks[0]:
            self.upload_masks_items[path].setText(2,"Yüklendi")

        while self.dowload_item1.childCount() > 0:
            self.dowload_item1.takeChild(0)
        while self.dowload_item2.childCount() > 0:
            self.dowload_item2.takeChild(0)

        self.dowload_images_items = dict()
        self.dowload_masks_items = dict()
        
        self.dowload_images_items,self.dowload_masks_items = local_folder_read(self.check_names)
        
        self.dowload_item1.addChildren(self.dowload_images_items.values())
        self.dowload_item2.addChildren(self.dowload_masks_items.values())


        # print(self.dowload_masks_items)
    
    def check(self,par):
        self.check_names = []
        while self.upload_item1.childCount() > 0:
            self.upload_item1.takeChild(0)
        while self.upload_item2.childCount() > 0:
            self.upload_item2.takeChild(0)

        self.upload_images_items = dict()
        self.upload_masks_items = dict()

        for i in list(self.check_name_list.keys()):
            if self.check_name_list[i].isChecked():
                self.check_names.append(i)
        self.upload_images_items,self.upload_masks_items,self.yes_no = drive_folder_read(self.check_names) 

        self.upload_item1.addChildren(self.upload_images_items.values())
        self.upload_item2.addChildren(self.upload_masks_items.values())


        while self.dowload_item1.childCount() > 0:
            self.dowload_item1.takeChild(0)
        while self.dowload_item2.childCount() > 0:
            self.dowload_item2.takeChild(0)

        self.dowload_images_items = dict()
        self.dowload_masks_items = dict()
        
        self.dowload_images_items,self.dowload_masks_items = local_folder_read(self.check_names)
        
        self.dowload_item1.addChildren(self.dowload_images_items.values())
        self.dowload_item2.addChildren(self.dowload_masks_items.values())

        string = ""
        for names in self.check_names:
            string += str(names)
            string += "\n"
        with open("name.txt","w") as f:
            f.write(string)
        f.close()





if __name__ == "__main__":
    app = QApplication([])
    window = NewDialog()
    app.exec()

    


    
