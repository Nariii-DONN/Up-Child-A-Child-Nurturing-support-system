from flask_app import app, db, AdminUser
from werkzeug.security import generate_password_hash

# Use Flask app context so database works
with app.app_context():
    admin = AdminUser.query.filter_by(email='admin@upchild.com').first()

    if admin:
        admin.password_hash = generate_password_hash('admin123')
        db.session.commit()
        print("✅ Admin password updated successfully!")
    else:
        print("❌ Admin not found, creating a new one...")
        new_admin = AdminUser(
            username='admin',
            email='admin@upchild.com',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(new_admin)
        db.session.commit()
        print("✅ New admin created successfully!")
