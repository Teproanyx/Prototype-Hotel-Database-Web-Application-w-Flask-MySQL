# Prototype Hotel Management System

Using Flask backend with a MySQL database to implement a basic CRUD web application

## Instruction For Running This Server

1. Download Python 3.12, and all dependencies
2. Download MySQL, remember your root password
3. Download this codebase
4. Create an instance folder
5. Create a config.json file inside said folder
6. Inside the config file, the following config are needed to run this server on your localhost
`{
    "DATABASE": {
        "host": "localhost",
        "user": "root",
        "password": [INSERT YOUR MYSQL ROOT PASSWORD HERE]
    },
    "SECRET_KEY": [PUT IN ANY VALID STRING, JUST KEEP IT SECRET]
}`
7. In the root folder of project, run `flask --app manager init-db` followed by `flask --app manager ins-example` followed by `flask --app manager run`
8. Check your localhost; profit
