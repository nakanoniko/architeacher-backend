import random, os, os.path as op

from flask import jsonify, url_for, request

from flask_admin import helpers

from backend import app, admin, db, security
from backend.models import DictBase, Building, Architect, Region, District, MetroRoute, MetroStation, Style, Element,\
    User, Role
from backend.views import SuperuserModelView, UserModelView, BuildingView, ArchitectView, ElementView, StyleView, \
    MetroStationView, DistrictView, RegionView, MetroRouteView, UserView

# mapping between endpoints and classes
mapping = {
    'regions': {
        'class': Region,
        'search': 'name'
    },
    'districts': {
        'class': District,
        'search': 'name'
    },
    'metro_routes': {
        'class': MetroRoute,
        'search': 'name'
    },
    'metro_stations': {
        'class': MetroStation,
        'search': 'name'
    },
    'buildings': {
        'class': Building,
        'search': 'title'
    },
    'architects': {
        'class': Architect,
        'search': 'name'
    },
    'styles': {
        'class': Style,
        'search': 'name'
    },
    'elements': {
        'class': Element,
        'search': 'name'
    },
}


def get_all(_cls, _search):
    def _get_all():

        if _search in request.args:
            search = request.args[_search]
        else:
            search = None

        if search:
            items = _cls.query.filter(getattr(_cls, _search).like('%'+search+'%')).all()
        else:
            items = _cls.query.all()

        return jsonify([item.to_dict() for item in items])

    return _get_all


def get_one(_cls):

    def _get_one(_id):
        item = _cls.query.get_or_404(_id)
        return jsonify(item.to_dict())

    return _get_one


def get_random(_cls):

    def _get_random():
        count = _cls.query.count()
        rnd = random.randrange(0, count)
        item = _cls.query[rnd]
        return jsonify(item.to_dict())

    return _get_random


for endpoint, val in mapping.items():
    app.add_url_rule('/api/' + endpoint, 'get_' + endpoint + '_all', get_all(val['class'], val['search']))
    app.add_url_rule('/api/' + endpoint + '/<int:_id>', 'get_' + endpoint + '_one', get_one(val['class'],))
    app.add_url_rule('/api/' + endpoint + '/random', 'get_' + endpoint + '_random', get_random(val['class'],))


admin.add_view(SuperuserModelView(Role, db.session))
admin.add_view(UserView(User, db.session))

admin.add_view(BuildingView(Building, db.session))
admin.add_view(ArchitectView(Architect, db.session))
admin.add_view(ElementView(Element, db.session))
admin.add_view(StyleView(Style, db.session))
admin.add_view(MetroRouteView(MetroRoute, db.session))
admin.add_view(MetroStationView(MetroStation, db.session))
admin.add_view(DistrictView(District, db.session))
admin.add_view(RegionView(Region, db.session))

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=helpers,
        get_url=url_for
    )
