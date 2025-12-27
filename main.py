from fastapi import FastAPI
from pydantic import BaseModel
from email_validator import validate_email, EmailNotValidError
import socket

app = FastAPI(
    title="TrustEmail API",
    description="API professionnelle de vérification d'adresses email",
    version="1.0.0"
)

class EmailRequest(BaseModel):
    email: str

@app.get("/")
def root():
    return {"message": "TrustEmail API is running"}

@app.post("/verify-email")
def verify_email(data: EmailRequest):
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