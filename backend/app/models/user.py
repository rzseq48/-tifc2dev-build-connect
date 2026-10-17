from ..extensions import db
class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(80), unique=True, nullable=False)
    password_hash=db.Column(db.String(255), nullable=False)
    created_tickets=db.relationship("Ticket", foreign_keys="Ticket.created_by_id", back_populates="created_by")
    assigned_tickets=db.relationship("Ticket", foreign_keys="Ticket.assigned_to_id", back_populates="assigned_to")
    def to_dict(self): return {"id":self.id,"username":self.username}
