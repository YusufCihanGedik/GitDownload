from drive.Google import Create_Service
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload

import os
import io
import pandas as pd
import time

CLIENT_SECRET_FILE = "client_secret_918073330772-etjv2j7ogaki3ud3487iih1p5j95uv3k.apps.googleusercontent.com.json"
API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]

global FOLDER_ID
FOLDER_ID = None

servise = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
folder_id = "1iaCnBLffKoerFnuQburYZglFXTnpqb9V"
query = f"parents = '{folder_id}'"

def total_folder_read():
    folder_id = "1iaCnBLffKoerFnuQburYZglFXTnpqb9V"
    query = f"parents = '{folder_id}'"
    response = servise.files().list(q=query,fields='files(kind,mimeType,id,name, modifiedTime)').execute()
    files = response.get("files",[])

    df = pd.DataFrame(files)
    return df["name"].to_list()

def folder_read(UserId):
    folder_id = "1iaCnBLffKoerFnuQburYZglFXTnpqb9V"
    query = f"parents = '{folder_id}'"
    response = servise.files().list(q=query,fields='files(kind,mimeType,id,name, modifiedTime)').execute()
    files = response.get("files",[])

    df = pd.DataFrame(files)
    FOLDER_ID = df[df["name"]== UserId]["id"].values[0]

    query = f"parents = '{FOLDER_ID}'"
    response = servise.files().list(q=query,fields='files(kind,mimeType,id,name, modifiedTime)').execute()
    files = response.get("files",[])
    df = pd.DataFrame(files)

    image_id = df[df["name"] == "images"]["id"].values[0]
    mask_id = df[df["name"] == "mask"]["id"].values[0]
    
    query = f"parents = '{image_id}'"
    response = servise.files().list(q=query,fields='files(kind,mimeType,id,name, modifiedTime)').execute()
    files = response.get("files",[])
    images_df = pd.DataFrame(files)

    query = f"parents = '{mask_id}'"
    response = servise.files().list(q=query,fields='files(kind,mimeType,id,name, modifiedTime)').execute()
    files = response.get("files",[])
    masks_df = pd.DataFrame(files)

    return images_df,masks_df,image_id,mask_id

def folder_dowload(file_ids,files_names,folder_type,use_id):
    for file_id, file_name in zip(file_ids, files_names):
        request = servise.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print("Download prosses {0}".format(status.progress() * 100))
        fh.seek(0)
        with open(os.path.join("./drive/Dowload/{0}/{1}".format(use_id,folder_type), file_name), "wb") as f:
            f.write(fh.read())
            f.close()

def folder_upload(file_names,mime_types,folder_type,folder_id,UserId=None):
    if folder_id is None:
        if UserId is None:
            raise ValueError("UserId bulunmuyor")
        folder_read(UserId)
    path = f"drive/Dowload/{UserId}/{folder_type}"

    for file_name, mime_type in zip(file_names, mime_types):
        file_metadata = {
            "name": file_name,
            "parents": [folder_id]
        }
        media = MediaFileUpload("./{0}/{1}".format(path,file_name), mimetype=mime_type)
        servise.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()

def folder_update(file_names,mime_types,file_ids,folder_type,folder_id,UserId=None):
    if folder_id is None:
        if UserId is None:
            raise ValueError("UserId bulunmuyor")
        folder_read(UserId)
    path = f"drive/Dowload/{UserId}/{folder_type}"

    for file_name, mime_type,file_id in zip(file_names, mime_types, file_ids):
        file_metadata = {
            "name" : file_name
        }

        media = MediaFileUpload("./{0}/{1}".format(path,file_name), mimetype=mime_type)
        servise.files().update(
        fileId=file_id,
        body=file_metadata,
        media_body=media
        ).execute()

def drive_delete(UserId):
    images_df,masks_df,image_id,mask_id = folder_read(UserId)
    for file_id in images_df["id"]:
        try:
            servise.files().delete(fileId=file_id).execute()
            print("Dosya başarıyla silindi.")
        except Exception as error:
            print(f'Hata oluştu: {error}')
    for file_id in masks_df["id"]:
        try:
            servise.files().delete(fileId=file_id).execute()
            print("Dosya başarıyla silindi.")
        except Exception as error:
            print(f'Hata oluştu: {error}')

def folder_create(national_part):
    folder_id = "13t1yHfeoRQQfM4v_NKHof5rLE7F3_Upp"
    file_metadata = {
        "name": national_part,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [folder_id]
    }
    created_folder = servise.files().create(body=file_metadata).execute()
    created_folder_id = created_folder.get("id")
    image_file_metadata = {
        "name": "images",
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [created_folder_id]
    }
    mask_file_metadata = {
        "name": "mask",
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [created_folder_id]
    }
    servise.files().create(body=image_file_metadata).execute()
    servise.files().create(body=mask_file_metadata).execute()

def data_drive_read(UserId):
    folder_id = "13t1yHfeoRQQfM4v_NKHof5rLE7F3_Upp"
    query = f"parents = '{folder_id}'"
    response = servise.files().list(q=query,fields='files(kind,mimeType,id,name, modifiedTime)').execute()
    files = response.get("files",[])

    df = pd.DataFrame(files)
    if len(df)<1:
        print(UserId)
        folder_create(UserId)
    if len(df[df["name"]== UserId])<1:
        folder_create(UserId)
        response = servise.files().list(q=query,fields='files(kind,mimeType,id,name, modifiedTime)').execute()
        files = response.get("files",[])
        df = pd.DataFrame(files)
    FOLDER_ID = df[df["name"]== UserId]["id"].values[0]

    query = f"parents = '{FOLDER_ID}'"
    response = servise.files().list(q=query,fields='files(kind,mimeType,id,name, modifiedTime)').execute()
    files = response.get("files",[])
    df = pd.DataFrame(files)

    image_id = df[df["name"] == "images"]["id"].values[0]
    mask_id = df[df["name"] == "mask"]["id"].values[0]
    
    return image_id,mask_id

def data_drive_upload(file_names,mime_types,folder_type,folder_id,UserId):
    path = f"drive/Dowload/{UserId}/{folder_type}"
    print(file_names)
    for file_name, mime_type in zip(file_names, mime_types):
        file_metadata = {
            "name": file_name,
            "parents": [folder_id]
        }
        media = MediaFileUpload("./{0}/{1}".format(path,file_name), mimetype=mime_type)
        servise.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()