# Lab 03 — Docker Basic Commands

## Objective

Practice essential Docker commands for managing containers, inspecting resources, transferring files, and modifying container filesystems.

## Environment

- AWS EC2 — Ubuntu 24.04 LTS
- Docker Engine
- NGINX
- Visual Studio Code (Remote SSH)

## 1. Pull and Run NGINX

Search for and download the official NGINX image:

```bash
docker search nginx
docker pull nginx:latest
docker images
```

Create a container with port 8080 mapped to NGINX port 80:

```bash
docker run -it -d -p 8080:80 --name cont-l03-nginx nginx:latest
docker ps
```

Access the web server from an external browser using the EC2 public IP and port 8080.

## 2. Execute Commands Inside the Container

```bash
docker exec -it cont-l03-nginx bash
```

Inspect the container environment:

```bash
whoami
pwd
cat /etc/os-release
ls /usr/share/nginx/html/
exit
```

The `exit` command closes the interactive shell without stopping the container.

## 3. Inspect Container Logs and Resources

```bash
docker logs cont-l03-nginx
docker logs -f cont-l03-nginx
docker stats cont-l03-nginx
docker inspect cont-l03-nginx
docker history nginx:latest
```

Use `Ctrl+C` to stop following logs or resource statistics without stopping the container.

## 4. Copy Files Between Host and Container

Copy NGINX configuration and the default HTML page to the host:

```bash
docker cp cont-l03-nginx:/etc/nginx/nginx.conf ./nginx.conf
docker cp cont-l03-nginx:/usr/share/nginx/html/index.html ./index.html
```

Replace `index.html` with the customized Mexican restaurant demo page included in this directory.

Copy the updated HTML into the running container:

```bash
docker cp ./index.html cont-l03-nginx:/usr/share/nginx/html/index.html
```

Refresh the external browser to verify the updated page. No container restart is required.

## 5. Modify Files and Permissions

Create a test file on the host and copy it into the container:

```bash
echo "Text from host" > newfile.txt
docker cp newfile.txt cont-l03-nginx:/tmp/
docker exec -it cont-l03-nginx bash
```

Inside the container, update ownership and permissions:

```bash
chown root:root /tmp/newfile.txt
chmod 400 /tmp/newfile.txt
ls -l /tmp/newfile.txt
```

Restore write permissions and append another line:

```bash
chmod 600 /tmp/newfile.txt
echo "New line from inside container" >> /tmp/newfile.txt
cat /tmp/newfile.txt
exit
```

Copy the modified file back to the host:

```bash
docker cp cont-l03-nginx:/tmp/newfile.txt ./newfile-copy.txt
cat ./newfile-copy.txt
```

Expected output:

```text
Text from host
New line from inside container
```

## Result

Successfully deployed and accessed an NGINX container, inspected its runtime information, transferred files between the host and container, and modified file permissions and content.

The customized `index.html` demonstrates how a running container can serve updated content without rebuilding the Docker image.