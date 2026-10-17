from flask import Flask
from flask_cors import CORS
from .extensions import db, jwt


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///helpdesk.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY="development-only-secret-key-0123456789",
    )
    if test_config:
        app.config.update(test_config)
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    from .models import User, Ticket, Comment
    from .routes.auth_routes import auth_bp
    from .routes.ticket_routes import tickets_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(tickets_bp, url_prefix="/api/tickets")
    with app.app_context():
        db.create_all()
        if not app.config.get("TESTING") and User.query.count() == 0:
            seed_data()
    return app


def seed_data():
    from werkzeug.security import generate_password_hash
    from .models import User, Ticket
    u1=User(username="agent1", password_hash=generate_password_hash("Password123!"))
    u2=User(username="agent2", password_hash=generate_password_hash("Password123!"))
    db.session.add_all([u1,u2]); db.session.flush()
    db.session.add_all([
        Ticket(title="VPN access", description="Remote user cannot connect.", priority="High", category="Network", status="New", created_by_id=u1.id, assigned_to_id=u2.id),
        Ticket(title="Printer issue", description="Third-floor printer is offline.", priority="Medium", category="Hardware", status="Triaged", created_by_id=u2.id),
    ])
    db.session.commit()
