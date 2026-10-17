from flask import Blueprint, jsonify
from ..extensions import db
from ..models import Ticket

tickets_bp=Blueprint("tickets", __name__)

@tickets_bp.route("", methods=["GET"])
def list_tickets():
    return jsonify([t.to_dict() for t in Ticket.query.order_by(Ticket.id).all()]), 200

@tickets_bp.route("/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    ticket=db.session.get(Ticket,ticket_id)
    if not ticket:return jsonify({"error":"Ticket not found."}),404
    return jsonify(ticket.to_dict()),200

@tickets_bp.route("", methods=["POST"])
def create_ticket():
    # TODO LAB 3: Implement and protect this route.
    return jsonify({"error":"Not implemented."}),501

@tickets_bp.route("/<int:ticket_id>", methods=["PATCH"])
def update_ticket(ticket_id):
    # TODO LAB 3: Implement and protect this route.
    return jsonify({"error":"Not implemented."}),501

@tickets_bp.route("/<int:ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id):
    # TODO LAB 3: Implement and protect this route.
    return jsonify({"error":"Not implemented."}),501
