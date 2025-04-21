# Import all the models, so that Base knows about them before being
# imported by Alembic or used directly.
from app.db.base_class import Base
from app.models.user import User
from app.models.route import Route
from app.models.point import Point
from app.models.checklist import Checklist
from app.models.item import Item
from app.models.place import Place 