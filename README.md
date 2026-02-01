# TASK10
Docker Volumes and Docker Network

---

## Docker Volumes
### The Problem: Ephemeral Storage
Containers (like Docker) are **ephemeral** by design.That means:
* A container’s filesystem exists only while the container is running.
* When a container is stopped, deleted, or recreated, any data written inside the container’s writable layer is lost.

This causes problems when containers are used for applications that generate or store data, such as:
- Databases (MySQL, PostgreSQL, MongoDB)
- Log files
- User uploads
- Application state or configuration generated at runtime

**Scaling issues**: If you run multiple containers, each has its own isolated filesystem. Data inside one container isn’t automatically shared with others.

#### Why does this happen?
Containers are built from **immutable images**. At runtime:
- The image stays read-only
- A thin writable layer is added on top
- All changes go into that writable layer
When the container dies, that writable layer disappears with it.

### The Solution: Docker Volumes
Volumes solve this problem by **decoupling data from the container lifecycle**.
#### What is a volume?
Volumes act like an **external hard drive** for your container. They decouple the data from the container's lifecycle.
A volume is a **persistent storage mechanism** that::
- Lives outside the container filesystem
- Is managed by Docker (or the container runtime)
- Can be mounted into one or more containers
### How volumes prevent data loss
- **Data Persistence**:Volumes exist outside the container’s writable layer. If the container is destroyed, the volume remains on the host machine. When you start a new container, you can simply "plug" that same volume back in, and your data is exactly where you left it.
- **Sharing**: Volumes can be mounted into multiple containers, enabling data sharing between them.
- **Isolation**: Volumes are managed by Docker (or the container runtime), separate from the container’s writable layer.
- **Performance**: Volumes bypass the storage driver and write directly to the host’s filesystem, making them much faster for high-I/O tasks.
- **Backup & Migration**: Because the data is stored in a dedicated area on your host (usually `/var/lib/docker/volumes/`), it is much easier to back up or migrate than trying to "reach inside" a running container.

### Managing Volumes Directly
If you want to prepare your "storage" before launching a container, use these management commands:
- **Create a volume**: `docker volume create my_data`
- **List all volumes**: `docker volume ls`
- **Inspect details (find the mount path on your host)**: `docker volume inspect my_data`
- **Remove a volume**: `docker volume rm my_data`
> A volume must not be in use to be removed.
### Attaching Volumes to Containers
There are two ways to do this: the older `-v`(volume) flag and the newer, more explicit `--mount` flag.

#### Option A: The -v Flag (Shorthand)
This is the most common method due to its brevity. The syntax is [volume_name]:[container_path].

* **Basic Syntax**: `docker run -v volume_name:container_path image_name`
* **Example**:
```Bash
docker run -d \
  --name my_db \
  -v my_data:/var/lib/mysql \
  mysql:latest
```
* **Example (Linking your current project folder)**:

```Bash
docker run -dp 8080:80 \
  -v $(pwd):/app \
  nginx:latest
```
In this case, any change you make to the files in your current directory ($(pwd)) will instantly reflect inside the /app folder of the container.
If my_data doesn't exist, Docker will automatically create it for you.

#### Option B: The --mount Flag (Recommended)
This is preferred for complex setups because it is more "wordy" and less prone to mistakes.
```Bash
docker run -d \
  --name my_db \
  --mount source=my_data,target=/var/lib/mysql \
  mysql:latest
```
Verify volume usage

### Check which volumes a container uses:

`docker inspect container_name`
Look for:
```json
"Mounts": [
  {
    "Type": "volume",
    "Name": "mysql_data",
    "Destination": "/var/lib/mysql"
  }
]
```
### Share a volume between containers
```
docker run -d \
  --name app1 \
  -v shared_data:/data \
  alpine sleep 1000

docker run -d \
  --name app2 \
  -v shared_data:/data \
  alpine sleep 1000
```
Both containers can access /data.

### Read-only volume
```
docker run -d \
  -v my_volume:/data:ro \
  nginx
```
Prevents container from modifying the data.
### Clean up unused volumes
Remove unused volumes:
`docker volume prune`
> ⚠️ This deletes all unused volumes.


---
## Docker Network
In the world of Docker, **Networking** is the system that allows containers to talk to each other, to the host machine, and to the outside world (the internet).

Without a network, a container is an isolated island. With a network, it becomes part of a distributed architecture.

Think of it as a virtual network layer created by Docker, similar to how networks connect physical machines.

It provides each container with its own isolated network environment (IP address, interfaces, routing) and enables secure, controlled communication between containers and external services.
 
---

### How Docker networking works (conceptually)
- Each container gets
  - An IP address
  - A virtual network interface
- Docker creates virtual networks on the host
- Containers attached to the same network can communicate directly
```
Web Container  ---->  DB Container
     (same Docker network)
```

Docker uses Network Drivers to manage how containers communicate. When you install Docker, it automatically creates three default networks: **Bridge**, **Host**, and **None**.
|Driver|Behavior|Best Use Case|
| :--- | :--- | :--- |
|Bridge|The default. Creates a private internal network on the host. Containers get their own IP addresses but are isolated from the host's physical network.|Standard standalone containers.|
|Host|Removes isolation. The container shares the host’s IP and port space directly.|High-performance apps where network overhead must be zero.|
|None|Complete isolation. The container has no external network interface.|High-security tasks or batch processing that requires no network.|
|Overlay|Connects multiple Docker daemons (hosts) together.|Docker Swarm or multi-host clusters.|
|Macvlan|Assigns a real IP from your local networ. Containers appear as physical devices on the network| .. |

### Key Concept: DNS & Service Discovery
One of the best features of **User-Defined Bridge Networks** is built-in DNS.

If you create a custom network and attach two containers named `web` and `database`, the web container doesn't need to know the IP address of the database. It can simply reach it by typing: `ping database`

Docker's internal DNS resolver handles the translation automatically. This is much more reliable than hardcoding IP addresses, which change every time a container restarts.

### Common CLI Commands
You manage networks similarly to how you manage volumes:
* **Create a network**: `docker network create my_app_net`
* **Run a container on a specific network**: `docker run -d --name db --network my_app_net mysql`
* **Connect an already running container to a network**: `docker network connect my_app_net existing_container`
* **List all networks**: `docker network ls`

| Task                     | Command                                          |
| ------------------------ | ------------------------------------------------ |
| List networks            | `docker network ls`                              |
| Create network           | `docker network create my_network`               |
| Inspect network          | `docker network inspect my_network`              |
| Remove network           | `docker network rm my_network`                   |
| Clean unused             | `docker network prune`                           |
| Run container on network | `docker run --network my_network image`          |
| Connect container        | `docker network connect my_network container`    |
| Disconnect container     | `docker network disconnect my_network container` |


### Port Mapping (The Gateway)
Even if a container is on a network, it is blocked from the internet by default for security. To make a web server inside a container accessible to your browser, you use Port Mapping with the `-p` flag:

`docker run -p 8080:80 nginx`

> This tells Docker: "Take any traffic hitting the host at port 8080 and forward it to port 80 inside this container."

### Key benefits of Docker networks
- Automatic DNS (use container names)
- Isolation between applications
- Secure communication
- Easy scaling
- Port conflict avoidance
