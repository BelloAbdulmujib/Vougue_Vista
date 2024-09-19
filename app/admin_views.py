from flask_admin.form import FileUploadField
from flask_admin.contrib.sqla import ModelView
from flask_uploads import UploadSet, IMAGES
from werkzeug.utils import secure_filename
from flask import redirect, url_for

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'jpeg', 'png', 'jpg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class ProductAdmin(ModelView):
    form_extra_fields = {
        'image': FileUploadField('Product Image')
    }

    def on_model_change(self, form, model, is_created):
        """ Process the uploaded image file """
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            form.image.data.save(file_path)
            model.image = filename
