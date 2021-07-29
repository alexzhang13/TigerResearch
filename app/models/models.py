from app import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "user"
    netid = db.Column(db.String(64), primary_key=True)
    id = db.Column(db.String(64))
    email = db.Column(db.String(64))

    # prof_likes = db.relationship('ProfLikes', backref=db.backref('user', lazy='joined'),
    #                             lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Professor (db.Model):
    __tablename__ = "profdb"

    name = db.Column(db.String(64), index=True, default="")
    netid = db.Column(db.String(64), primary_key=True)
    rating = db.Column(db.Integer(), default=0)
    department = db.Column(db.String(64), default="")
    type = db.Column(db.String(64), default="")
    email = db.Column(db.String(120), default="")
    website = db.Column(db.String(120), default="")
    keywords = db.Column(db.String(1024), default="")
    research_interests = db.Column(db.String(1024), default="")
    room = db.Column(db.String(64), default="")
    advising = db.Column(db.Boolean, default=True)
    likes = db.Column(db.Integer, default=0)
    # user_likes = db.relationship('PostLikes', backref=db.backref('post', lazy='joined'),
    #                             lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return '<Professor {}>'.format(self.netid)
    
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


# likes_table = db.Table('likes',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.netid')),
#     db.Column('prof_id', db.Integer, db.ForeignKey('prof.netid'))
# )

@login.user_loader
def load_user(netid):
    return User.query.filter_by(id=netid).first()