from run import db
from run import Role, User

db.drop_all()
db.create_all()

admin_role = Role(name='Admin')

user_john = User(username='john', role=admin_role)

db.session.add(admin_role)

db.session.commit()
