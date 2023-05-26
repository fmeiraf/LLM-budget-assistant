# LLM Budgeting Assistant

This is an attempt to create a budgeting assistant. This will be using LLMs to parse raw text I will grab from my account's online banking apps. This assistant will: 

- Parse through credit card transations
- Assign categories based on transactions names (try to make this as consistent and flexible as possible)
- Write me weekly or ad-hoc summaries about my spending trends
- Create a dashboard for me to check the data
- Provide tips on how I could save more money or achieve my goals

# Running as locally

### For first set up or updates in the containeer
- Run:
    - docker-compose up -d


# Tech stack

- **Frontend** : Discord
- **Database**: PostgreSQL
- **LLM**: GPT 3.5 (or other OpenAI model..)
- **Prompting management**: Guardrails

