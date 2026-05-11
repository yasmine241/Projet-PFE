from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import Client

clients_bp = Blueprint("clients", __name__)


# ======================
# CREATE CLIENT
# ======================
@clients_bp.route("/api/clients", methods=["POST"])
@jwt_required()
def create_client():
    data = request.get_json()

    new_client = Client(
        nom=data["nom"],
        prenom=data["prenom"],
        email=data["email"],
        mot_de_passe=data["mot_de_passe"],
        telephone=data.get("telephone"),
        date_naissance=data["date_naissance"],
        adresse=data.get("adresse"),
        pays=data.get("pays", "France"),
        statut="ACTIF"
    )

    db.session.add(new_client)
    db.session.commit()

    return jsonify({"message": "Client created successfully"}), 201


# ======================
# GET ALL CLIENTS
# ======================
@clients_bp.route("/api/clients", methods=["GET"])
@jwt_required()
def get_clients():
    clients = Client.query.all()

    result = []
    for c in clients:
        result.append({
            "id": c.client_id,
            "nom": c.nom,
            "prenom": c.prenom,
            "email": c.email,
            "pays": c.pays,
            "statut": c.statut
        })

    return jsonify(result)


# ======================
# GET ONE CLIENT
# ======================
@clients_bp.route("/api/clients/<int:id>", methods=["GET"])
@jwt_required()
def get_client(id):
    client = Client.query.get(id)

    if not client:
        return jsonify({"message": "Client not found"}), 404

    return jsonify({
        "id": client.client_id,
        "nom": client.nom,
        "prenom": client.prenom,
        "email": client.email,
        "telephone": client.telephone,
        "pays": client.pays,
        "statut": client.statut
    })


# ======================
# UPDATE CLIENT
# ======================
@clients_bp.route("/api/clients/<int:id>", methods=["PUT"])
@jwt_required()
def update_client(id):
    client = Client.query.get(id)

    if not client:
        return jsonify({"message": "Client not found"}), 404

    data = request.get_json()

    client.nom = data.get("nom", client.nom)
    client.prenom = data.get("prenom", client.prenom)
    client.telephone = data.get("telephone", client.telephone)
    client.adresse = data.get("adresse", client.adresse)
    client.pays = data.get("pays", client.pays)
    client.statut = data.get("statut", client.statut)

    db.session.commit()

    return jsonify({"message": "Client updated successfully"})


# ======================
# DELETE CLIENT
# ======================
@clients_bp.route("/api/clients/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_client(id):
    client = Client.query.get(id)

    if not client:
        return jsonify({"message": "Client not found"}), 404

    db.session.delete(client)
    db.session.commit()

    return jsonify({"message": "Client deleted successfully"})