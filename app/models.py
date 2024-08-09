from app import db

class UserSelection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    selected_fields = db.Column(db.String(200))

def get_user_selections():
    return UserSelection.query.all()
