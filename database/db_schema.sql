CREATE SCHEMA IF NOT EXISTS llm_finances;

-- Table: users
CREATE TABLE IF NOT EXISTS llm_finances.users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,

    UNIQUE (email)
);

-- Table: accounts
CREATE TABLE IF NOT EXISTS llm_finances.accounts (
    account_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES llm_finances.users(user_id),
    account_last_4_digits VARCHAR(4) NULL,
    account_name VARCHAR(50) NOT NULL,
    
    CONSTRAINT unique_account_name_per_user UNIQUE (user_id, account_name)
);

-- Table: categories
CREATE TABLE IF NOT EXISTS llm_finances.categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    user_id INT REFERENCES llm_finances.users(user_id),

    CONSTRAINT unique_category_per_user UNIQUE (user_id, category_name)
);

-- Table: transactions
CREATE TABLE IF NOT EXISTS llm_finances.transactions (
    transaction_id SERIAL PRIMARY KEY,
    transaction_date DATE NOT NULL,
    transaction_description VARCHAR(100) NOT NULL,
    credit DECIMAL(10, 2),
    debit DECIMAL(10, 2),
    account_id INT REFERENCES llm_finances.accounts(account_id),
    category_id INT REFERENCES llm_finances.categories(category_id),
    user_id INT REFERENCES llm_finances.users(user_id)
);
