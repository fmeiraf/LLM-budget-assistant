# LLM Budgeting Assistant

This is an attempt to create a budgeting assistant. This will be using LLMs to parse raw text I will grab from my account's online banking apps. This assistant will:

- Parse through credit card transations
- Assign categories based on transactions names (try to make this as consistent and flexible as possible)
- Split big inputs from customers that might exceed model max tokens limitations (i.e 4096 etc)
- Write me weekly or ad-hoc summaries about my spending trends
- Create a dashboard for me to check the data
- Provide tips on how I could save more money or achieve my goals

# Running it locally

This bot has the database and pgadmin running on separate (but connected) containers.

### For first set up or updates in the containeer

- Run:

  - docker-compose up -d

- If you need to clean up the volumes to reset database, run:
  - docker-compose down
  - docker volume rm llm-budget-assistant_pgadmin

### For updates in the enviroment specs

To make sure new changes in dependencies are correctly added to requirements ( and are easily usable afterwards..):

After new additions run:

`pip list --format=freeze > requirements.txt`

For fresh enviroment installations:

`pip install -r requirements.txt`
