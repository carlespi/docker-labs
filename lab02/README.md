# Lab 02 — Docker Setup and Validation on Ubuntu 24.04

## Objective

Verify an existing Docker Engine installation on Ubuntu 24.04 LTS, including service configuration, user permissions, and container execution.

## Environment

- AWS EC2 — Ubuntu 24.04 LTS
- Docker Engine
- Linux systemd

## Steps

### 1. Verify Docker Installation

```bash
docker --version
docker info
```

### 2. Verify Docker Service

```bash
systemctl is-active docker
systemctl is-enabled docker
```

Expected output:

```text
active
enabled
```

### 3. Verify User Permissions

```bash
groups
```

Confirm that the current user belongs to the `docker` group, allowing Docker commands without `sudo`.

Note: Membership in the Docker group grants root-equivalent privileges.

### 4. Run a Test Container

```bash
docker run --rm hello-world
```

Expected output:

```text
Hello from Docker!
```

The `--rm` option automatically removes the container after execution.

### 5. Inspect Docker Resources

```bash
docker images
docker ps -a
```

### 6. Review Docker Service Logs

```bash
sudo journalctl -u docker -n 30 --no-pager
```

## Result

Docker Engine was successfully validated on Ubuntu 24.04 LTS. The service is running, automatic startup is enabled, and the current user can execute Docker containers without sudo.