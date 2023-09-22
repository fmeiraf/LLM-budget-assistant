# run_streamlit.py
import subprocess
from database import Database, db_config
from sqlalchemy import text

import os
from dotenv import load_dotenv

load_dotenv()

database = Database(**db_config)
DEFAULT_ADD_CREDITS = 3
DEFAULT_QUERY_CREDITS = 5


def start_streamlit():
    # run PostgreSQL triggers

    ## trigger SQL
    print("here1")
    trigger_function_sql = text(
        f"""
    CREATE OR REPLACE FUNCTION add_credit_on_user_insertion()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO llm_finances.credits(user_id, user_parsing_credit, user_query_credit)
        VALUES (NEW.user_id, {DEFAULT_ADD_CREDITS}, {DEFAULT_QUERY_CREDITS});
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """
    )

    trigger_sql = text(
        """
    CREATE TRIGGER trigger_add_credit
    AFTER INSERT ON llm_finances.users
    FOR EACH ROW
    EXECUTE FUNCTION add_credit_on_user_insertion();
    """
    )

    session = database.Session()
    session.execute(trigger_function_sql)
    session.execute(trigger_sql)
    try:
        session.commit()
    except Exception as e:
        print(e)
    # session.commit()
    session.close()

    # The command to run streamlit
    print("here")
    cmd = [
        "streamlit",
        "run",
        "app/Home.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
    ]
    # Use subprocess to run the command
    process = subprocess.Popen(cmd)

    # You can wait for the process to complete with the following line,
    # but this will block your script until the Streamlit server is terminated.
    process.wait()


if __name__ == "__main__":
    start_streamlit()
