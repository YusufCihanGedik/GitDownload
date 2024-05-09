import os
import glob
import json
import datetime

from PyQt5.QtWidgets import QTreeWidgetItem

import sys
from drive.drive_utils import *

def drive_folder_read(UserIds):
    def append(images_items,images,typ,UserId):
        for i in images:
            item = QTreeWidgetItem()
            name = i.split("\\")[-1][:-4]
            item.setText(0,name)
            item.setText(1,UserId)
            item.setText(2,typ)
            images_items[i.split("\\")[-1]] = item
        return images_items
    
    images_names,mask_names = [],[]
    images_items,masks_items = {},{}
    no_images_dict,no_masks_dict = {},{}
    for UserId in UserIds:
        images_df,masks_df,image_id,mask_id = folder_read(UserId)

        
        if len(images_df)>0:
            images_names = images_df["name"].to_list()
        else:
            images_names =  []
        
        if len(masks_df)>0:
            mask_names = masks_df["name"].to_list()
        else:
            mask_names = []

        
        no_images,yes_images,no_masks,yes_masks = drive_folder_control(UserId,images_names,mask_names)

        if len(images_df)>0:
            images_id = images_df[images_df["name"].isin(list(no_images))]["id"].to_list()
            images_name = images_df[images_df["name"].isin(list(no_images))]["name"].to_list()
        else:
            images_id,images_name =  [],[]
        
        if len(masks_df) > 0:
            masks_id = masks_df[masks_df["name"].isin(list(no_masks))]["id"].to_list()
            masks_name = masks_df[masks_df["name"].isin(list(no_masks))]["name"].to_list()
        else:
            masks_id,masks_name = [],[]
        
        

        no_images_dict[UserId] = [no_images,images_id,images_name]
        no_masks_dict[UserId] = [no_masks,masks_id,masks_name]

        images_items = append(images_items,no_images,"Yüklenmedi",UserId)
        images_items = append(images_items,yes_images,"Yüklendi",UserId)


        masks_items = append(masks_items,no_masks,"Yüklenmedi",UserId)
        masks_items = append(masks_items,yes_masks,"Yüklendi",UserId)

    return images_items,masks_items,[no_images_dict,no_masks_dict]


def drive_folder_control(UserId,drive_images,drive_masks):
    if len(glob.glob(f"drive/Dowload/{UserId}"))<1:
        os.mkdir(f"drive/Dowload/{UserId}")
        os.mkdir(f"drive/Dowload/{UserId}/images")
        os.mkdir(f"drive/Dowload/{UserId}/mask")

    images = glob.glob(f"drive/Dowload/{UserId}/images/**")
    masks = glob.glob(f"drive/Dowload/{UserId}/mask/**")

    images = [i.split("\\")[-1] for i in images]
    set2 = set(drive_images)
    set1 = set(images)
    yes_images = list(set(drive_images) & set(images))
    no_images = set2 - set1
    masks = [i.split("\\")[-1] for i in masks]
    set2 = set(drive_masks)
    set1 = set(masks)
    yes_masks = list(set(drive_masks) & set(masks))
    no_masks = set2 - set1

    return no_images,yes_images,no_masks,yes_masks

def read_time(path):
    modification_time = os.path.getmtime(path)
    modification_datetime = datetime.datetime.fromtimestamp(modification_time)
    formatted_time = modification_datetime.strftime("%d/%m/%Y %H:%M:%S")
    return formatted_time

# def upload_time_control(path,path_type,UserId):
#     if path_type == "images":
#         path = path[:-4]
#         if len(glob.glob(f"drive/Dowload/{UserId}/mask/{path}.json")) > 0:
#             with open(f"drive/Dowload/{UserId}/mask/{path}.json","r") as file:
#                 data = json.load(file)
#             if "image_text" in list(data.keys()):
#                 if len(data["image_text"])>0:
#                     return 0
#                 else:
#                     return 1
#             else:
#                 return 1
#         else:
#             return 0
        
#     else:
#         with open(f"drive/Dowload/{UserId}/mask/{path}","r") as file:
#             data = json.load(file)
#         if "image_text" in list(data.keys()):
#             if len(data["image_text"])>0:
#                 return 0
#             else:
#                 return 1
#         else:
#             return 1
        
def upload_time_control(path,path_type,UserId):
    if path_type == "images":
        path = path[:-4]
        if len(glob.glob(f"drive/Dowload/{UserId}/mask/{path}.json")) > 0:
            with open(f"drive/Dowload/{UserId}/mask/{path}.json","r") as file:
                data = json.load(file)
            if "image_text" in list(data.keys()):
                if len(data["image_text"])>0:
                    return 0
                else:
                    return 1
            else:
                return 1
        else:
            return 0
        
    else:
        with open(f"drive/Dowload/{UserId}/mask/{path}","r") as file:
            data = json.load(file)
        if "image_text" in list(data.keys()):
            if len(data["image_text"])>0:
                return 0
            else:
                return 1
        else:
            return 1

    # if len(glob.glob(f"Dowload/{UserId}/data.json")) == 0:
    #     return 0
    # json_path = f"Dowload/{UserId}/data.json"
    # with open(json_path,"r") as f:
    #     formatted_dict = json.load(f)

    # if path_type == "images":
    #     formatted_time = read_time(f"Dowload/{UserId}/images/{path}")
    #     if (path in list(formatted_dict[0].keys())):
    #         if formatted_dict[0][path] == formatted_time:
    #             return 1
    #         else:
    #             return 0
    #     else:
    #         return 0
            
    # elif path_type == "mask":
    #     formatted_time = read_time(f"Dowload/{UserId}/mask/{path}")
    #     if (path in list(formatted_dict[1].keys())):
    #         if formatted_dict[1][path] == formatted_time:
    #             return 1
    #         else:
    #             return 0
    #     else:
    #         return 0
    # else:
    #     raise ValueError("Hatali dosya tipi!!!!")
    
def local_folder_read(UserIds):
    images_items = dict()
    masks_items = dict()

    for UserId in UserIds:
        images = glob.glob(f"drive/Dowload/{UserId}/images/**")
        images = [image.split("\\")[-1] for image in images]
        masks = glob.glob(f"drive/Dowload/{UserId}/mask/**")
        masks = [mask.split("\\")[-1] for mask in masks]

        # upload_time_update(images,"images",UserId)
        # upload_time_update(masks,"mask",UserId)

        for image in images:
            item = QTreeWidgetItem()
            name = image.split("\\")[-1][:-4]
            item.setText(0,name)
            item.setText(1,UserId)
            if upload_time_control(image.split("\\")[-1],"images",UserId):
                item.setText(2,"Güncel")
            else:
                item.setText(2,"Güncel Değil!")
            images_items[image.split("\\")[-1]] = item

        for mask in masks:
            item = QTreeWidgetItem()
            name = mask.split("\\")[-1][:-4]
            item.setText(0,name)
            item.setText(1,UserId)
            if upload_time_control(mask.split("\\")[-1],"mask",UserId):
                item.setText(2,"Güncel")
            else:
                item.setText(2,"Güncel Değil!")
            masks_items[mask.split("\\")[-1]] = item

    return images_items,masks_items

# def local_folder_read(UserIds):
#     images_items = dict()
#     masks_items = dict()

#     no_images_dict,no_masks_dict = {},{}
#     for UserId in UserIds:
#         images_df,masks_df,image_id,mask_id = folder_read(UserId)
#         if len(images_df)>0:
#             images_names = images_df["name"].to_list()
#         else:
#             images_names =  []
        
#         if len(masks_df)>0:
#             mask_names = masks_df["name"].to_list()
#         else:
#             mask_names = []

#         no_images,yes_images,no_masks,yes_masks = local_folder_control(UserId,images_names,mask_names)
#         if len(images_df)>0:
#             images_id = images_df[images_df["name"].isin(list(no_images))]["id"].to_list()
#             images_name = images_df[images_df["name"].isin(list(no_images))]["name"].to_list()
#         else:
#             images_id,images_name =  [],[],[]
        
#         if len(masks_df) > 0:
#             masks_id = masks_df[masks_df["name"].isin(list(no_masks))]["id"].to_list()
#             masks_name = masks_df[masks_df["name"].isin(list(no_masks))]["name"].to_list()
#         else:
#             masks_id,masks_name = [],[]


#         no_images_dict[UserId] = [no_images,images_id,images_name]
#         no_masks_dict[UserId] = [no_masks,masks_id,masks_name]

        


#         images = glob.glob(f"Dowload/{UserId}/images/**")
#         masks = glob.glob(f"Dowload/{UserId}/mask/**")

        # for image in images:
        #     item = QTreeWidgetItem()
        #     name = image.split("\\")[-1][:-4]
        #     item.setText(0,name)
        #     item.setText(1,UserId)
        #     if upload_time_control(image,"images",UserId):
        #         item.setText(2,"Güncel")
        #     else:
        #         item.setText(2,"Güncel Değil!")
        #     images_items[image.split("\\")[-1]] = item

        # for mask in masks:
        #     item = QTreeWidgetItem()
        #     name = image.split("\\")[-1][:-4]
        #     item.setText(0,name)
        #     item.setText(1,UserId)
        #     if upload_time_control(mask,"masks",UserId):
        #         item.setText(2,"Güncel")
        #     else:
        #         item.setText(2,"Güncel Değil!")
        #     masks_items[mask.split("\\")[-1]] = item

#     return images_items,masks_items,[no_images_dict,no_masks_dict]

def local_folder_control(UserId,drive_images,drive_masks):
    if len(glob.glob(f"drive/Dowload/{UserId}"))<1:
        os.mkdir(f"drive/Dowload/{UserId}")
        os.mkdir(f"drive/Dowload/{UserId}/images")
        os.mkdir(f"drive/Dowload/{UserId}/mask")

    images = glob.glob(f"drive/Dowload/{UserId}/images/**")
    masks = glob.glob(f"drive/Dowload/{UserId}/mask/**")

    images = [i.split("\\")[-1] for i in images]
    set2 = set(drive_images)
    set1 = set(images)
    yes_images = list(set(drive_images) & set(images))
    no_images = set2 - set1
    masks = [i.split("\\")[-1] for i in masks]
    set1 = set(drive_masks)
    set2 = set(masks)
    yes_masks = list(set(drive_masks) & set(masks))
    no_masks = set2 - set1

    return no_images,yes_images,no_masks,yes_masks

def upload_time_update(paths,folder_type,UserId):
    json_path = f"drive/Dowload/{UserId}/data.json"
    if len(glob.glob(f"drive/Dowload/{UserId}/data.json")) == 0:
        formatted_dict = [dict(),dict()]
    else:
        with open(json_path,"r") as f:
            formatted_dict = json.load(f)
    if folder_type == "images":
        types = 0
    elif folder_type == "mask":
        types = 1
    else:
        raise ValueError("Dosya tipi yanlis!!!!")
    for path in paths:
        path = f"drive/Dowload/{UserId}/{folder_type}/{path}"
        formatted_time = read_time(path)
        formatted_dict[types][path.split("/")[-1]] = formatted_time
    with open(json_path,"w") as f:
        json.dump(formatted_dict,f)

def json_re(paths,UserId):
    for path in paths:
        with open(f"drive/Dowload/{UserId}/mask/{path}","r") as file:
            data = json.load(file)
        if "image_text" in list(data.keys()):
            if len(data["image_text"])>0:
                data["image_text"] = ""
        with open(f"drive/Dowload/{UserId}/mask/{path}","w") as file:
            json.dump(data,file)