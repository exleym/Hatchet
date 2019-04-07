from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from hatchet.autoswag import AutoSwag

db = SQLAlchemy()
cors = CORS()
ma = Marshmallow()
swag = AutoSwag()

