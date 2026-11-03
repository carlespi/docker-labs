# Lab 07 - Docker Networking

## Objective

Explore Docker networking modes and understand how containers communicate with each other, the Docker host, and external networks.

## Environment

- AWS EC2 - Ubuntu 24.04 LTS
- Docker Engine
- Alpine Linux containers

## Scenario 1: Using the Default Bridge Network

The default `bridge` network provides private IP addresses to containers and allows communication between them using those addresses.

### 1. Run Two Containers on the Default Bridge Network:

```bash
docker run -dit --name cont-l07-alpine-1 alpine:latest sh
docker run -dit --name cont-l07-alpine-2 alpine:latest sh
```

### 2. Inspect the Default Bridge Network:

```bash
docker network ls
docker network inspect bridge
```

The inspection displays network configuration, subnet, gateway, and connected containers.

### 3. Test Communication Between Containers:

Retrieve the second container's IP address:

```bash
docker inspect cont-l07-alpine-2 --format '{{.NetworkSettings.Networks.bridge.IPAddress}}'
```

Enter the first container:

```bash
docker exec -it cont-l07-alpine-1 sh
```

Install network utilities and test connectivity:

```sh
apk add --no-cache iputils
ping -c 4 <CONTAINER_2_IP>
ping -c 4 google.com
exit
```

This demonstrates container-to-container communication through private IP addresses and tests external connectivity.

## Scenario 2: Using the Host Network

Host networking allows a container to share the host's network namespace instead of having its own independent network interfaces and IP address.

### 1. Run a Container on the Host Network:

```bash
docker run --name cont-l07-host --network host -dit alpine:latest sh
```

### 2. Inspect the Host Network:

```bash
docker network inspect host
docker inspect cont-l07-host --format '{{.HostConfig.NetworkMode}}'
```

Expected network mode: `host`.

### 3. Test Host Network Access:

```bash
docker exec -it cont-l07-host sh
```

Inside the container:

```sh
apk add --no-cache curl
curl -I https://www.google.com
exit
```

Host networking shares the EC2 network stack and does not require Docker port publishing through `-p`.

## Scenario 3: Using a Custom Bridge Network

User-defined bridge networks provide isolated container networking with automatic DNS resolution between containers.

### 1. Create a Custom Network:

```bash
docker network create --driver bridge net-l07-custom
```

### 2. Run Two Containers on the Custom Network:

```bash
docker run -dit --name cont-l07-custom-1 --network net-l07-custom alpine:latest sh
docker run -dit --name cont-l07-custom-2 --network net-l07-custom alpine:latest sh
```

### 3. Inspect the Custom Network:

```bash
docker network inspect net-l07-custom
```

### 4. Test Container Communication:

```bash
docker exec -it cont-l07-custom-1 sh
```

Inside the container:

```sh
apk add --no-cache iputils
ping -c 4 cont-l07-custom-2
exit
```

Unlike the default bridge network, a user-defined bridge network supports communication using container names through Docker's built-in DNS.

## Scenario 4: Using the None Network

The `none` network disables external network connectivity while retaining the container's loopback interface.

### 1. Run a Container on the None Network:

```bash
docker run -dit --name cont-l07-none --network none alpine:latest sh
```

### 2. Inspect the None Network:

```bash
docker network inspect none
docker inspect cont-l07-none --format '{{.HostConfig.NetworkMode}}'
```

Expected network mode: `none`.

### 3. Test Network Isolation:

```bash
docker exec -it cont-l07-none sh
```

Inside the container:

```sh
ping -c 4 8.8.8.8
cat /proc/net/dev
exit
```

The external ping should fail because the container has no external network interface or route.

## Conclusion

The lab demonstrates four Docker networking configurations:

- **Default Bridge:** Private IP-based communication between containers.
- **Host:** Direct use of the host network namespace.
- **Custom Bridge:** Isolated networking with automatic container-name DNS resolution.
- **None:** Network isolation without external connectivity.

These networking options provide different levels of connectivity, isolation, and control depending on application requirements.