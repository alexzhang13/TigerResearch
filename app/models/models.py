from app import db
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSVECTOR
from werkzeug.security import generate_password_hash, check_password_hash

class TSVector(sa.types.TypeDecorator):
    impl = TSVECTOR

def to_tsvector_ix(*columns):
    cols = " || ' ' || ".join(columns)
    return "to_tsvector('english', " + cols + ")"

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
    __tablename__ = "profdb"

    name = db.Column(db.String(64), index=True, default="")
    netid = db.Column(db.String(64), primary_key=True)
    department = db.Column(db.String(64), default="")
    type = db.Column(db.String(64), default="")
    email = db.Column(db.String(120), default="")
    website = db.Column(db.String(120), default="")
    keywords = db.Column(db.String(1024), default="")
    research_interests = db.Column(db.String(1024), default="")
    room = db.Column(db.String(64), default="")
    advising = db.Column(db.Boolean, default=True)

    __ts_vector__ = db.Column(TSVector(),db.Computed(
        to_tsvector_ix('name', 'department', 'email', 'keywords', 'research_interests'),
         persisted=True))

    __table_args__ = (
        sa.Index('ix_profs_tsv',
          __ts_vector__, 
          postgresql_using='gin'),
    )

    def __repr__(self):
        return '<Professor {}>'.format(self.name)
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'netid': self.netid,
           'name': self.name,
           'type': self.type,
           'department': self.department,
           'email': self.email,
           'website': self.website,
           'keywords': self.keywords,
           'research_interests': self.research_interests,
           'room': self.room,
           'advising': self.advising
       }