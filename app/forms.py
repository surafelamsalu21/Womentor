from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

class ResumeUploadForm(FlaskForm):
    """Form for uploading resumes."""
    file = FileField('Upload Resume', validators=[DataRequired(message="Please upload a file.")])
    submit = SubmitField('Upload')
