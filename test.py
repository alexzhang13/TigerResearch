from app import db
from app.models.models import Professor
import csv

db.drop_all()
db.create_all()

with open('db2.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['advising'] == "N":
            advising = False
        else:
            advising = True
        
        p = Professor(id=row['id'], name=row['name'], department=row['department'], 
        email=row['email'], website=row['website'], keywords=row['keywords'], 
        room=row['room'], advising=advising)

        db.session.add(p)
    db.session.commit()