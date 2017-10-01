import os
import os.path as op
from base64 import b64encode
from datetime import datetime

from flask import abort, redirect, request, url_for

from flask_security import current_user

from flask_admin.contrib.sqla import ModelView
from flask_admin.model.form import InlineFormAdmin
from flask_admin.form.upload import ImageUploadField, FileUploadField
from markupsafe import Markup

from backend.models import BuildingImage, BuildingNumberFact, BuildingTextFact, ArchitectFact, ElementPlace, \
    ElementExample, Style
from backend.fields import CKTextAreaField

images_path = op.join(op.dirname(__file__), '../images/uploads')


class CustomModelView(ModelView):
    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))


def is_accessible(role):
    if not current_user.is_active or not current_user.is_authenticated:
        return False

    if current_user.has_role(role):
        return True
    return False


class SuperuserModelView(CustomModelView):
    def is_accessible(self):
        return is_accessible('superuser')


class UserModelView(CustomModelView):
    def is_accessible(self):
        return is_accessible('user')


def gen_filename(filename):
    ext = filename.split('.')[-1]
    filename = b64encode(str(datetime.now()).encode()).decode() + '.' + ext
    return filename


class BuildingImageView(InlineFormAdmin):
    form_overrides = {
        'path': ImageUploadField,
    }
    form_args = {
        'path': {
            'base_path': images_path,
            'url_relative_path': 'images/uploads/',
            'namegen': lambda u, v: gen_filename(v.filename),
        }

    }


class BuildingView(UserModelView):
    column_default_sort = 'title'
    column_searchable_list = ('title',)
    column_list = (
        'title',
        'year_build_start',
        'year_build_end',
        'address',
        'station',
        'district',
    )

    column_sortable_list = (
        ('station', 'station.name'),
        ('district', 'district.name'),
        'title',
        'year_build_start',
        'year_build_end',
        'address'
    )

    column_formatters = {
        'station': lambda v, c, m, name: Markup('<a href=/admin/metrostation/edit/?id={}>{}</a>'
                                                .format(m.station.id, m.station.name)) if m.station else '',
        'district': lambda v, c, m, name: Markup('<a href=/admin/district/edit/?id={}>{}</a>'
                                                 .format(m.district.id, m.district.name)) if m.district else '',
        'title': lambda v, c, m, name: Markup('<a href=edit/?id={}>{}</a>'
                                              .format(m.id, m.title))

    }

    form_overrides = {
        'text': CKTextAreaField,
        'leading_img_path': ImageUploadField,
    }

    form_args = {
        'leading_img_path': {
            'base_path': images_path,
            'url_relative_path': 'images/uploads/',
            'namegen': lambda u, v: gen_filename(v.filename),
        }
    }

    inline_models = (BuildingTextFact,
                     BuildingNumberFact,
                     BuildingImageView(BuildingImage))

    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'


class ArchitectView(UserModelView):
    column_default_sort = 'name'
    column_searchable_list = ('name',)
    column_list = (
        'surname',
        'name',
        'patronymic',
        'born',
        'died'
    )

    inline_models = (ArchitectFact,)

    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'

    form_overrides = {
        'img_path': ImageUploadField,
        'square_img': ImageUploadField,
        'landscape_img': ImageUploadField,
        'portrait_img': ImageUploadField,

        'text': CKTextAreaField
    }

    column_formatters = {
        'surname': lambda v, c, m, name: Markup('<a href=edit/?id={}>{}</a>'
                                                .format(m.id, m.surname))
    }

    _img_args = {
        'base_path': images_path,
        'url_relative_path': '/images/uploads/',
        'namegen': lambda u, v: gen_filename(v.filename),
    }

    form_args = {
        'img_path': _img_args,
        'square_img': _img_args,
        'landscape_img': _img_args,
        'portrait_img': _img_args,
    }


def image_column_formatter(_id, path, big=False):
    return Markup('<a href="edit/?id={}" style="margin:auto; display:block; text-align:center;">'
                  '<img src="{}" style="width:{};"/>'
                  '</a>'
                  .format(_id, '/images/uploads/' + path, '75%' if big else '30%'))


class ElementExampleView(InlineFormAdmin):
    form_overrides = {
        'img_path': ImageUploadField,
    }
    form_args = {
        'img_path': {
            'base_path': images_path,
            'url_relative_path': 'images/uploads/',
            'namegen': lambda u, v: gen_filename(v.filename),
        }

    }

class ElementView(UserModelView):
    column_default_sort = 'name'
    column_searchable_list = ('name',)
    column_list = (
        'name',
        'date',
        'img_path'
    )

    inline_models = (ElementPlace, ElementExampleView(ElementExample))

    form_overrides = {
        'text': CKTextAreaField,
        'img_path': FileUploadField
    }

    form_args = {
        'img_path': {
            'namegen': lambda u, v: gen_filename(v.filename),
            'base_path': images_path,
        }
    }

    column_formatters = {
        'img_path': lambda v, c, m, name: image_column_formatter(m.id, m.img_path),
        'name': lambda v, c, m, name: Markup('<a href=edit/?id={}>{}</a>'
                                             .format(m.id, m.name))
    }

    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'


class StyleView(UserModelView):
    column_default_sort = 'name'
    column_searchable_list = ('name',)
    column_list = (
        'name',
        'date',
        'building_img_path',
        'door_handle_img_path',
        'column_img_path',
        'previous',
        'following'
    )

    column_sortable_list = (
        'name',
        'date',
        'building_img_path',
        'door_handle_img_path',
        'column_img_path',
        'previous',
        'following'
    )

    form_overrides = {
        'text': CKTextAreaField,
        'building_img_path': FileUploadField,
        'column_img_path': FileUploadField,
        'door_handle_img_path': FileUploadField,
    }

    _img_args = {
        'namegen': lambda u, v: gen_filename(v.filename),
        'base_path': images_path,
    }

    form_args = {
        'building_img_path': _img_args,
        'door_handle_img_path': _img_args,
        'column_img_path': _img_args
    }

    column_formatters = {
        'building_img_path': lambda v, c, m, name: image_column_formatter(m.id, m.building_img_path, big=True),
        'door_handle_img_path': lambda v, c, m, name: image_column_formatter(m.id, m.door_handle_img_path),
        'column_img_path': lambda v, c, m, name: image_column_formatter(m.id, m.column_img_path),
        'name': lambda v, c, m, name: Markup('<a href=edit/?id={}>{}</a>'.format(m.id, m.name)),
        'previous': lambda v, c, m, name: Markup('<a href=edit/?id={}>{}</a>'
                                                 .format(m.previous.id, m.previous.name) if m.previous else ''),
        'following': lambda v, c, m, name: Markup('<a href=edit/?id={}>{}</a>'
                                                  .format(m.following.id, m.following.name) if m.following else ''),

    }

    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'


class MetroStationView(UserModelView):
    column_default_sort = 'name'
    column_searchable_list = ('name',)
    column_list = (
        'name',
        'district',
    )

    column_sortable_list = (
        'name',
        ('district', 'district.name'),
    )
    column_formatters = {
        'name': lambda v, c, m, name: Markup('<a href=edit/?id={}>{}</a>'.format(m.id, m.name)),
        'district': lambda v, c, m, name: Markup('<a href=edit/?id={}>{}</a>'.format(m.district.id, m.district.name)),
    }


class DistrictView(UserModelView):
    column_default_sort = 'name'
    column_searchable_list = ('name',)
    column_list = (
        'name',
        'region',
    )

    column_sortable_list = (
        'name',
        ('region', 'region.name'),
    )

    column_formatters = {
        'name': lambda v, c, m, name: Markup('<a href=edit/?id={}>{}</a>'.format(m.id, m.name)),
        'region': lambda v, c, m, name: Markup('<a href=edit/?id={}>{}</a>'.format(m.region.id, m.region.name)),
    }


class RegionView(UserModelView):
    column_default_sort = 'name'
    column_searchable_list = ('name',)
    column_list = (
        'name',
        'abbr',
    )

    column_formatters = {
        'name': lambda v, c, m, name: Markup('<a href=edit/?id={}>{}</a>'.format(m.id, m.name)),
    }


class MetroRouteView(UserModelView):
    column_default_sort = 'name'
    column_searchable_list = ('name',)
    column_list = (
        'name',
        'color',
    )

    column_formatters = {
        'name': lambda v, c, m, name: Markup('<a href=edit/?id={}>{}</a>'.format(m.id, m.name)),
        'color': lambda v, c, m, name: Markup('<a href=edit/?id={}>'
                                              '<div style="background-color:{}; height:20px;">'
                                              '</div>'
                                              '</a>'
                                              .format(m.id, m.color))
    }


class UserView(SuperuserModelView):
    column_exclude_list = ('password',)
