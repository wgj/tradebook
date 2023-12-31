from eodhd import APIClient
from datetime import datetime, timedelta
import logging

def get_historical_data(api_key, stocks, days):
    logger = logging.getLogger('main')
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    end_date = end_date.strftime('%Y-%m-%d')
    start_date = start_date.strftime('%Y-%m-%d')

    api = APIClient(api_key)

    # Get the data
    for stock in stocks:
        logger.info(f'Getting historical data for {stock} from {start_date} to {end_date}')
        resp = api.get_historical_data(stock, "d", start_date, end_date)
        yield resp
