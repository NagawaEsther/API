from authors_app import db
from datetime import datetime

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    origin = db.Column(db.String(100))
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='companies')
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, name, origin, description, user_id):
        super(Company, self).__init__()
        #self.id = id
        self.name = name
        self.origin = origin
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return f"<Company(name='{self.name}', origin='{self.origin}')>"
