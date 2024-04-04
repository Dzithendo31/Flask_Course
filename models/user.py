import uuid

#Relative Import ..2Folders Up, .1Folder up
#from extensions import db

#absoulut from the base where is the File
from extensions import db
from flask_login import UserMixin
class User(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(50), primary_key=True,default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(100))
    real_name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    # JSON - Keys
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "real_name": self.real_name,
            "password": self.password
        }
    def get_id(self):
        return self.id
