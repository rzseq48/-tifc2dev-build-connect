import pytest
from app import create_app
from app.extensions import db
from app.models import User, Ticket
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    app=create_app({"TESTING":True,"SQLALCHEMY_DATABASE_URI":"sqlite:///:memory:","JWT_SECRET_KEY":"test-secret-key-0123456789abcdef"})
    with app.app_context():
        db.create_all();u1=User(username="agent1",password_hash=generate_password_hash("Password123!"));u2=User(username="agent2",password_hash=generate_password_hash("Password123!"));db.session.add_all([u1,u2]);db.session.flush();db.session.add(Ticket(title="VPN",description="Cannot connect",priority="High",category="Network",status="New",created_by_id=u1.id,assigned_to_id=u2.id));db.session.commit()
    yield app

@pytest.fixture
def client(app): return app.test_client()

def token(client): return client.post("/api/auth/login",json={"username":"agent1","password":"Password123!"}).get_json()["access_token"]
def headers(client): return {"Authorization":f"Bearer {token(client)}"}

def test_get_tickets_returns_ticket_data(client): assert client.get("/api/tickets").status_code==200
def test_get_ticket_returns_requested_ticket(client): assert client.get("/api/tickets/1").get_json()["id"]==1
def test_ticket_response_contains_assigned_user(client): assert client.get("/api/tickets/1").get_json()["assigned_to"]["username"]=="agent2"
def test_create_ticket_returns_created_ticket(client):
 r=client.post("/api/tickets",headers=headers(client),json={"title":"Email","description":"Mailbox full","category":"Software","priority":"High"});assert r.status_code==201;assert r.get_json()["created_by"]["username"]=="agent1"
def test_created_ticket_persists_across_requests(client):
 r=client.post("/api/tickets",headers=headers(client),json={"title":"Email","description":"Mailbox full","category":"Software"});tid=r.get_json()["id"];assert client.get(f"/api/tickets/{tid}").status_code==200
def test_create_rejects_invalid_input(client): assert client.post("/api/tickets",headers=headers(client),json={"title":"","description":"x","category":"y"}).status_code==400
def test_authenticated_create_succeeds(client): assert client.post("/api/tickets",headers=headers(client),json={"title":"A","description":"B","category":"C"}).status_code==201
def test_unauthenticated_create_is_rejected(client): assert client.post("/api/tickets",json={"title":"A","description":"B","category":"C"}).status_code==401
def test_update_ticket_changes_supported_fields(client):
 r=client.patch("/api/tickets/1",headers=headers(client),json={"status":"Triaged"});assert r.status_code==200;assert r.get_json()["status"]=="Triaged"
def test_invalid_update_does_not_change_ticket(client,app):
 assert client.patch("/api/tickets/1",headers=headers(client),json={"status":"Unknown"}).status_code==400
 with app.app_context(): assert db.session.get(Ticket,1).status=="New"
def test_unauthenticated_update_is_rejected(client): assert client.patch("/api/tickets/1",json={"status":"Triaged"}).status_code==401
def test_delete_ticket_removes_ticket(client):
 assert client.delete("/api/tickets/1",headers=headers(client)).status_code==200;assert client.get("/api/tickets/1").status_code==404
def test_unauthenticated_delete_is_rejected(client): assert client.delete("/api/tickets/1").status_code==401
def test_missing_ticket_returns_not_found(client): assert client.patch("/api/tickets/999",headers=headers(client),json={"status":"Triaged"}).status_code==404
