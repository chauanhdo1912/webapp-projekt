import os
from werkzeug.utils import secure_filename
from flask import current_app
from functools import wraps
from flask import abort, flash
from flask_login import current_user


def save_food_image(file_storage):
    if file_storage and file_storage.filename != '':
        filename= secure_filename(file_storage.filename)
        
        upload_folder= os.path.join(current_app.root_path, 'static','dishes_uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_storage.save(os.path.join(upload_folder,filename))
        return filename
    return None


