# Lab 03 - Docker Commit and Push to Docker Hub

## Objective

Create a custom Docker image from a modified NGINX container, publish it to Docker Hub, and verify that the image can be pulled and used to deploy a new container.

## Environment

- AWS EC2 — Ubuntu 24.04 LTS
- Docker Engine
- NGINX
- Docker Hub

## 1. Create a Custom Docker Image

Use the existing NGINX container, previously customized with a Mexican restaurant HTML page, to create a reusable image.

```bash
docker commit cont-l03-nginx img-l03-nginx:lab03
docker images
```

## 2. Tag and Push to Docker Hub

Assign a Docker Hub repository name to the image:

```bash
docker tag img-l03-nginx:lab03 carlespi/img-l03-nginx:lab03
```

Authenticate and publish:

```bash
docker login
docker push carlespi/img-l03-nginx:lab03
```

The image was successfully published with the `lab03` tag.

## 3. Pull and Deploy the Image

Retrieve the published image:

```bash
docker pull carlespi/img-l03-nginx:lab03
```

Create a new container using the image:

```bash
docker run -d --name cont-l03-pushed-nginx -p 8081:80 carlespi/img-l03-nginx:lab03
docker ps
```

## 4. Verification

The new container successfully served the customized HTML page through port `8081`, verified from an external Windows browser.

The published image is available on [Docker Hub](https://hub.docker.com/r/carlespi/img-l03-nginx).

## Result

Successfully created a reusable Docker image using `docker commit`, tagged and published it to Docker Hub, pulled the image, and deployed a new NGINX container while preserving the customized web content.