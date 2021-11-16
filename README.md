# RiskAnalysis

## With Docker & Server (Uvicorn):

  MongoClient: change host=MONGO['DOCKER'] to host=MONGO['HOST']
  
  Graph: change Graph(NEO4J['DOCKER_URI']) to Graph(NEO4J['URI'])

  sudo docker-compose up
  
  sudo docker stop riskanalysis-api

  uvicorn --reload riskanalysis.src.app:app


## With Docker-Compose:

  sudo docker-compose up
    
    - you may need to restart riskanalysis-mongo-express, if it starts earlier than riskanalysis-mongo
    - you may need to restart riskanalysis-api, if it tries to connect to riskanalysis-mongo or riskanalysis-neo4j before they finished starting

### Configuration riskanalysis-mongo

  following steps are easiest to fulfill with login into riskanalysis-mongo-express ({wherever_you_host}:8081)
  
  create database "RiskAnalysis"
  
  create collection "tilt" in "RiskAnalysis"
  
  create collection "riskScore" in "RiskAnalysis"
  
  insert TILT documents into "tilt"
  
  example TILTs can be found in: tilt-riskanalysis/riskanalysis/src/tilt/
  
  testing: call /generate/{i} to mock TILTs
  
  call /update to setup the databases

## Call API:
  
  http localhost:8000/update
  
  http localhost:8000/update/{domain}
  
  http localhost:8000/{domain}
  
  http localhost:8000/calculate
  
  http localhost:8000/calculateRisk/{domain}
  
  testing: http localhost:8000/deleteGraph
  
  testing: http localhost:8000/deleteProperties
  
  testing: http localhost:8000/deleteCollection/{collectionName}
  
  testing: http localhost:8000/generate/{i_TILTs}                   can be broken, if path changes
