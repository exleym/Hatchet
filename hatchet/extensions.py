from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from hatchet.autoswag import AutoSwag

db = SQLAlchemy()
cors = CORS()
swag = AutoSwag()

