import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, sessionmaker

from open_precision.core.model.vehicle import Vehicle

basedir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.abspath(
    '../../../../.config/JetBrains/PyCharm2022.1/scratches/user_interfaces/flask_web_ui/templates')
static_dir = os.path.abspath(
    '../../../../.config/JetBrains/PyCharm2022.1/scratches/user_interfaces/flask_web_ui/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mapper_registry = registry()
mapper_registry.mapped(Vehicle)
# start_mapping(mapper_registry)
engine = create_engine('sqlite:///' + os.path.join(basedir, 'data.sqlite'), echo=True)
Session = sessionmaker(bind=engine)
db = SQLAlchemy(app)
db.create_all()


@app.route('/')
def index():
    v = Vehicle(name="abc", gps_receiver_offset_x=3, gps_receiver_offset_y=5, gps_receiver_offset_z=7,
                turn_radius_left=2.1,
                turn_radius_right=2.3, wheelbase=3.0)
    print(v.id)
    db.session.add(v)
    db.session.commit()
    print(v.id)
    return f'a: {2}'


app.run()

print("ende")
