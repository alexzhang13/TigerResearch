from app import db, login
from flask_login import UserMixin


class ProfLike(db.Model):
    __tablename__ = 'prof_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.netid'))
    prof_id = db.Column(db.String(64), db.ForeignKey('prof.netid'))

class User(UserMixin, db.Model):
    __tablename__ = "user"
    netid = db.Column(db.String(64), primary_key=True)
    id = db.Column(db.String(64))
    email = db.Column(db.String(64))

    likes = db.relationship('ProfLike', foreign_keys='ProfLike.user_id', 
        backref='user', lazy='dynamic')

    def like_prof(self, prof):
        if not self.has_liked_prof(prof):
            like = ProfLike(user_id=self.netid, prof_id=prof.netid)
            db.session.add(like)

    def unlike_prof(self, prof):
        if self.has_liked_prof(prof):
            ProfLike.query.filter_by(
                user_id=self.netid,
                prof_id=prof.netid).delete()

    def has_liked_prof(self, prof_netid):
        return ProfLike.query.filter(
            ProfLike.user_id == self.netid,
            ProfLike.prof_id == prof_netid).count() > 0

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Professor (db.Model):
    __tablename__ = "prof"

    name = db.Column(db.String(64), index=True, default="")
    netid = db.Column(db.String(64), primary_key=True)
    department = db.Column(db.String(64), default="")
    department_full = db.Column(db.String(64), default="")
    department_color = db.Column(db.String(16), default="")
    type = db.Column(db.String(64), default="")
    email = db.Column(db.String(120), default="")
    website = db.Column(db.String(120), default="")
    picture = db.Column(db.String(256), default="")
    keywords = db.Column(db.String(256), default="")
    fingerprints = db.Column(db.PickleType(), default="")
    projects = db.Column(db.PickleType(), default="")
    publications = db.Column(db.PickleType(), default="")
    courses = db.Column(db.PickleType(), default="")
    faculty = db.Column(db.PickleType(), default="")
    advising = db.Column(db.Boolean, default=True)
    citations = db.Column(db.Integer(), default=0)
    hindex = db.Column(db.Integer(), default=0)
    rating = db.Column(db.Integer(), default=0)

    likes = db.relationship('ProfLike', backref='prof', lazy='dynamic')

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
           'department_full': self.department_full,
           'department_color': self.department_color,
           'email': self.email,
           'website': self.website,
           'keywords': self.keywords,
           'projects': self.projects,
           'publications': self.publications,
           'citations': self.citations,
           'hindex': self.hindex,
           'advising': self.advising,
           'picture': self.picture,
           'faculty': self.faculty,
           'fingerprints': self.fingerprints,
           'courses': self.courses,
           'likes': self.likes.count()
       }
       
    

@login.user_loader
def load_user(netid):
    return User.query.filter_by(id=netid).first()