# Documentation settings
SWAGGERUI_URL = '/swagger'
SCHEMA_URL = '/static/swagger.json'
PAGE_TITLE = 'Falcon api Swagger Doc'
FAVICON_URL = 'https://falconframework.org/favicon-32x32.png'

# MongoDB datasource constant
MONGO = {
    'DATABASE': 'tilt',
    'HOST': 'localhost',
    'DOCKER': 'riskanalysis-mongo',
    'PORT': 27017,
    'USERNAME': 'root',
    'PASSWORD': 'SuperSecret',
    'AUTHENTICATION_SOURCE': 'admin'
}

# Neo4j datasource constant
NEO4J = {
    'DOCKER_URI': 'neo4j://riskanalysis-neo4j:7687',
    'URI': 'neo4j://localhost:7687',
    'Username': 'neo4j',
    'Password': 'test'
}