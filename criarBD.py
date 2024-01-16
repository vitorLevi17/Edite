from edite import database, app
from edite.models import Usuario, Foto

with app.app_context():
    database.create_all()