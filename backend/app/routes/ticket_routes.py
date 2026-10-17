from flask import Blueprint, jsonify
from ..extensions import db
from ..models import Ticket
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import SQLAlchemyError

from ..models import User
from ..services.ticket_service import (EDITABLE_FIELDS, clean_required_text, validate_ticket_payload
)
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
@jwt_required()
def create_ticket():
    data = request.get_json(silent=True)
    error = validate_ticket_payload(data)

    if error:
        return jsonify({"error": error}), 400

    assigned_user = None
    if data.get("assigned_to_id") is not None:
        assigned_user = db.session.get(User, data["assigned_to_id"])
        if assigned_user is None:
            return jsonify({"error": "Assigned user not found."}), 400

    ticket = Ticket(
        title=clean_required_text(data["title"]),
        description=clean_required_text(data["description"]),
        priority=data.get("priority", "Medium"),
        category=clean_required_text(data["category"]),
        status=data.get("status", "New"),
        created_by_id=int(get_jwt_identity()),
        assigned_to_id=assigned_user.id if assigned_user else None,
    )

    try:
        db.session.add(ticket)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Ticket could not be created."}), 500

    return jsonify(ticket.to_dict()), 201

@tickets_bp.route("/<int:ticket_id>", methods=["PATCH"])
@jwt_required()
def update_ticket(ticket_id):
    ticket = db.session.get(Ticket, ticket_id)
    if ticket is None:
        return jsonify({"error": "Ticket not found."}), 404

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not data:
        return jsonify({"error": "A non-empty JSON request body is required."}), 400

    unsupported = set(data) - EDITABLE_FIELDS
    if unsupported:
        return jsonify(
            {"error": f"Unsupported fields: {', '.join(sorted(unsupported))}."}
        ), 400

    error = validate_ticket_payload(data, partial=True)
    if error:
        return jsonify({"error": error}), 400

    if (
        "assigned_to_id" in data
        and data["assigned_to_id"] is not None
        and db.session.get(User, data["assigned_to_id"]) is None
    ):
        return jsonify({"error": "Assigned user not found."}), 400

    for field, value in data.items():
        if field in {"title", "description", "category"}:
            value = clean_required_text(value)
        setattr(ticket, field, value)

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Ticket could not be updated."}), 500

    return jsonify(ticket.to_dict()), 200

@tickets_bp.route("/<int:ticket_id>", methods=["DELETE"])
@jwt_required()
def delete_ticket(ticket_id):
    ticket = db.session.get(Ticket, ticket_id)
    if ticket is None:
        return jsonify({"error": "Ticket not found."}), 404

    try:
        db.session.delete(ticket)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Ticket could not be deleted."}), 500

    return jsonify({"message": "Ticket deleted.", "id": ticket_id}), 200