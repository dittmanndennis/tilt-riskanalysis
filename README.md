# RiskAnalysis

uvicorn --reload riskanalysis.src.app:app

http localhost:8000/{domain}

Docker:

  sudo docker build . -t <tag>
  
  sudo docker run -p 8000:8000 {image-id}
  
    -> sudo docker images
  
  sudo docker start {container-id}
  
    -> sudo docker ps (-a)
