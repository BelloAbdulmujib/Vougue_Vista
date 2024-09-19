import re
from flask import current_app
from flask_admin.form import FileUploadField
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from wtforms.validators import ValidationError
import os

def sanitize_filename(filename):
    # Remove invalid characters and limit the length
    sanitized = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    return sanitized[:255] 

def allowed_file(filename):
    allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

class ProductAdmin(ModelView):
    form_extra_fields = {
        'image': FileUploadField('Product Image', base_path='uploads')
    }

    def is_accessible(self):
        return True

    def on_model_change(self, form, model, is_created):
        """ Process the uploaded image file """
        if form.image.data:
            UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER'] 
            filename = sanitize_filename(form.image.data.filename)
            if allowed_file(filename):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                form.image.data.save(file_path)
                model.image = filename
            else:
                raise ValidationError("File type not allowed. Please upload a valid image.")
