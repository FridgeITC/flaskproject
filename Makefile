
ec2conf:
    sudo yum update -y
    sudo yum install docker -y
    sudo service docker start
    sudo docker build -t yolov5-flask .
    docker run -p 8080:8080 yolov5-flask:latest

