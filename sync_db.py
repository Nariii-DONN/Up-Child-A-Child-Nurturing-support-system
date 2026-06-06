from flask_app import app, db, Fund
from sqlalchemy import text

with app.app_context():
    print("Creating tables...")
    db.create_all()
    
    print("Checking for default fund record...")
    fund = Fund.query.first()
    if not fund:
        print("Inserting default fund record...")
        new_fund = Fund(total_available=0, total_allocated=0, total_distributed=0)
        db.session.add(new_fund)
        db.session.commit()
        print("Done.")
    else:
        print("Fund record already exists.")
    
    print("Database sync complete.")
