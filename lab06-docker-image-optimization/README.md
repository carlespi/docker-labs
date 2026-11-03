# Lab 06 - Docker Image Size Reduction

## Objective

Explore Docker image optimization techniques and measure how package cleanup, smaller base images, and multi-stage builds affect image size.

## Environment

- AWS EC2 — Ubuntu 24.04 LTS
- Docker Engine
- Ubuntu, Python Slim, and Python Alpine base images
- Python sample application

## Step 1: Create an Inefficient Docker Image

Created a basic Python application and an unoptimized Dockerfile using `ubuntu:latest`, with separate installation commands and no package cache cleanup.

```bash
docker build -t img-l06-unoptimized .
```

**Disk usage: 904 MB**

## Step 2: Optimize by Cleaning Cache and Removing Unused Packages

Combined dependency installation and cache cleanup into a single Dockerfile instruction:

```dockerfile
RUN apt-get update && apt-get install -y \
    curl wget git python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
```

```bash
docker build -t img-l06-optimized .
```

**Disk usage: 829 MB — 8.3% reduction**

## Step 3: Use a Smaller Base Image

Replaced Ubuntu with `python:3.9-slim` and removed unnecessary package installations.

```dockerfile
FROM python:3.9-slim
```

```bash
docker build -t img-l06-small-base .
```

**Disk usage: 183 MB — 79.8% reduction**

## Step 4: Use Multi-Stage Build to Further Reduce Size

Used `python:3.9-slim` as the builder stage and `python:3.9-alpine` as the final runtime stage.

```dockerfile
FROM python:3.9-slim AS builder
# Build dependencies and application

FROM python:3.9-alpine
# Copy application files from the builder stage
```

```bash
docker build -t img-l06-multi-stage .
```

**Disk usage: 79.8 MB — 91.2% reduction**

The final image only includes the lightweight Python runtime and application files. The builder-stage dependencies are not transferred to the runtime image.

## Comparison of Image Sizes

| Image | Disk Usage | Content Size | Reduction |
|---|---:|---:|---:|
| `img-l06-unoptimized` | 904 MB | 242 MB | Baseline |
| `img-l06-optimized` | 829 MB | 211 MB | 8.3% |
| `img-l06-small-base` | 183 MB | 45 MB | 79.8% |
| `img-l06-multi-stage` | 79.8 MB | 19.7 MB | 91.2% |

Reductions are calculated relative to the unoptimized image's disk usage.

## Verification

Run each image to validate the sample Python application:

```bash
docker run --rm img-l06-unoptimized
docker run --rm img-l06-optimized
docker run --rm img-l06-small-base
docker run --rm img-l06-multi-stage
```

Expected output:

```text
Hello from Docker
```

## Result

Reduced Docker image disk usage from **904 MB to 79.8 MB (91.2%)**.

The largest improvement came from selecting a smaller base image and excluding unnecessary dependencies. The final multi-stage image uses Alpine; its reduced size should not be attributed solely to the multi-stage technique.