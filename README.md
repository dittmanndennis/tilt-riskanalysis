# RiskAnalysis

## Without Docker:

  uvicorn --reload riskanalysis.src.app:app


## With Docker:

  sudo docker build . -t <tag>
  
  sudo docker run -p 8000:8000 {image-id}
  
    -> sudo docker images
  
  sudo docker start {container-id}
  
    -> sudo docker ps (-a)

  
## Call API:
  
  http localhost:8000/{domain}
