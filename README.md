# Contact Manager API 📞

A RESTful API service for managing contacts, built with **Python (FastAPI)** and **MySQL**.
The project demonstrates a clean architecture (Service-Repository pattern), manual SQL query execution (no ORM), and full containerization using **Docker**.

## 🚀 Features

* **CRUD Operations**: Create, Read, Update, and Delete contacts.
* **Manual SQL**: All database interactions are performed using raw SQL queries for optimized performance and control.
* **Architecture**: Separation of concerns using **Router -> Service -> Repository** layers.
* **Dockerized**: Fully containerized application and database using Docker Compose.
* **Data Persistence**: MySQL data is persisted using Docker Volumes.
* **Health Checks**: Ensures the API only starts after the Database is fully ready.

## 🛠️ Tech Stack

* **Language**: Python 3.11
* **Framework**: FastAPI
* **Database**: MySQL 8.0
* **Containerization**: Docker & Docker Compose
* **Libraries**: `mysql-connector-python`, `pydantic`, `uvicorn`

## 📂 Project Structure

```text
week10_contacts/
├── app/
│   ├── db/
│   │   ├── sql_repository/     # Raw SQL implementations & init.sql
│   │   ├── manager.py          # Database connection management
│   │   └── Idatabase.py        # Repository Interfaces
│   ├── models/                 # Pydantic data models
│   ├── routes/                 # API Endpoints (Controllers)
│   ├── services/               # Business Logic Layer
│   ├── main.py                 # Application Entrypoint
│   └── Dockerfile              # API Container configuration
├── compose.yaml                # Docker Compose orchestration
├── requirements.txt            # Python dependencies
└── README.md                   # Project Documentation
```

## ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/binya2/week10_contacts.git
    cd week10_contacts
    ```

2.  **Run with Docker Compose:**
    ```bash
    docker compose up --build -d
    ```

3.  **Wait for Initialization:**
    The database takes about 20-30 seconds to initialize the schema and populate sample data.

## 🔌 API Endpoints

Base URL: `http://localhost:8000`

| Method | Endpoint | Description | Request Body |
| :--- | :--- | :--- | :--- |
| **GET** | `/contacts` | Retrieve all contacts | None |
| **POST** | `/contacts` | Create a new contact | `{"first_name": "...", "last_name": "...", "phone_number": "..."}` |
| **PUT** | `/contacts/{id}` | Update contact phone | `{"phone_number": "..."}` |
| **DELETE** | `/contacts/{id}` | Delete a contact | None |

## 🧪 Testing (Curl Commands)

You can test the API using `curl` or Postman.

**1. Get All Contacts:**
```bash
curl http://localhost:8000/contacts
```

**2. Create a Contact:**
```bash
curl -X POST http://localhost:8000/contacts \
  -H "Content-Type: application/json" \
  -d '{"first_name":"New","last_name":"User","phone_number":"050-9999999"}'
```

**3. Update a Contact (Phone Only):**
```bash
curl -X PUT http://localhost:8000/contacts/1 \
  -H "Content-Type: application/json" \
  -d '{"phone_number":"054-1234123"}'
```

**4. Delete a Contact:**
```bash
curl -X DELETE http://localhost:8000/contacts/1
```

## 🔄 Admin / Maintenance

To reset the database (if IDs get messy or for clean testing):
```bash
docker compose down -v
docker compose up --build -d
```
*The `-v` flag removes the volume, triggering `init.sql` to run again on startup.*