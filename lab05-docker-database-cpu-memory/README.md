# Lab 05 - Docker Databases, XML Configuration & Resource Limits

## Objective

Explore how Docker simplifies database deployment, application configuration management, and resource allocation through hands-on exercises with MySQL, Python, XML, and NGINX.

## Environment

- AWS EC2 - Ubuntu 24.04 LTS
- Docker Engine
- MySQL
- NGINX
- Python 3.9

## 1. Docker and Databases: Running a Database in a Containerized Environment

Created a MySQL container and verified the database service using Docker logs and the MySQL CLI.

```bash
docker run --name cont-l05-mysql -e MYSQL_ROOT_PASSWORD=rootpwd -d -p 3306:3306 mysql
docker ps
docker logs cont-l05-mysql
```

Connected to MySQL:

```bash
docker exec -it cont-l05-mysql mysql -u root -p
```

Executed SQL commands:

```sql
SHOW DATABASES;
exit;
```

Successfully accessed the database server and listed the available databases.

## 2. Docker and XML Format: Processing XML Files in Dockerized Applications

Created a Python application that reads database configuration values from an XML file.

Project files:

- `config.xml` - Contains sample database connection settings.
- `script.py` - Parses XML and extracts the database hostname and username.
- `Dockerfile` - Defines the Python application image.

### Build and Run the Application

```bash
docker build -t img-l05-xml .
docker run --rm img-l05-xml
```

Expected output:

```text
Connecting to database at localhost with user root
```

The script parses configuration values but does not establish an actual MySQL connection.

### Mounting XML Configurations Externally

Created a container with a bind mount that maps the configuration file from the EC2 host to the container.

```bash
docker run -it -d \
  -v "$(pwd)/config.xml:/app/config.xml" \
  --name cont-l05-xml \
  img-l05-xml bash
```

Executed the Python script inside the running container:

```bash
docker exec cont-l05-xml python /app/script.py
```

Modified the hostname in the host's `config.xml` and verified that the container read the updated value without rebuilding the image.

This demonstrated how bind mounts allow applications to use externally managed configuration files.

### Inspecting Container Metadata

Inspected the container's bind mounts:

```bash
docker inspect cont-l05-xml --format '{{json .Mounts}}'
```

Exported the container metadata to a JSON file:

```bash
docker inspect cont-l05-xml > metadata.json
```

The metadata includes container configuration, runtime state, network settings, and filesystem mounts.

## 3. CPU and Memory Limits

Created two NGINX containers with different CPU and memory restrictions.

### Container 1 - 0.5 CPU and 256 MiB RAM

```bash
docker run -d --cpus="0.5" --memory="256m" --name cont-l05-nginx-1 nginx:latest
```

Verified the resource configuration:

```bash
docker inspect cont-l05-nginx-1 --format 'NanoCpus={{.HostConfig.NanoCpus}} Memory={{.HostConfig.Memory}} CpuShares={{.HostConfig.CpuShares}}'
```

Result:

```text
NanoCpus=500000000 Memory=268435456 CpuShares=0
```

### Container 2 - 0.25 CPU and 128 MiB RAM

```bash
docker run -d --cpus="0.25" --memory="128m" --name cont-l05-nginx-2 nginx:latest
```

Verified the resource configuration:

```bash
docker inspect cont-l05-nginx-2 --format 'NanoCpus={{.HostConfig.NanoCpus}} Memory={{.HostConfig.Memory}} CpuShares={{.HostConfig.CpuShares}}'
```

Result:

```text
NanoCpus=250000000 Memory=134217728 CpuShares=0
```

Both containers were successfully started with their configured CPU and memory limits.

These limits restrict maximum resource usage rather than reserving resources exclusively for each container.

## Result

Successfully completed the following exercises:

- Deployed and accessed a MySQL database running inside Docker.
- Built a Python container that parses database configuration from XML.
- Used bind mounts to provide external configuration without rebuilding the image.
- Inspected container metadata and filesystem mounts.
- Configured and verified CPU and memory limits for two NGINX containers.

The lab demonstrated how Docker supports database deployment, external application configuration, and resource management in containerized environments.