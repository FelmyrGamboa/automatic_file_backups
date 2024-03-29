# Final Project: Automated Google Drive Backups
# https://youtu.be/fkWM7A-MxR0
# https://youtu.be/zT7niRUOs9o

import os
import os.path
import shutil
import datetime
import schedule
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

source_dir = r"C:\Users\Felmyr Gamboa\Desktop\BSCpE 1-5 First Sem\Programming Logic and Design\Final Project\backupfiles_trial"
destination_dir = r"C:\Users\Felmyr Gamboa\Desktop\Backups"

def creating_backup_folder_to_directory(source, dest):

    today = datetime.date.today()
    destination_dir = os.path.join(dest, str(today))

    try:
        shutil.copytree(source, destination_dir)
        print(f"Folder copied to: {destination_dir}")

    except FileExistsError:
        print(f"Folder already exists in: {dest} \n")

scopes = ['https://www.googleapis.com/auth/drive']

credits = None

def automate_gdrive_backup_files():
    if os.path.exists("token.json"):
        credits = Credentials.from_authorized_user_file("token.json", scopes)

    if not credits or not credits.valid:
        if credits and credits.expired and credits.refresh_token:
            credits.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "automatic_file_backups/user_credentials.json", scopes)
            credits = flow.run_local_server(port = 0)

        with open("token.json", 'w') as token:
            token.writable(credits.to_json())

    try:
        service = build("drive", "v3", credentials = credits)

        response = service.files().list(
            q = "name = 'BackupFolder' and mimeType = 'application/vnd.google-apps.folder'",
            spaces = 'drive'
        ).execute()

        if not response['files']:
            file_metadata = {
                "name" : "BackupFolder",
                "mimeType" : "application/vnd.google-apps.folder"
            }

            file = service.files().create(body = file_metadata, fields = "id").execute()

            folder_id = file.get('id')

        else: 
            folder_id = response["files"][0]['id']

        for file in os.listdir("backupfiles_trial"):
            file_metadata = {
                "name": file,
                "parents": [folder_id]

            }

            media = MediaFileUpload(f"backupfiles_trial/{file}")
            upload_file = service.files().create(body = file_metadata,
                                                 media_body = media,
                                                 fields = "id").execute()
            
            print("Backed up files: " + file)
        print("\nFiles has been backup in google drive. ")

    except HttpError as execute:
        print("Error: " + str(execute))


schedule.every().day.at("01:40").do(lambda: creating_backup_folder_to_directory(source_dir, destination_dir))
schedule.every().day.at("01:40").do(lambda: automate_gdrive_backup_files())

while True:
    schedule.run_pending()
    time.sleep(60)