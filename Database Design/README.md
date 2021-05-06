# cs6400-2021-01-Team032

## How to run LSRS locally

### Backend

First, install all python package dependencies:

```
pip install -r requirements.txt
```

Next, if this is your first time setting up LSRS to run locally, you should create a .env file in the top-level project directory with the following information:

```python
FLASK_APP = "lsrs_back_end.py"
user = "my_local_username" # your local postgres username
pw = "p@s$w0rd" # your local postgres password
host = "localhost"
port = "5433" # can also be 5432, depending on your settings
db = "lsrs" # or whatever you called your local lsrs database
```

You should now be able to run the back end REST API using the command:

```
flask run
```

### Frontend

TBA
