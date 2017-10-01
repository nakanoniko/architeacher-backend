from flask_security.utils import encrypt_password

from backend import db, app
from backend.models import Building, BuildingImage, Architect, MetroRoute, MetroStation, District, Region, \
    BuildingNumberFact, BuildingTextFact, Style, ArchitectFact, Element, ElementPlace, ElementExample, User,Role

from backend import user_datastore

from datetime import datetime
import random

text = '<p>Жилой дом на Котельнической набережной — одна из «сталинских высоток» в Москве, находится в ' \
       'устье реки Яузы по адресу Котельническая набережная № 1/15. Построена в 1938—1952 годах; авторы ' \
       'проекта — Д. Н. Чечулин, А. К. Ростковский, инженер Л. М. Гохман. Является памятником ' \
       'архитектуры регионального значения.</p><blockquote>«Старый», 9-этажный жилой корпус, ' \
       'выходящий на Москва-реку, был спроектирован в 1938 году и завершён в 1940-м. Центральный объём ' \
       'строился в 1948—1952 годах. Он насчитывает 26 этажей (32 вместе с техническими этажами) и имеет ' \
       'высоту 176 м.</blockquote><p>Всего в здании находятся 700 квартир, 540 из них расположены в ' \
       'центральном объёме (из них 336 двухкомнатных, 173 трёхкомнатных, 18 четырёхкомнатных и 13 ' \
       'однокомнатных). Из широких окон квартир на верхних этажах открывается вид на город, Москву-реку ' \
       'и Кремль. Также в здании находятся магазины, почтовое отделение, кинотеатр «Иллюзион» (базовый ' \
       'кинотеатр Госфильмофонда; выходит на Большой Ватин переулок), музей-квартира Г. С. Улановой (' \
       'открылась в 2004 году в кв. № 185 — балерина жила здесь с 1986 года, а ранее, с октября 1952 ' \
       'года, занимала квартиру № 316 в корпусе Б).</p><p>Помещения общественного назначения, ' \
       'такие как овощной (со стороны Подгорной набережной) и кондитерский (торец здания со стороны ' \
       'Верхней Радищевской) магазины, существовавшие до начала 2000-х годов, отличались своими ' \
       'интерьерами: стены и потолки были богато украшены пышными росписями с изображениями цветочных ' \
       'гирлянд и всевозможных даров природы. Входные вестибюли и лифтовые холлы жилых подъездов также ' \
       'декорированы барельефами, лепниной и росписями.</p><blockquote>Корпус А был изначально заселён ' \
       'работниками НКВД[3].</blockquote><p>Дом строили советские заключённые и немецкие военнопленные[' \
       '4][5][6], привлечённые через Главное управления лагерей промышленного строительства (' \
       'Главпромстрой)[7]. Согласно воспоминаниям жительницы дома С. Н. Перовской, в 1954 году, ' \
       'когда она сюда переехала, на окнах 5-го и 8-го этажей, где были большие карнизы, ' \
       '«стояли решетки, чтобы не могли выбраться заключённые»[8].</p> '


def generate_text():
    return ' '.join([
        ''.join([random.choice('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
                 for _ in range(1, random.randint(4, 10))])
        for _ in range(1, random.randint(26, 50))
    ])


def create_db():
    with app.app_context():
        app.logger.info('reflecting db')
        db.reflect()

        app.logger.info('dropping db')
        db.drop_all()

        app.logger.info('creating db')
        db.create_all()

        roles = [
            Role(name="user"),
            Role(name="superuser")
        ]
        db.session.add_all(roles)

        user_datastore.create_user(
            first_name='Никита',
            last_name='Кулаков',
            email='kul7nik@gmail.com',
            password=encrypt_password('Kul7nick'),
            roles=roles,
        )
        user_datastore.create_user(
            first_name='Екатерина',
            last_name='Лебедева',
            email='katerlebedevaa@yandex.ru',
            password=encrypt_password('Lasunec123'),
            roles=roles[:1],
        )

        routes = [
            MetroRoute(
                color='rgb({0},{1},{2})'.format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                name='Ветка #' + str(i)
            ) for i in range(1, 11)
        ]

        regions = [
            Region(
                name='Округ #' + str(i),
                abbr='ABBR',
                description=generate_text()[:50]
            ) for i in range(1, 11)
        ]

        districts = [
            District(
                name='Район #' + str(i),
                region=regions[(i - 1) // 4],
                description=generate_text()[:50]
            ) for i in range(1, 41)
        ]

        stations = [
            MetroStation(
                name='Станция #' + str(i),
                district=districts[i - 1],
                routes=[routes[(i - 1) % len(routes)], routes[i % len(routes)]],
                description=generate_text()[:50]
            ) for i in range(1, 41)
        ]

        app.logger.info('creating buildings')
        buildings = [
            Building(
                title='Title #' + i,
                title_info='Some info in title #' + i,
                year_build_start=int(datetime.now().year),
                year_build_end=int(datetime.now().year),
                leading_img_path='visotka.jpg',
                latitude=random.uniform(55.614926, 55.860389),
                longitude=random.uniform(37.416317, 37.772211),
                images=[
                    BuildingImage(
                        name='image #{}:{}'.format(1, i),
                        path='shema.jpg'
                    ),
                    BuildingImage(
                        name='image #{}:{}'.format(2, i),
                        path='visota.jpg'
                    ),
                    BuildingImage(
                        name='image #{}:{}'.format(3, i),
                        path='visotka.jpg'
                    )

                ],
                text=text,
                address='address #' + i,
                station=stations[random.randint(0, 39)],
                district=districts[random.randint(0, 39)],
                number_facts=[
                    BuildingNumberFact(
                        number=j * random.randint(1, 100),
                        name='nfact #' + str(j)
                    )
                    for j in range(1, random.randint(2, 4))
                ],
                text_facts=[
                    BuildingTextFact(
                        text=generate_text()
                    )
                ]
            ) for i in map(str, range(1, 11))
        ]

        architects = [
            Architect(name='Name#' + str(i),
                      surname='Surname#' + str(i),
                      patronymic='Patronymic#' + str(i),
                      born=random.choice([1825, 1927, None, 1953]),
                      died=random.choice([1825, 1927, None, 1953]),
                      alive=random.choice([False, False, False, True]),
                      place_of_birth='Place of birth #' + str(i),
                      quote=generate_text()[:100],
                      text=text,
                      img_path='shusev.jpg',
                      facts=[
                          ArchitectFact(
                              name='name#' + str(i),
                              text=generate_text()[:60]
                          )
                          for i in range(1, random.randint(2, 5))
                      ],
                      square_img='arch-square.png',
                      portrait_img='arch-portrait.png',
                      landscape_img='arch-landscape.png'

                      )
            for i in range(1, 20)
        ]
        for i, architect in enumerate(architects):
            if i < len(architects) - 1:
                architect.buildings = [buildings[i % len(buildings)], buildings[(i+1) % len(buildings)]]
            else:
                architect.buildings = [buildings[i % len(buildings)]]

        styles = [
            Style(name="Стиль #" + str(i),
                  date=random.choice([1800, 1810, 1825, 1840, 1860, 1875]),
                  philosophy='philosophy #' + str(i),
                  ideology='ideology #' + str(i),
                  text=text,
                  fact=generate_text(),
                  architects=[architects[i - 1], architects[(i * 2) % len(architects)]],
                  buildings=[buildings[i - 1]],
                  building_img_path='klass-build.svg',
                  column_img_path='klass-col.svg',
                  door_handle_img_path='klass-door.svg',
                  description=generate_text()[:75]
                  )
            for i in range(1, 11)
        ]
        for i, style in enumerate(styles):
            if i != 0:
                styles[i].previous = styles[i - 1]

        elements = [
            Element(
                name='Element#' + str(i),
                date=random.choice([1800, 1810, 1825, 1840, 1860, 1875]),
                text=text,
                styles=[styles[i - 1], styles[i * 2 % len(styles)]],
                places=[
                    ElementPlace(
                        name='Element Place #1:' + str(i)
                    ),
                    ElementPlace(
                        name='Element Place #2:' + str(i)
                    ),
                    ElementPlace(
                        name='Element Place #3:' + str(i)
                    ),
                    ElementPlace(
                        name='Element Place #4:' + str(i)
                    ),
                ],
                examples=[
                    ElementExample(
                        img_path='usadba.jpg',
                        building=buildings[i - 1]
                    ),
                    ElementExample(
                        img_path='usadba.jpg',
                        building=buildings[i * 2 % len(buildings)],
                    ),
                ],
                img_path='kartush.svg',
                description=generate_text()[:60]
            )
            for i in range(1, 11)
        ]

        db.session.add_all(buildings)
        db.session.add_all(architects)
        db.session.add_all(routes)
        db.session.add_all(stations)
        db.session.add_all(districts)
        db.session.add_all(regions)
        db.session.add_all(styles)
        db.session.add_all(elements)

        db.session.commit()
