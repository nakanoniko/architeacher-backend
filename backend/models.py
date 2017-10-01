from backend import db
from datetime import date
from flask_security import RoleMixin, UserMixin


def dictonify(d: dict, exclude=None):
    if exclude is None:
        exclude = ['_sa_instance_state']
    return {
        k: v if not isinstance(v, date) else str(v) if v is not None else None
        for k, v
        in d.items()
        if k not in exclude and not isinstance(v, list)
    }


class DictBase:
    def to_dict(self):
        return dictonify(self.__dict__)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


building_architect = db.Table(
    'building_architect',
    db.Column('building_id', db.Integer, db.ForeignKey('building.id')),
    db.Column('architect_id', db.Integer, db.ForeignKey('architect.id'))
)

building_style = db.Table(
    'building_style',
    db.Column('building_id', db.Integer, db.ForeignKey('building.id'), nullable=False),
    db.Column('style_id', db.Integer, db.ForeignKey('style.id'), nullable=False)
)

architect_style = db.Table(
    'architect_style',
    db.Column('architect_id', db.Integer, db.ForeignKey('architect.id'), nullable=False),
    db.Column('style_id', db.Integer, db.ForeignKey('style.id'), nullable=False)
)

element_style = db.Table(
    'element_style',
    db.Column('element_id', db.Integer, db.ForeignKey('element.id'), nullable=False),
    db.Column('style_id', db.Integer, db.ForeignKey('style.id'), nullable=False)
)

station_route = db.Table(
    'station_route',
    db.Column('station_id', db.Integer, db.ForeignKey('metro_station.id'), nullable=False),
    db.Column('route_id', db.Integer, db.ForeignKey('metro_route.id'), nullable=False)
)


class MetroRoute(db.Model, DictBase):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

    def to_dict(self):
        result = dictonify(self.__dict__)
        result.update({
            'stations': [station.id for station in self.stations]
        })
        return result

    def __str__(self):
        return self.name


class MetroStation(db.Model, DictBase):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    routes = db.relationship('MetroRoute', secondary=station_route, backref=db.backref('stations', lazy='dynamic'))
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'), nullable=False)
    district = db.relationship('District', backref=db.backref('stations', lazy='dynamic'))
    description = db.Column(db.String, nullable=False)

    def to_dict(self):
        result = dictonify(self.__dict__)
        result.update({
            'routes': [route.id for route in self.routes]
        })
        return result

    def __str__(self):
        return self.name


class District(db.Model, DictBase):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    region = db.relationship('Region', backref=db.backref('districts', lazy='dynamic'))
    description = db.Column(db.String, nullable=False)

    def __str__(self):
        return self.name


class Region(db.Model, DictBase):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    abbr = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    def __str__(self):
        return self.name


class BuildingImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'), nullable=False)

    def __str__(self):
        return self.name + ': ' + self.path


class BuildingNumberFact(db.Model, DictBase):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'), nullable=False)


class BuildingTextFact(db.Model, DictBase):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'), nullable=False)


class Building(db.Model, DictBase):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    title_info = db.Column(db.String)
    address = db.Column(db.String, nullable=False)
    year_build_start = db.Column(db.Integer, nullable=False)
    year_build_end = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    architects = db.relationship('Architect',
                                 secondary=building_architect,
                                 backref=db.backref('buildings', lazy='dynamic'))
    styles = db.relationship('Style',
                             secondary=building_style,
                             backref=db.backref('buildings', lazy='dynamic'))

    leading_img_path = db.Column(db.String, nullable=False)
    images = db.relationship('BuildingImage', backref=db.backref('building'))

    text = db.Column(db.Text, nullable=False)

    station_id = db.Column(db.Integer, db.ForeignKey('metro_station.id'), nullable=False)
    station = db.relationship('MetroStation', backref=db.backref('buildings', lazy='dynamic'))

    district_id = db.Column(db.Integer, db.ForeignKey('district.id'), nullable=False)
    district = db.relationship('District', backref=db.backref('buildings', lazy='dynamic'))

    text_facts = db.relationship('BuildingTextFact', backref=db.backref('building'))
    number_facts = db.relationship('BuildingNumberFact', backref=db.backref('building'))

    def __str__(self):
        return self.title

    def to_dict(self):
        result = dictonify(self.__dict__)
        result.update({
            'images': [
                {
                    'id': image.id,
                    'name': image.name,
                    'path': image.path
                } for image in self.images
            ],
            'architects': [
                {
                    'id': architect.id,
                    'name': architect.surname
                } for architect in self.architects
            ],
            'styles': [
                {
                    'id': style.id,
                    'name': style.name,
                    'path': style.building_img_path,
                } for style in self.styles
            ],
            'number_facts': [
                {
                    'id': fact.id,
                    'number': fact.number,
                    'name': fact.name
                } for fact in self.number_facts
            ],
            'text_facts': [
                {
                    'id': fact.id,
                    'text': fact.text
                } for fact in self.text_facts
            ]

        })
        return result


class ArchitectFact(db.Model, DictBase):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)
    architect_id = db.Column(db.Integer, db.ForeignKey('architect.id'), nullable=False)


class Architect(db.Model, DictBase):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    patronymic = db.Column(db.String)
    born = db.Column(db.Integer)
    died = db.Column(db.Integer)
    alive = db.Column(db.Boolean, default=False, nullable=False)
    place_of_birth = db.Column(db.String, nullable=False)
    quote = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)
    styles = db.relationship('Style', backref=db.backref('architects', lazy='dynamic'), secondary=architect_style)
    img_path = db.Column(db.String)
    square_img = db.Column(db.String)
    portrait_img = db.Column(db.String)
    landscape_img = db.Column(db.String)
    facts = db.relationship('ArchitectFact', backref=db.backref('architect'))

    def __str__(self):
        return '{}, {} {}'.format(self.surname, self.name, self.patronymic)

    def to_dict(self):
        result = dictonify(self.__dict__)
        result.update({
            'styles': [
                {
                    'id': style.id,
                    'name': style.name,
                } for style in self.styles
            ],
            'buildings': [
                {
                    'id': building.id,
                    'title': building.title,
                    'title_info': building.title_info,
                    'path': building.leading_img_path,
                } for building in self.buildings
            ],
            'facts': [
                fact.to_dict()
                for fact in self.facts
            ]
        })
        return result


class Style(db.Model, DictBase):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    previous_id = db.Column(db.Integer, db.ForeignKey('style.id'))
    previous = db.relationship('Style', backref=db.backref('following', uselist=False), remote_side=[id], uselist=False)
    date = db.Column(db.Integer, nullable=False)
    philosophy = db.Column(db.String, nullable=False)
    ideology = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)
    fact = db.Column(db.String, nullable=False)
    building_img_path = db.Column(db.String, nullable=False)
    door_handle_img_path = db.Column(db.String, nullable=False)
    column_img_path = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    def __str__(self):
        return self.name

    def to_dict(self):
        result = dictonify(self.__dict__)
        result.update({
            'following_id': self.following.id if self.following else None,
            'architects': [
                {
                    'id': architect.id,
                    'surname': architect.surname,
                    'patronymic': architect.patronymic,
                    'name': architect.name,
                    'path': architect.img_path
                } for architect in self.architects],
            'buildings': [
                {
                    'id': building.id,
                    'title': building.title,
                    'title_info': building.title_info,
                    'path': building.leading_img_path,
                } for building in self.buildings
            ],
            'elements': [
                {
                    'id': element.id,
                    'name': element.name,
                    'description': element.description,
                    'path': element.img_path

                } for element in self.elements
            ]
        })
        return result


class ElementExample(db.Model, DictBase):
    id = db.Column(db.Integer, primary_key=True)
    img_path = db.Column(db.String, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'), nullable=False)
    building = db.relationship('Building')
    element_id = db.Column(db.Integer, db.ForeignKey('element.id'), nullable=False)


class ElementPlace(db.Model, DictBase):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    element_id = db.Column(db.Integer, db.ForeignKey('element.id'), nullable=False)


class Element(db.Model, DictBase):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    date = db.Column(db.Integer, nullable=False)
    styles = db.relationship('Style', secondary=element_style, backref=db.backref('elements', lazy='dynamic'))
    places = db.relationship('ElementPlace', backref=db.backref('element'))
    examples = db.relationship('ElementExample', backref=db.backref('element'))
    text = db.Column(db.Text, nullable=False)
    img_path = db.Column(db.String, nullable=False)

    def __str__(self):
        return self.name

    def to_dict(self):
        result = dictonify(self.__dict__)
        result.update({
            'styles': [
                {
                    'id': style.id,
                    'name': style.name
                } for style in self.styles
            ],
            'places': [
                {
                    'id': place.id,
                    'name': place.name
                } for place in self.places
            ],
            'examples': [
                {
                    'id': example.id,
                    'img_path': example.img_path,
                    'building': {
                        'id': example.building.id,
                        'title': example.building.title,
                        'title_info': example.building.title_info,
                    }
                } for example in self.examples
            ]
        })
        return result
