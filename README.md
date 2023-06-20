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

- If you need to clean up the volumes to reset database, run"
  - docker volume rm llm-budget-assistant_postgres
  - docker volume rm llm-budget-assistant_pgadmin

# Tech stack

- **Frontend** : Discord/pycord
- **Database**: PostgreSQL
- **LLM**: GPT 3.5 (or other OpenAI model..)
- **Prompting management**: [Guardrails-ai](https://shreyar.github.io/guardrails/)
