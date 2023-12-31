# tradebook1
## Setup
```shell
$ ./docker.sh
$ python main.py --create-tables
```

## Running
```shell
python main.py --update-stocks
python main.py --create-products
```

## Configuration
### Adding stocks
Add additional stocks to `config.yaml`:
```yaml
stocks:
  - AAPL
  - MSFT
  ```