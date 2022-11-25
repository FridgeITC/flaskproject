# flaskproject

## Installation
For installation and setup use
```shell
pip install -r requeriments.txt
```
## Running
> By default the server runs on port 8080 on all addresses
```shell
python3 rest.py
```

## Docker
The example dockerfile shows how to expose the rest API:

# Build
```shell
docker build -t yolov5-flask .
```

# Run
> consider using the -dp flag for detached process, you need to build the image first to run the container
```shell
docker run -p 8080:8080 yolov5-flask:latest
```


