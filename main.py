import yaml
import pandas as pd
from sqlalchemy import MetaData, Table, create_engine
import eodhd_
import logging
import sys
import db
import argparse
import products
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert

def update_historical_data(config, engine):
    stock_dfs = []
    for df in eodhd_.get_historical_data(config['stocks'], config['days']):
        stock_dfs.append(df)

    for df in stock_dfs:
        db.insert_dataframe(engine, 'stocks', df)
        db.prune_old_data(engine, 'stocks', config['days'])

def main():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('--create-tables', action='store_true', help='Create the tables in PostgreSQL if not exist')
    parser.add_argument('--update-stocks', action='store_true', help='Update historical data for stocks')
    parser.add_argument('--create-products', action='store_true', help='Update historical data for stocks')
    args = parser.parse_args()

    engine = db.setup_connection(config)

    if args.create_tables:
        db.create_tables(engine)
        sys.exit(0)

    if args.update_stocks:
        update_historical_data(config, engine)
        sys.exit(0)

    if args.create_products:
        products.distribution_of_returns(config, engine)

if __name__ == "__main__":
    main()
