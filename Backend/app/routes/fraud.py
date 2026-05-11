from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import Fraud, Transaction
from datetime import datetime

fraud_bp = Blueprint("fraud", __name__)


# ======================
# GET FRAUDES EN ATTENTE  ← placée AVANT /<int:id> pour éviter le conflit de route
# ======================
@fraud_bp.route("/fraud/pending", methods=["GET"])
@jwt_required()
def get_pending_frauds():
    frauds = Fraud.query.filter_by(statut_analyse="EN_ATTENTE").all()

    return jsonify([
        {
            "id": f.fraud_id,
            "transaction_id": f.transaction_id,
            "type_fraude": f.type_fraude,
            "niveau_risque": f.niveau_risque,
            "score_ml": f.score_ml,
            "date_detection": str(f.date_detection)
        }
        for f in frauds
    ])


# ======================
# GET ALL FRAUDES
# ======================
@fraud_bp.route("/fraud", methods=["GET"])
@jwt_required()
def get_frauds():
    frauds = Fraud.query.all()

    return jsonify([
        {
            "id": f.fraud_id,
            "transaction_id": f.transaction_id,
            "type_fraude": f.type_fraude,
            "niveau_risque": f.niveau_risque,
            "score_ml": f.score_ml,
            "date_detection": str(f.date_detection),
            "statut_analyse": f.statut_analyse,
            "analyste_id": f.analyste_id,
            "commentaire": f.commentaire
        }
        for f in frauds
    ])


# ======================
# GET ONE FRAUDE
# ======================
@fraud_bp.route("/fraud/<int:id>", methods=["GET"])
@jwt_required()
def get_fraud(id):
    fraud = Fraud.query.get(id)

    if not fraud:
        return jsonify({"message": "Fraud record not found"}), 404

    return jsonify({
        "id": fraud.fraud_id,
        "transaction_id": fraud.transaction_id,
        "type_fraude": fraud.type_fraude,
        "niveau_risque": fraud.niveau_risque,
        "score_ml": fraud.score_ml,
        "date_detection": str(fraud.date_detection),
        "statut_analyse": fraud.statut_analyse,
        "analyste_id": fraud.analyste_id,
        "commentaire": fraud.commentaire
    })


# ======================
# VALIDER UNE FRAUDE
# ======================
@fraud_bp.route("/fraud/<int:id>/valider", methods=["PUT"])
@jwt_required()
def valider_fraud(id):
    fraud = Fraud.query.get(id)

    if not fraud:
        return jsonify({"message": "Fraud record not found"}), 404

    data = request.get_json()

    fraud.statut_analyse = "VALIDEE"
    fraud.analyste_id    = data.get("analyste_id", fraud.analyste_id)
    fraud.commentaire    = data.get("commentaire", fraud.commentaire)

    transaction = Transaction.query.get(fraud.transaction_id)
    if transaction:
        transaction.statut = "REJETEE"

    db.session.commit()

    return jsonify({"message": "Fraude validée, transaction rejetée"})


# ======================
# REJETER UNE ALERTE (faux positif)
# ======================
@fraud_bp.route("/fraud/<int:id>/rejeter", methods=["PUT"])
@jwt_required()
def rejeter_fraud(id):
    fraud = Fraud.query.get(id)

    if not fraud:
        return jsonify({"message": "Fraud record not found"}), 404

    data = request.get_json()

    fraud.statut_analyse = "FAUX_POSITIF"
    fraud.analyste_id    = data.get("analyste_id", fraud.analyste_id)
    fraud.commentaire    = data.get("commentaire", fraud.commentaire)

    transaction = Transaction.query.get(fraud.transaction_id)
    if transaction:
        transaction.statut = "VALIDEE"

    db.session.commit()

    return jsonify({"message": "Alerte rejetée, transaction validée (faux positif)"})
