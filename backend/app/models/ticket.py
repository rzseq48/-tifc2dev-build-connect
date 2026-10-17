from datetime import datetime, timezone
from ..extensions import db
class Ticket(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(120), nullable=False)
    description=db.Column(db.Text, nullable=False)
    priority=db.Column(db.String(20), nullable=False, default="Medium")
    category=db.Column(db.String(50), nullable=False)
    status=db.Column(db.String(30), nullable=False, default="New")
    created_by_id=db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    assigned_to_id=db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    created_at=db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), nullable=False)
    updated_at=db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), onupdate=lambda:datetime.now(timezone.utc), nullable=False)
    created_by=db.relationship("User", foreign_keys=[created_by_id], back_populates="created_tickets")
    assigned_to=db.relationship("User", foreign_keys=[assigned_to_id], back_populates="assigned_tickets")
    def to_dict(self):
        return {"id":self.id,"title":self.title,"description":self.description,"priority":self.priority,"category":self.category,"status":self.status,"created_by":self.created_by.to_dict() if self.created_by else None,"assigned_to":self.assigned_to.to_dict() if self.assigned_to else None,"created_at":self.created_at.isoformat(),"updated_at":self.updated_at.isoformat()}
