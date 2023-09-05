# LLM Budgeting Assistant

This is an attempt to create a finance/budgeting assistant. This will be using LLMs to parse raw text coming from account statements and feeding this into a database used for further analysis. Among the features on this app:

- Parse raw account transations
- Assign categories based on transactions names (try to make this as consistent and flexible as possible)
- Split big inputs from customers that might exceed model max tokens limitations (i.e 4096 etc)
- Simple dashboard for data visualization
- **_Enable user to talk to its own data through chat UI_**

# Example running on GCP

## Setting up first installation

- `sudo apt-get update -y`

- `sudo apt-get upgrade`

_Install Docker_

- `curl -fsSL https://get.docker.com -o get-docker.sh`

- `sudo sh get-docker.sh`

- `sudo usermod -aG docker {user}`

- `newgrp docker`

_Installing docker-compose_

- `sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
- `sudo chmod +x /usr/local/bin/docker-compose`

# Running it locally

The application is all built using docker containers. There are 3 containers, where pdadmin is only used for development.

- Run:

- Clone this repo

- Create .env file with the following format in the root directory:

```
OPENAI_API_KEY="..."
POSTGRES_PASSWORD="..."
POSTGRES_USER=".."
PGADMIN_DEFAULT_EMAIL="..."
PGADMIN_DEFAULT_PASSWORD="..."
DISCORD_BOT_TOKEN=".."
DISCORD_GUILD_ID=..
OPENAI_MODEL_NAME="gpt-3.5-turbo"
ENVIRONMENT="PROD"
```

- `docker-compose --profile (dev or prod) up -d --build --force-recreate`

- If you need to clean up the volumes to reset database, run:
  - `docker-compose down`
  - `docker volume rm llm-budget-assistant_pgadmin`

### For updates in the enviroment specs

To make sure new changes in dependencies are correctly added to requirements ( and are easily usable afterwards..):

After new additions run:

`pip list --format=freeze > requirements.txt`

For fresh enviroment installations:

`pip install -r requirements.txt`
