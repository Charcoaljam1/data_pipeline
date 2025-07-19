CREATE TABLE date_dim(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    date DATE NOT NULL,
    year INTEGER GENERATED ALWAYS AS (EXTRACT(YEAR FROM date)) STORED,
    quarter TEXT GENERATED ALWAYS AS ('Q'||(EXTRACT(QUARTER FROM date)::TEXT)) STORED,
    month INTEGER GENERATED ALWAYS AS (EXTRACT(MONTH FROM date)) STORED,
    week INTEGER GENERATED ALWAYS AS (EXTRACT(WEEK FROM date)) STORED,
    day TEXT
);

CREATE TABLE stock_fact(
    stock_metric_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id),
    date_id INTEGER NOT NULL REFERENCES date_dim(id),
    open_price DECIMAL(10,2) NOT NULL,
    close_price DECIMAL(10,2) NOT NULL,
    high_price DECIMAL(10,2) NOT NULL,
    low_price DECIMAL(10,2) NOT NULL,
    volume INTEGER,
    earnings_per_share DECIMAL(15,2),
    price_to_earnings_ratio DECIMAL(10,2),
    dividends_per_share DECIMAL(10,2),
    current_assets DECIMAL(15,2) NOT NULL,
    non_current_assets DECIMAL(15,2) NOT NULL,
    total_assets DECIMAL(15,2) NOT NULL,
    current_liabilities DECIMAL(15,2) NOT NULL,
    non_current_liabilities DECIMAL(15,2) NOT NULL,
    total_liabilities DECIMAL(15,2) NOT NULL,
    total_debt DECIMAL(15,2) NOT NULL,
    equity DECIMAL(15,2) NOT NULL,
    gross_income DECIMAL(15,2) NOT NULL,
    net_income DECIMAL(15,2) NOT NULL,
    profit_ratio DECIMAL(5,2) NOT NULL
);

