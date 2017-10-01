from wtforms import widgets


class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, *args, **kwargs):
        kwargs['id'] = 'ckeditor'

        return super(CKTextAreaWidget, self).__call__(*args, **kwargs)
