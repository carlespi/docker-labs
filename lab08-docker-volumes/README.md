# Lab 08 - Docker Volumes Hands-on

## Objective

Explore Docker storage options and understand how data persists across container restarts, removal, and recreation.

Storage options covered:

- Bind Mounts
- Named Volumes
- Anonymous Volumes

## Environment

- AWS EC2 - Ubuntu 24.04 LTS
- Docker Engine
- Alpine Linux

## Scenario 1: Using Bind Mounts

Bind mounts map a directory from the Docker host into a container. Both environments access the same files, and changes are immediately visible.

### 1. Create a Host Directory:

```bash
mkdir -p docker_bind_test
echo "This is a bind mount test file" > docker_bind_test/test.txt
```

### 2. Run a Container with a Bind Mount(Run Anyone Command based on your OS)

```bash
docker run -dit --name cont-l08-bind \
  --mount type=bind,source="$(pwd)/docker_bind_test",target=/app \
  alpine:latest sh
```

The host directory is mounted at `/app` inside the container.

### 3. Inspect the Container:

```bash
docker exec -it cont-l08-bind sh
```

Inside Alpine:

```sh
ls /app
cat /app/test.txt
exit
```

Expected output:

```text
This is a bind mount test file
```

### 4. Modify the File from Host:

From EC2:

```bash
echo "Updated from host" >> docker_bind_test/test.txt
docker exec cont-l08-bind cat /app/test.txt
```

Expected output:

```text
This is a bind mount test file
Updated from host
```

This confirms that changes made on the host are immediately visible inside the container.

### 5. Cleanup:

```bash
docker rm -f cont-l08-bind
ls -l docker_bind_test/
cat docker_bind_test/test.txt
```

The file remains on the host after the container is removed.

## Scenario 2: Using Named Volumes

Named volumes are persistent storage resources managed by Docker and identified by a user-defined name.

### 1. Create a Named Volume:

```bash
docker volume create vol-l08-named
docker volume ls
```

### 2. Run a Container with the Named Volume:

```bash
docker run -dit --name cont-l08-named \
  --mount type=volume,source=vol-l08-named,target=/app \
  alpine:latest sh
```

The named volume is mounted at `/app` inside the container.

### 3. Inspect the Volume in the Container:

```bash
docker exec -it cont-l08-named sh
```

Inside Alpine:

```sh
echo "This is a named volume test file" > /app/test.txt
ls /app
cat /app/test.txt
exit
```

The file is written to the mounted Docker volume.

#### Verify the Volume Directly from the EC2 Host

Identify the volume's physical storage location:

```bash
docker volume inspect vol-l08-named
```

Display only the mountpoint:

```bash
docker volume inspect vol-l08-named --format '{{.Mountpoint}}'
```

On a standard rootful Docker Engine installation, the location typically resembles:

```text
/var/lib/docker/volumes/vol-l08-named/_data
```

Verify that `test.txt` exists in the Docker-managed storage directory:

```bash
sudo ls -l "$(docker volume inspect vol-l08-named --format '{{.Mountpoint}}')"
sudo cat "$(docker volume inspect vol-l08-named --format '{{.Mountpoint}}')/test.txt"
```

Expected output:

```text
This is a named volume test file
```

This confirms that the file is stored in the volume's host-side storage location, not in the container's writable layer.

Direct inspection is useful for learning and troubleshooting. In normal operation, volume contents should be managed through containers rather than manually modifying Docker's internal directories.

### 4. Restart the Container:

```bash
docker stop cont-l08-named
docker start cont-l08-named
docker exec -it cont-l08-named sh
```

Inside Alpine:

```sh
ls /app
cat /app/test.txt
exit
```

The file remains available after restarting the container.

### 5. Remove the Container and Reattach Volume:

Remove the original container:

```bash
docker rm -f cont-l08-named
```

Create a new container using the existing volume:

```bash
docker run -it --rm --name cont-l08-named-new \
  --mount type=volume,source=vol-l08-named,target=/app \
  alpine:latest sh
```

Inside the new container:

```sh
ls /app
cat /app/test.txt
exit
```

Expected output:

```text
This is a named volume test file
```

This demonstrates that named volumes preserve data independently of container removal and recreation.

### 6. Inspect the named volume:

```bash
docker volume inspect vol-l08-named
```

Relevant fields:

- `Name`: Volume identifier.
- `Driver`: Storage driver, typically `local`.
- `Mountpoint`: Host-side storage location.
- `Scope`: Volume scope, typically `local`.

### 7. Cleanup:

```bash
docker volume rm vol-l08-named
```

Removing the named volume permanently deletes its stored data.

## Scenario 3: Using Anonymous Volumes

Anonymous volumes are Docker-managed volumes created without a user-defined name.

Docker automatically generates a unique identifier. These volumes can persist after container removal, but are less convenient to identify and reuse.

### 1. Run a Container with an Anonymous Volume:

```bash
docker run -dit --name cont-l08-anonymous \
  --mount type=volume,target=/app \
  alpine:latest sh
```

Omitting `source` instructs Docker to create a new anonymous volume.

### 2. Inspect the Volume in the Container:

```bash
docker exec -it cont-l08-anonymous sh
```

Inside Alpine:

```sh
echo "This is an anonymous volume test file" > /app/test.txt
ls /app
cat /app/test.txt
exit
```

List Docker volumes:

```bash
docker volume ls
```

Identify the anonymous volume attached to this specific container:

```bash
docker inspect cont-l08-anonymous --format '{{range .Mounts}}{{.Name}}{{end}}'
```

The result is an automatically generated volume identifier.

### 3. Stop and Remove the Container:

```bash
docker stop cont-l08-anonymous
docker rm cont-l08-anonymous
```

Because the container is removed without the `-v` option, its anonymous volume remains in Docker.

### 4. Check the Volume:

Create another container with a new anonymous volume:

```bash
docker run -it --rm --mount type=volume,target=/app alpine:latest sh
```

Inside Alpine:

```sh
ls /app
exit
```

The original `test.txt` does not appear because Docker created a different anonymous volume.

Check the existing volumes:

```bash
docker volume ls
```

**Important:** The original anonymous volume still retains its data. It is not automatically attached to the new container.

## Comparison of Docker Storage Options

### Bind Mounts

- **Storage location:** Specific host file or directory.
- **Management:** Host-managed.
- **Persistence:** Survives container removal.
- **Reuse:** Mount the same host path.
- **Typical use:** Configuration files, development files, and source code.

### Named Volumes

- **Storage location:** Docker-managed storage.
- **Management:** Docker-managed with a user-defined name.
- **Persistence:** Survives container removal unless explicitly deleted.
- **Reuse:** Reference the same volume name.
- **Typical use:** Databases and persistent application data.

### Anonymous Volumes

- **Storage location:** Docker-managed storage.
- **Management:** Docker-managed with an automatically generated identifier.
- **Persistence:** Can survive container removal.
- **Reuse:** Possible using the generated identifier, but less convenient.
- **Typical use:** Container-specific data without a predefined volume name.

## Key Docker Commands

### Volume Management

```bash
docker volume create <volume_name>
docker volume ls
docker volume inspect <volume_name>
docker volume rm <volume_name>
```

### Volume Mount Syntax

**Bind Mount**

```bash
--mount type=bind,source=<host_directory>,target=<container_directory>
```

**Named Volume**

```bash
--mount type=volume,source=<volume_name>,target=<container_directory>
```

**Anonymous Volume**

```bash
--mount type=volume,target=<container_directory>
```

## Conclusion

This lab demonstrated three Docker storage options and their behavior across container lifecycle operations.

- Bind mounts provide direct access to files stored on the Docker host.
- Named volumes provide Docker-managed persistent storage that can be shared and reused.
- Anonymous volumes provide persistent Docker-managed storage without a user-defined name.

The main takeaway is that **container removal does not necessarily result in data loss**. Data persistence depends on the storage mechanism and whether the underlying storage resource is retained.