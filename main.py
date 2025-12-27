from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from email_validator import validate_email, EmailNotValidError
import socket

# 🔐 Clé API (simple pour l’instant)
API_KEY = "trustemail-123456"

# 🔐 Vérification de la clé API
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key"
        )

# 🚀 Application FastAPI
app = FastAPI(
    title="TrustEmail API",
    description="API professionnelle de vérification d'adresses email développée par Master Bronz Digital",
    version="1.0.0"
)

# 📩 Modèle de requête
class EmailRequest(BaseModel):
    email: str

# 🔍 Route de test
@app.get("/")
def root():
    return {"message": "TrustEmail API is running"}

# 🔐 Endpoint protégé par API Key
@app.post("/verify-email")
def verify_email(
    data: EmailRequest,
    api_key: str = Depends(verify_api_key)
):
    result = {
        "email": data.email,
        "is_valid": False,
        "domain_exists": False
    }

    try:
        validate_email(data.email)
        result["is_valid"] = True

        domain = data.email.split("@")[1]
        socket.gethostbyname(domain)
        result["domain_exists"] = True

    except EmailNotValidError:
        pass
    except socket.gaierror:
        pass

    return result