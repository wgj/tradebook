import pandas as pd

def distribution_of_returns(config, engine):
    df = pd.read_sql_table('stocks', engine)
    df = df.set_index(['symbol', 'date'])
    df = df.sort_index()
    # TODO(wgj): Figure out whether a value should look like `0.01502133`, `0.015`, or `1.50%`
    df['C-C Returns'] = df.groupby('symbol')['adjusted_close'].pct_change()
    df['H-L Returns'] = (df['low'] - df['high']) / df['high']
    df['O-C Returns'] = (df['close'] - df['open']) / df['open']
    df = df.dropna()
    df = df.reset_index()
    df = df.set_index(['symbol', 'date'])
    df = df.sort_index()
    df = df.drop(columns=['interval', 'open', 'high', 'low', 'close', 'adjusted_close', 'volume'])
    df.to_sql('dor', engine, if_exists='replace')
