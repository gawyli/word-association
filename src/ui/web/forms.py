from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ResponseForm(FlaskForm):
    response = StringField('Your Response', validators=[DataRequired()])
    submit = SubmitField('Submit')