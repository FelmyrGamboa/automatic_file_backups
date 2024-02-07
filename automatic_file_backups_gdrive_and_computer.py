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