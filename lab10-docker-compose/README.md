# Lab 10 - Docker-Compose Hands-On Practice

## Overview

Deploy a three-tier application using Docker Compose, demonstrating container orchestration, service-to-service communication, persistent storage, and application updates.

The application consists of three independent services:

- **Frontend:** NGINX serves a static HTML dashboard.
- **Backend:** Python Flask provides HTTP endpoints and connects to MySQL.
- **Database:** MySQL 8.0 processes SQL queries and uses persistent storage.

Docker Compose manages the services, networking, container configuration, and storage through a single YAML file.

## Technologies

- Docker Engine
- Docker Compose V2
- NGINX Alpine
- Python 3.9 Slim
- Flask
- MySQL 8.0
- AWS EC2 - Ubuntu 24.04

## Project Structure

```text
lab10-docker-compose/
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── frontend/
│   └── index.html
└── README.md
```

## Application Components

### Frontend - NGINX

The frontend uses the official `nginx:alpine` image to serve a custom HTML dashboard.

A read-only bind mount provides NGINX with the files stored in the project's `frontend` directory.

```yaml
volumes:
  - ./frontend:/usr/share/nginx/html:ro
```

Changes to `frontend/index.html` are reflected in the browser without rebuilding the NGINX image or recreating its container.

### Backend - Python Flask

The backend uses a custom Docker image built from `backend/Dockerfile`.

It exposes two HTTP endpoints:

- `/` - Returns `Hello from Flask Backend!`
- `/data` - Connects to MySQL, executes a SQL query, and returns the result as JSON.

The backend connects to MySQL using the Docker Compose service name `database`.

```python
connection = mysql.connector.connect(
    host="database",
    user="root",
    password="rootpassword",
    database="mydb"
)
```

Docker's internal DNS resolves `database` to the appropriate container IP address.

The SQL query used in this lab returns a static string rather than retrieving records from a table.

```sql
SELECT 'Hello from new MySQL!' AS message;
```

A successful response confirms that Flask can connect to MySQL, authenticate, select the database, and execute the query.

### Database - MySQL

The database service uses the official `mysql:8.0` image.

A Docker named volume stores its data outside the container's writable filesystem.

```yaml
volumes:
  - db-data:/var/lib/mysql
```

The volume persists when the database container is stopped, removed, or recreated, provided the volume itself is retained.

MySQL listens internally on port `3306`. This port is not published on the EC2 host.

## Networking and Ports

Docker Compose automatically creates a default bridge network for the application.

All three services join this network and can communicate using their service names.

**Frontend:**
- Container port: `80`
- EC2 published port: `8080`

**Backend:**
- Container port: `5001`
- EC2 published port: `8081`

**Database:**
- Container port: `3306`
- EC2 published port: None
- Accessible internally through the Docker Compose network

The database does not require a published host port because Flask communicates with it over Docker's internal network.

## Prerequisites

- Docker Engine installed and running
- Docker Compose V2 installed
- Git repository cloned locally
- Ports `8080` and `8081` available on the Docker host
- Appropriate firewall or AWS Security Group rules for external browser access

Verify the Docker installation:

```bash
docker --version
docker compose version
```

## Steps to Run the Application

### 1. Navigate to the Project Directory:

```bash
cd docker-labs/lab10-docker-compose
```

Run this command from the directory containing the cloned `docker-labs` repository.

### 2. Build and Start the Services:

Build the custom backend image:

```bash
docker build -t img-l10-backend:local ./backend
```

Start all three services:

```bash
docker compose up -d
```

Docker Compose creates the containers, application network, and MySQL named volume.

It also downloads the NGINX and MySQL images if they are not already available.

### 3. Access the Application:

Replace `<EC2_PUBLIC_IP>` with your instance's public IPv4 address.

**Frontend dashboard:**

```text
http://<EC2_PUBLIC_IP>:8080
```

**Backend endpoint:**

```text
http://<EC2_PUBLIC_IP>:8081
```

Expected response:

```text
Hello from Flask Backend!
```

**MySQL connection test:**

```text
http://<EC2_PUBLIC_IP>:8081/data
```

Expected JSON response:

```json
{
  "message": "Hello from new MySQL!"
}
```

The database may require a short initialization period on its first startup.

## Verify the Setup

### 1. Check Running Containers:

```bash
docker ps
```

Expected lab containers:

- `cont-l10-frontend`
- `cont-l10-backend`
- `cont-l10-database`

### 2. View Logs:

Display logs from all services:

```bash
docker compose logs
```

Inspect individual services:

```bash
docker compose logs frontend
docker compose logs backend
docker compose logs database
```

### 3. Upload the image to your repository

Tag the custom backend image for Docker Hub:

```bash
docker tag img-l10-backend:local carlespi/img-l10-backend:lab10
```

Authenticate and push:

```bash
docker login
docker push carlespi/img-l10-backend:lab10
```

The frontend and database use official Docker Hub images and do not require custom image builds.

### 4. Share the screenshot of your repository in WebEx spaces

The original instructor exercise requests a screenshot of the published image repository.

This step is specific to the training submission process and is not required to run the application.

### 5. Stop the Services:

```bash
docker compose down
```

This stops and removes the project's containers and default network.

Verify container removal:

```bash
docker ps -a
```

The project's named volume and Docker images remain available.

**Note:** Do not use `docker compose down -v` if you want to retain the MySQL volume.

### 6. Edit the files and check the results:

Modify the SQL query in `backend/app.py`.

Original:

```python
cursor.execute("SELECT 'Hello from MySQL!' AS message;")
```

Updated:

```python
cursor.execute("SELECT 'Hello from new MySQL!' AS message;")
```

Save the file and rebuild the backend image:

```bash
docker build -t img-l10-backend:local ./backend
docker compose up -d
```

The image must be rebuilt because `app.py` is copied into the image during the Docker build process.

### 7. Check the results by refreshing the web-page

Open:

```text
http://<EC2_PUBLIC_IP>:8081/data
```

Expected response:

```json
{
  "message": "Hello from new MySQL!"
}
```

This verifies that the updated application code was incorporated into the rebuilt image.

### 8. Similarly, update the content in the frontend and backend

Update `frontend/index.html` and refresh:

```text
http://<EC2_PUBLIC_IP>:8080
```

The updated frontend appears without rebuilding the NGINX image because the HTML file is provided through a bind mount.

Backend changes require rebuilding the custom image and recreating its container.

## Key Takeaways

- Docker Compose manages multiple services through a single YAML configuration.
- A Dockerfile builds a custom image; Compose configures and runs the application services.
- Docker Compose automatically creates a network with service-name DNS resolution.
- Bind mounts allow the frontend to use files directly from the host.
- Named volumes preserve database files independently of container removal.
- Publishing a container port is separate from opening that port in the AWS Security Group.
- Backend code changes require an image rebuild, while bind-mounted frontend changes are immediately available.
- `docker compose down` removes application containers and networks without deleting named volumes by default.

## Conclusion

This lab demonstrates how Docker Compose simplifies the deployment and lifecycle management of a multi-tier application.

The final deployment integrates NGINX, Python Flask, and MySQL using Docker-managed networking and persistent storage, while supporting separate update workflows for the frontend and backend.