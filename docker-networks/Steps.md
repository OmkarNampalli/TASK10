# Steps
## 1. Create Docker network
Use the following command to create a network: `docker network create my_network`
## 2. Run `mysql` container on network `my_network`
- Use the command given in `mysql-container-setup.txt` in this folder.
- Check mysql container is running status using `docker ps`
## 3. The app
- copy paste both files i.e., app.py and Dockerfile
- build image using `docker build -t python-app .`
- run image using `docker run -it --rm --name app --network my_network python-app`
## 4. Inspection
- use `docker network inspect my_network` and search for the containers.
