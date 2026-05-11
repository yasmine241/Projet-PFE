from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import Transaction, Fraud
from app.services.fraud_detector import FraudDetector
from datetime import datetime

transactions_bp = Blueprint("transactions", __name__)

detector = FraudDetector()


# ======================
# GET ALL TRANSACTIONS
# ======================
@transactions_bp.route("/api/transactions", methods=["GET"])
@jwt_required()
def get_transactions():
    txs = Transaction.query.all()

    return jsonify([
        {
            "id": t.transaction_id,
            "compte_id": t.compte_id,
            "type": t.type_transaction,
            "montant": t.montant,
            "devise": t.devise,
            "pays_origine": t.pays_origine,
            "pays_destination": t.pays_destination,
            "statut": t.statut,
            "score_risque": t.score_risque,
            "date_transaction": str(t.date_transaction)
        }
        for t in txs
    ])


# ======================
# GET ONE TRANSACTION
# ======================
@transactions_bp.route("/api/transactions/<int:id>", methods=["GET"])
@jwt_required()
def get_transaction(id):
    t = Transaction.query.get(id)

    if not t:
        return jsonify({"message": "Transaction not found"}), 404

    return jsonify({
        "id": t.transaction_id,
        "compte_id": t.compte_id,
        "type": t.type_transaction,
        "montant": t.montant,
        "devise": t.devise,
        "pays_origine": t.pays_origine,
        "pays_destination": t.pays_destination,
        "statut": t.statut,
        "score_risque": t.score_risque,
        "date_transaction": str(t.date_transaction)
    })


# ======================
# CREATE TRANSACTION
# ======================
@transactions_bp.route("/api/transactions", methods=["POST"])
@jwt_required()
def create_transaction():
    data = request.get_json()

    transaction_data = {
        "montant": data["montant"],
        "pays_origine": data.get("pays_origine", ""),
        "pays_destination": data.get("pays_destination", "")
    }

    result = detector.predict(transaction_data)

    score = result["score"]
    is_fraud = result["fraud"]

    status = "EN_ANALYSE" if is_fraud else "VALIDEE"

    new_tx = Transaction(
        compte_id=data["compte_id"],
        type_transaction=data["type_transaction"],
        montant=data["montant"],
        devise=data.get("devise", "EUR"),
        pays_origine=data.get("pays_origine", ""),
        pays_destination=data.get("pays_destination", ""),
        date_transaction=datetime.utcnow(),
        statut=status,
        score_risque=score
    )

    db.session.add(new_tx)
    db.session.commit()

    # Si fraude détectée → créer une alerte dans la table fraud
    if is_fraud:
        niveau = "ELEVE" if score >= 0.9 else "MOYEN"
        new_fraud = Fraud(
            transaction_id=new_tx.transaction_id,
            type_fraude="AUTOMATIQUE",
            niveau_risque=niveau,
            score_ml=score,
            date_detection=datetime.utcnow(),
            statut_analyse="EN_ATTENTE"
        )
        db.session.add(new_fraud)
        db.session.commit()

    return jsonify({
        "message": "Transaction created",
        "score_risque": score,
        "fraud": is_fraud,
        "status": status
    }), 201