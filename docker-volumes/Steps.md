# Steps
## 1. copy paste both files i.e., app.py and Dockerfile
## 2. build image using `docker build -t python-app .`
## 3. run image using `docker run -it --rm --name app -v $(pwd)/names.txt:/app/names.txt python-app`
