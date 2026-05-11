import os

class Config:

    # ======================
    # GENERAL SETTINGS
    # ======================
    SECRET_KEY = os.environ.get("SECRET_KEY", "sg_securebank_secret_key")

    # ======================
    # JWT CONFIG  (une seule clé)
    # ======================
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "sg_securebank_jwt_secret")

    # ======================
    # ORACLE DATABASE
    # ======================
    ORACLE_USER     = os.environ.get("ORACLE_USER", "system")
    ORACLE_PASSWORD = os.environ.get("ORACLE_PASSWORD", "2002")
    ORACLE_DSN      = os.environ.get("ORACLE_DSN", "localhost:1521/XE")

    SQLALCHEMY_DATABASE_URI = (
        f"oracle+oracledb://{os.environ.get('ORACLE_USER','system')}:"
        f"{os.environ.get('ORACLE_PASSWORD','2002')}@"
        f"{os.environ.get('ORACLE_DSN','localhost:1521/XE')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ======================
    # ML CONFIG
    # ======================
    MODEL_PATH       = "app/services/fraud_model.pkl"
    THRESHOLD_FRAUD  = 0.7
