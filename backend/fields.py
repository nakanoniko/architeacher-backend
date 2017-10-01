from wtforms.fields import TextAreaField
from .widgets import CKTextAreaWidget


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()
