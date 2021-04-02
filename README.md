# RiskAnalysis

gunicorn --reload app:api

http localhost:8000/images

Docker:
  sudo docker build .
  sudo docker run -p 8000:8000 <image-id>
    -> sudo docker images
  
  sudo docker start <container-id>
    -> sudo docker ps -a
