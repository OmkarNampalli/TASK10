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
