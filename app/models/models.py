from app import db
from app.models.search import TSVector
from werkzeug.security import generate_password_hash, check_password_hash

def to_tsvector_ix(*columns):
    cols = " || ' ' || ".join(columns)
    return "to_tsvector('english', " + cols

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Professor (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    department = db.Column(db.String(64))
    email = db.Column(db.String(120))
    website = db.Column(db.String(120))
    keywords = db.Column(db.String(120))
    room = db.Column(db.String(64))
    advising = db.Column(db.Boolean, default=True)

    __ts_vector__ = db.Column(TSVector(),db.Computed(
         to_tsvector_ix('name', 'department', 'email', 'keywords'),
         persisted=True))
         
    __table_args__ = (db.Index('ix_profs___ts_vector__',
          __ts_vector__, postgresql_using='gin'),)

    def __repr__(self):
        return '<Professor {}>'.format(self.name)
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id': self.id,
           'name': self.name,
           'department': self.department,
           'email': self.email,
           'website': self.website,
           'keywords': self.keywords,
           'room': self.room,
           'advising': self.advising
       }