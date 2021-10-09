# RiskAnalysis

## Without Docker:

  sudo docker-compose up
  
  sudo docker stop riskanalysis-api

  uvicorn --reload riskanalysis.src.app:app


## With Docker:

  sudo docker-compose up
    
    - you may need to restart riskanalysis-mongo-express, if it starts earlier than riskanalysis-mongo
    - you may need to restart riskanalysis-api, if it tries to connect do riskanalysis-mongo or riskanalysis-neo4j before they finished starting

### Configuration riskanalysis-mongo

  following steps are easiest to fulfill with login into riskanalysis-mongo-express (localhost:8081)
  
  create database "RiskAnalysis"
  
  create collection "tilt" in "RiskAnalysis"
  
  insert tilt documents into "tilt"

## Call API:
  
  http localhost:8000/update
  
  http localhost:8000/update/{domain}
  
  http localhost:8000/calculate
  
  http localhost:8000/{domain}
