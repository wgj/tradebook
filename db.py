from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float, Date
from sqlalchemy.dialects.postgresql import insert
from psycopg2.errors import UniqueViolation
import logging
from sqlalchemy.sql import text
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


def setup_connection(config):
    pg_user = config['database']['user']
    load_dotenv()
    pg_password = os.environ.get("POSTGRES_PASSWORD")
    pg_host = config['database']['host']
    pg_port = config['database']['port']
    pg_database = config['database']['database']
    
    return create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}')

def create_tables(engine):
    logger = logging.getLogger('main')
    metadata = MetaData()

    logging.info('Defining table `stocks`')
    stocks = Table(
    'stocks', metadata, 
    Column('date', Date, primary_key=True), 
    Column('symbol', String, primary_key=True), 
    Column('interval', String), 
    Column('open', Float), 
    Column('high', Float), 
    Column('low', Float),
    Column('close', Float), 
    Column('adjusted_close', Float), 
    Column('volume', Integer)
    )

    logging.info('Defining table `dor`')
    dor = Table(
    'dor', metadata, 
    Column('date', Date, primary_key=True), 
    Column('symbol', String, primary_key=True),
    # TODO(wgj): Decide if I like these column names.
    Column('C-C Returns', Float),
    Column('H-L Returns', Float),
    Column('O-C Returns', Float)
    )

    metadata.create_all(engine)

def insert_dataframe(engine, table, df):
    # Load the table details from the database
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables['stocks']

    _date = ''
    symbol = ''
    for index, row in df.iterrows():
        _date = index.date()
        symbol = row['symbol']
        insert_statement = insert(table).values(
            date=index.date(),
            symbol=row['symbol'],
            interval=row['interval'],
            open=row['open'],
            high=row['high'],
            low=row['low'],
            close=row['close'],
            adjusted_close=row['adjusted_close'],
            volume=row['volume']
        )
        do_nothing_statement = insert_statement.on_conflict_do_nothing(index_elements=['date', 'symbol'])
        
        logging.info(f'Inserting historical data for {symbol} on {_date}')

        try:
            with engine.begin() as connection:
                connection.execute(do_nothing_statement)
        except UniqueViolation:
            logging.warning('Duplicate key value, skipping insertion.')

def prune_old_data(engine, table, days):
    # calculate the date that is 90 days ago
    date_90_days_ago = datetime.now() - timedelta(days=days)
    query = f"DELETE FROM {table} WHERE date < '{date_90_days_ago.date()}'"
    with engine.begin() as connection:
        delete_statement = text(query)
        connection.execute(delete_statement)
