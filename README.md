# 🛡️ Sovereign Auth Gateway

> A decoupled, zero-bloat Authentication & Authorization microservice designed for high-privacy healthcare networks and academic research environments.

## 🎯 Architecture Overview

The Sovereign Auth Gateway acts as a centralized "Identity Vault" for microservice architectures. It offloads the heavy lifting of user registration, cryptographic password hashing, and token generation from core application logic. 

This project was built specifically with the data privacy and security requirements of **KathiraveluLab (Beehive)** in mind, prioritizing local hosting and zero third-party cloud dependencies to ensure strict healthcare data compliance.

### ✨ Core Features
* **Zero Third-Party Risk:** No external trackers or cloud auth providers (e.g., Clerk, Google). 100% locally hosted.
* **Stateless Authentication:** Issues secure JSON Web Tokens (JWT) with distinct Access and Refresh lifecycles.
* **Role-Based Access Control (RBAC):** Token payloads include cryptographic proof of user roles (e.g., `student`, `researcher`, `admin`) for seamless multi-tenant authorization.
* **Cryptographic Security:** Passwords are mathematically hashed via `pbkdf2:sha256` prior to database insertion. 
* **Anti-Bloat Deployment:** Fully containerized. The entire system boots via a single Docker command, enabling effortless deployment by hospital IT administrators.

---

## 🏗️ Tech Stack

* **Framework:** Python 3.10 / Flask (Application Factory Pattern)
* **Database:** MongoDB (Motor/PyMongo)
* **Security:** PyJWT, Werkzeug Security
* **Infrastructure:** Docker, Docker Compose

---

## 🚀 Quick Start (Docker)

To deploy the Gateway and its isolated MongoDB database locally, you only need Docker installed.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nitinkumar2024/sovereign-auth-gateway.git
   cd sovereign-auth-gateway



2. **Set up the Environment Vault:**
Create a `.env` file in the root directory:

    ```env
    MONGO_URI=mongodb://mongodb:27017/beehive_auth
    SECRET_KEY=your-highly-secure-cryptographic-key

    ```


3. **Ignite the Microservice:**
    ```bash
    docker-compose up -build -d

    ```


*The Gateway is now securely running and listening on `http://localhost:5000`.*

---

## 🔌 API Endpoints

### 1. Identity Provisioning

* **`POST /api/auth/signup`**
* **Payload:** `{"email": "user@example.com", "password": "secure123"}`
* **Action:** Hashes password, provisions a new identity in MongoDB, and assigns a default Role.



### 2. Authentication

* **`POST /api/auth/login`**
* **Payload:** `{"email": "user@example.com", "password": "secure123"}`
* **Action:** Verifies credentials and issues a short-lived `access_token` and long-lived `refresh_token`.



### 3. The Security Intercept (For S2S Communication)

* **`GET /api/gateway/validate`**
* **Headers:** `Authorization: Bearer <access_token>`
* **Action:** Other microservices (like a FastAPI AI backend or the main Beehive UI) ping this route to verify a user's token. Returns `200 OK` with user roles, or `401 Unauthorized` if the cryptographic signature is invalid or expired.



---

## 🤝 Service-to-Service Integration Example (Python/FastAPI)

Any external project can easily plug into this Gateway. Here is how an external backend validates a user before serving sensitive data:

```python
import requests

def verify_token_with_gateway(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("http://localhost:5000/api/gateway/validate", headers=headers)
    
    if response.status_code == 200:
        return response.json() # Returns {"user_id": "...", "role": "..."}
    else:
        raise Exception("Access Denied by Sovereign Gateway")

```