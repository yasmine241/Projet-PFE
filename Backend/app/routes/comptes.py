from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import Compte

comptes_bp = Blueprint("comptes", __name__)


# ======================
# GET ALL COMPTES
# ======================
@comptes_bp.route("/comptes", methods=["GET"])
@jwt_required()
def get_comptes():
    comptes = Compte.query.all()

    return jsonify([
        {
            "id": c.compte_id,
            "client_id": c.client_id,
            "numero_compte": c.numero_compte,
            "type_compte": c.type_compte,
            "solde": c.solde,
            "devise": c.devise,
            "statut": c.statut
        }
        for c in comptes
    ])


# ======================
# GET ONE COMPTE
# ======================
@comptes_bp.route("/comptes/<int:id>", methods=["GET"])
@jwt_required()
def get_compte(id):
    compte = Compte.query.get(id)

    if not compte:
        return jsonify({"message": "Compte not found"}), 404

    return jsonify({
        "id": compte.compte_id,
        "client_id": compte.client_id,
        "numero_compte": compte.numero_compte,
        "type_compte": compte.type_compte,
        "solde": compte.solde,
        "devise": compte.devise,
        "date_ouverture": str(compte.date_ouverture),
        "statut": compte.statut
    })


# ======================
# CREATE COMPTE
# ======================
@comptes_bp.route("/comptes", methods=["POST"])
@jwt_required()
def create_compte():
    data = request.get_json()

    new_compte = Compte(
        client_id=data["client_id"],
        numero_compte=data["numero_compte"],
        type_compte=data.get("type_compte", "COURANT"),
        solde=data.get("solde", 0.0),
        devise=data.get("devise", "EUR"),
        statut=data.get("statut", "ACTIF")
    )

    db.session.add(new_compte)
    db.session.commit()

    return jsonify({"message": "Compte created successfully"}), 201


# ======================
# UPDATE COMPTE
# ======================
@comptes_bp.route("/comptes/<int:id>", methods=["PUT"])
@jwt_required()
def update_compte(id):
    compte = Compte.query.get(id)

    if not compte:
        return jsonify({"message": "Compte not found"}), 404

    data = request.get_json()

    compte.solde = data.get("solde", compte.solde)
    compte.statut = data.get("statut", compte.statut)
    compte.devise = data.get("devise", compte.devise)

    db.session.commit()

    return jsonify({"message": "Compte updated successfully"})


# ======================
# DELETE COMPTE
# ======================
@comptes_bp.route("/comptes/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_compte(id):
    compte = Compte.query.get(id)

    if not compte:
        return jsonify({"message": "Compte not found"}), 404

    db.session.delete(compte)
    db.session.commit()

    return jsonify({"message": "Compte deleted successfully"})