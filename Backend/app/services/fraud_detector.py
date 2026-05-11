import random

class FraudDetector:

    def predict(self, transaction):
        """
        Simule un modèle ML (remplacé plus tard par Random Forest)
        """

        score = 0

        # montant élevé
        if transaction["montant"] > 5000:
            score += 0.4

        # très gros montant
        if transaction["montant"] > 10000:
            score += 0.3

        # pays différent
        if transaction.get("pays_origine") != transaction.get("pays_destination"):
            score += 0.3

        # bruit ML simulé
        score += random.uniform(0, 0.1)

        score = min(score, 1)

        is_fraud = score > 0.7

        return {
            "score": round(score, 2),
            "fraud": is_fraud
        }
    