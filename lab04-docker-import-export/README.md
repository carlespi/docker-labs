# Lab 04 - Docker Export/Import & Save/Load

## Objective

Practice backing up and restoring Docker containers and images, understanding the differences between `export/import` and `save/load`.

## Environment

- AWS EC2 — Ubuntu 24.04 LTS
- Docker Engine
- Ubuntu and NGINX images
- Docker Hub

## Section 1: Docker Export & Import

### 1. Create and Customize an Ubuntu Container

```bash
docker pull ubuntu:latest
docker run -it --name cont-l04-ubuntu ubuntu:latest
```

Inside the container, install `curl` and `figlet`:

```bash
apt update
apt install -y curl
apt install -y figlet
figlet Hello
exit
```

### 2. Export and Restore the Container

Export the customized container filesystem:

```bash
docker export cont-l04-ubuntu -o ubuntu-backup.tar
```

After removing the original container, import the backup as a new image:

```bash
docker import ubuntu-backup.tar img-l04-ubuntu:imported
```

Create a container from the imported image:

```bash
docker run -it --name cont-l04-ubuntu-restored img-l04-ubuntu:imported /bin/bash
```

Verify that the installed utilities were preserved:

```bash
which curl
which figlet
figlet Hurray.!
exit
```

### 3. Commit and Publish the Restored Container

Create a new image from the restored container:

```bash
docker commit cont-l04-ubuntu-restored img-l04-ubuntu:fixed
```

Tag and publish it to Docker Hub:

```bash
docker tag img-l04-ubuntu:fixed carlespi/img-l04-ubuntu:fixed
docker login
docker push carlespi/img-l04-ubuntu:fixed
```

Published image: [carlespi/img-l04-ubuntu](https://hub.docker.com/r/carlespi/img-l04-ubuntu)

## Section 2: Docker Save & Load

### 1. Save the NGINX Image

```bash
docker pull nginx:latest
docker save nginx:latest -o nginx-image-backup.tar
```

Unlike `docker export`, `docker save` preserves the complete image, including its layers and configuration.

### 2. Remove and Restore the Image

After removing the original container that depended on `nginx:latest`, remove the image:

```bash
docker rmi nginx:latest
```

Restore it from the backup:

```bash
docker load -i nginx-image-backup.tar
docker images
```

### 3. Run the Restored Image

```bash
docker run -dit --name cont-l04-nginx -p 8081:80 nginx:latest
docker ps
```

The restored NGINX image successfully served its default welcome page through port `8081`, verified from an external Windows browser.

## Section 3: Comparison & Significance

- **Export/Import:** Preserves a container's filesystem but discards image history and configuration metadata such as `CMD`.
- **Save/Load:** Preserves the complete image, including layers, history, and configuration metadata.

## Result

Successfully exported and imported a customized Ubuntu container, verified the restored applications, published the resulting image to Docker Hub, and restored an NGINX image using `docker save` and `docker load`.