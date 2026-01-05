# Rolling Project - Contacts Management API

A robust RESTful API for managing contacts, built with **FastAPI**. This project features a flexible architecture that supports switching between **MySQL** and **MongoDB** databases dynamically using the Repository pattern. It is containerized with Docker and ready for Kubernetes deployment.

## 🚀 Features

* **Dual Database Support:** Seamlessly switch between MySQL and MongoDB via configuration.
* **Clean Architecture:** Implements the Repository and Factory design patterns for separation of concerns.
* **FastAPI Powered:** High-performance, async-ready web framework using Python type hints.
* **Containerized:** Includes `Dockerfile` and `compose.yaml` for easy deployment.
* **Kubernetes Ready:** Includes K8s manifests for Pods and Services.
* **Auto-Initialization:** Automatically loads mock data (JSON for Mongo, SQL script for MySQL) upon first run.

## 🛠️ Tech Stack

* **Language:** Python 3.11
* **Framework:** FastAPI
* **Databases:** MySQL 8.0, MongoDB
* **Infrastructure:** Docker, Kubernetes (Minikube compatible)
* **Libraries:** `pymongo`, `mysql-connector-python`, `pydantic`, `uvicorn`

## 📂 Project Structure

```text
├── app/
│   ├── db/             # Database implementations (Factory, SQL/Mongo Repositories)
│   ├── models/         # Pydantic models
│   ├── routes/         # API endpoints (Contacts, Admin)
│   ├── services/       # Business logic layer
│   ├── main.py         # Application entry point
│   └── config.json     # Database configuration
├── k8s/                # Kubernetes manifests
├── compose.yaml        # Docker Compose configuration
└── requirements.txt    # Python dependencies
```

## ⚙️ Configuration

The application determines which database to use based on `app/config.json` or environment variables.

**Example `config.json`:**
```json
{
  "active_db": "mongo", 
  "connections": {
    "mysql": { "host": "localhost", "port": 3306, ... },
    "mongo": { "host": "localhost", "port": 27017, ... }
  }
}
```
* Set `"active_db"` to `"mysql"` or `"mongo"` to switch implementations.

## 🏃 Getting Started

### Option 1: Run with Docker Compose (Recommended)

This will start the API and a MySQL database container.

1.  Ensure Docker is running.
2.  Update `app/config.json` to set `"active_db": "mysql"` (since the compose file provides MySQL).
3.  Run the command:
    ```bash
    docker-compose up --build
    ```
4.  Access the API documentation at: `http://localhost:8000/docs`

### Option 2: Run Locally (Python)

1.  Install dependencies:
    ```bash
    pip install -r app/requirements.txt
    ```
2.  Ensure you have a running instance of MongoDB or MySQL locally.
3.  Update `app/config.json` with your local DB credentials.
4.  Run the server:
    ```bash
    cd app
    python main.py
    ```

### Option 3: Kubernetes (Minikube)

1.  Start Minikube:
    ```bash
    minikube start
    ```
2.  Apply the manifests:
    ```bash
    kubectl apply -f k8s/
    ```
3.  Access the service via NodePort or use port-forwarding.

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/contacts` | Retrieve all contacts |
| `POST` | `/contacts` | Create a new contact |
| `PUT` | `/contacts/{id}` | Update an existing contact |
| `DELETE` | `/contacts/{id}` | Delete a contact |
| `POST` | `/admin/reload-db` | Reload DB config without restarting server |

## 🧪 Testing

You can use the `test.http` file included in the root directory to test endpoints directly from your IDE (e.g., VS Code REST Client).

## 📝 License

This project is open-source and available for educational purposes.