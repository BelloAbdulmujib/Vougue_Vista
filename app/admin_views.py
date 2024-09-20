from flask_admin.contrib.sqla import ModelView
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_admin.form import FileUploadField
from wtforms.validators import ValidationError
import cloudinary.uploader

class ProductAdmin(ModelView):
    # Use FileField to handle file uploads in the form
    form_extra_fields = {
        'image': FileField('Product Image', validators=[
            FileRequired(),
            FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
        ])
    }

    def on_model_change(self, form, model, is_created):
        """ Process the uploaded image file to Cloudinary """
        if form.image.data:
            try:
                upload_result = cloudinary.uploader.upload(form.image.data)
                # Save the secure_url (or public_id) to the model's image field
                model.image = upload_result.get('secure_url')

            except Exception as e:
                raise ValidationError(f"Failed to upload image: {str(e)}")
