# RiskAnalysis

## With Docker & Server (Uvicorn):

  sudo docker-compose up
  
  sudo docker stop riskanalysis-api

  uvicorn --reload riskanalysis.src.app:app


## With Docker-Compose:

  sudo docker-compose up
    
    - you may need to restart riskanalysis-mongo-express, if it starts earlier than riskanalysis-mongo
    - you may need to restart riskanalysis-api, if it tries to connect do riskanalysis-mongo or riskanalysis-neo4j before they finished starting

### Configuration riskanalysis-mongo

  following steps are easiest to fulfill with login into riskanalysis-mongo-express ({wherever_you_host}:8081)
  
  create database "RiskAnalysis"
  
  create collection "tilt" in "RiskAnalysis"
  
  create collection "riskScore" in "RiskAnalysis"
  
  insert TILT documents into "tilt"

## Call API:
  
  http localhost:8000/update
  
  http localhost:8000/update/{domain}
  
  http localhost:8000/{domain}
  
  http localhost:8000/calculate
  
  http localhost:8000/calculateRisks
  
  http localhost:8000/deleteGraph
  
  http localhost:8000/deleteProperties
  
  http localhost:8000/deleteCollection/{collectionName}
  
  http localhost:8000/generate/{i_TILTs}
