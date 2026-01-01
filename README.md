# Contacts API Service 📞

A robust RESTful API for managing contacts, built with **Python (FastAPI)**.
The project implements **Clean Architecture** principles and the **Repository Pattern**, allowing for easy switching between different database implementations (MongoDB, SQL, etc.).

## 🚀 Features

* **CRUD Operations**: Create, Read, Update, and Delete contacts.
* **Architecture**: Clean separation of concerns (Routes -> Services -> Manager -> Repository).
* **Polymorphism**: Supports multiple database backends via `ldatabase.py` interface.
* **Containerized**: Fully Dockerized with Kubernetes support.
* **Configurable**: Environment-based configuration.

---

## 📂 Project Structure

Based on the actual project layout:

```text
.
├── app/
│   ├── db/                     # Database Layer
│   │   ├── mongo_repository/   # MongoDB implementation
│   │   ├── sql_repository/     # SQL implementation structure
│   │   ├── __init__.py
│   │   ├── exceptions.py       # Custom DB exceptions
│   │   ├── factory.py          # Pattern: Creates the correct DB connector
│   │   ├── ldatabase.py        # Interface (Abstract Base Class) for DBs
│   │   └── manager.py          # Database Manager (Facade)
│   ├── models/                 # Pydantic Data Models
│   │   ├── contact.py
│   │   └── types.py
│   ├── routes/                 # API Endpoints (Controllers)
│   ├── services/               # Business Logic Layer
│   ├── config.json             # Configuration file
│   ├── Dockerfile              # Docker build instructions
│   ├── main.py                 # App Entry Point
│   └── requirements.txt        # Python dependencies
├── k8s/                        # Kubernetes Deployment Files
│   ├── api-pod.yaml
│   ├── api-service.yaml
│   ├── mongodb-pod.yaml
│   └── mongodb-service.yaml
└── .venv/                      # Virtual Environment
```

---

## 🛠️ Getting Started

### Prerequisites

* Python 3.11+
* Docker & Docker Hub account
* Minikube & Kubectl (for Kubernetes)

### 1. Running Locally (Python)

Ensure you have a local instance of MongoDB running.

```bash
# 1. Navigate to the app directory (or root)
cd week10_contacts

# 2. Install dependencies
pip install -r app/requirements.txt

# 3. Run the server (Running as a module is recommended to handle imports)
# Make sure your PYTHONPATH is set correctly, or run from the root:
python -m app.main
```
The API will be available at `http://localhost:8000`.

---

### 2. Running with Docker 🐳

Since the `Dockerfile` is inside the `app` folder, pay attention to the build context.

**Step 1: Build the Image**
```bash
# Run this from the folder containing 'app'
docker build -t <your-docker-id>/contacts-api:v1 -f app/Dockerfile app/
```

**Step 2: Run the API**
```bash
docker run -d --name api-container --network contacts-net \
  -e MONGO_HOST=mongo-container \
  -p 8000:8000 \
  <your-docker-id>/contacts-api:v1
```

---

### 3. Running on Kubernetes (Minikube) ☸️

```bash
# 1. Start Minikube
minikube start

# 2. Apply Database Config
kubectl apply -f k8s/mongodb-pod.yaml
kubectl apply -f k8s/mongodb-service.yaml

# 3. Apply API Config
kubectl apply -f k8s/api-service.yaml
kubectl apply -f k8s/api-pod.yaml

# 4. Access the Service
minikube service api-service
```

---

## 🔌 How to Add/Switch Databases

The project uses a **Factory Pattern** located in `app/db/factory.py`.

### To Add a New Database (e.g., PostgreSQL):

1.  **Implement the Interface:**
    Go to `app/db/sql_repository/` and create a class that implements the methods defined in `app/db/ldatabase.py`.

2.  **Update the Factory:**
    Modify `app/db/factory.py` to recognize the new database type.

    ```python
    # Example logic inside factory.py
    def get_db_manager(config):
        if config.type == "mongo":
            return create_mongo_manager(config)
        elif config.type == "sql":
             # Add your new SQL manager creation here
            return create_sql_manager(config)
    ```

3.  **Update Config:**
    Change your `config.json` or Environment Variables to set the active DB type.

---

## 📝 API Endpoints

* `GET /contacts` - Retrieve all contacts.
* `GET /contacts/{id}` - Retrieve a specific contact.
* `POST /contacts` - Create a new contact.
* `PUT /contacts/{id}` - Update a contact.
* `DELETE /contacts/{id}` - Delete a contact.

---

## 👨‍💻 Author

**Beni** - *Software Engineer*