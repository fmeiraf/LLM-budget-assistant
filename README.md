# LLM Budgeting Assistant

_Live at:_ 💸 [**banqstream.com**](banqstream.com)

This is an attempt to create a finance/budgeting assistant. This will be using LLMs to parse raw text coming from account statements and feeding this into a database used for further analysis. Among the features on this app:

- Parse raw account transations
- Assign categories based on transactions names (try to make this as consistent and flexible as possible)
- Split big inputs from customers that might exceed model max tokens limitations (i.e 4096 etc)
- Simple dashboard for data visualization
- **_Enable user to talk to its own data through chat UI_**

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

# Running on GCP (or other cloud services)

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

_Add firewall rule_

- Make sure you have a TCP firewall rule set up for the same port used by streamlit (default is 8501)

_Making custom domain to work_

Instal nginx ([for more reference](https://www.alibabacloud.com/blog/using-lets-encrypt-to-enable-https-for-a-streamlit-web-service_600130)):

- `sudo apt-get install nginx`
- `sudo nano /etc/nginx/sites-available/default`
  - Add this to the file above
  - ````server {
        listen       80;
        server_name  47.74.21.181; # Domain name or IP address
        location / {
            proxy_pass http://0.0.0.0:8501/; # Route from HTTP port 80 to Streamlit port 8501
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }```
    ````

Installing SSL:

- `sudo apt install certbot python3-certbot-nginx`
- `sudo certbot --nginx -d ＜Domain＞`

### For updates in the enviroment specs

To make sure new changes in dependencies are correctly added to requirements ( and are easily usable afterwards..):

After new additions run:

`pip list --format=freeze > requirements.txt`

For fresh enviroment installations:

`pip install -r requirements.txt`
