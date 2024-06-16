# Requirements

- Python > 3.11
- pyenv

Pyenv is used to install a Python environment where to install dependencies as local instead of in the global context of your machine. 

# Local Development

```bash
python3 -m venv .venv
./.venv/bin/python3 -m pip install --upgrade pip
./.venv/bin/python3 -m pip install -r requirements.txt
./.venv/bin/python3 -m flask run --host=0.0.0.0
```

Search the variable **DATABASE_HOST** in the `.env` file inside this folder and ensure yourself it is set to **localhost**.

# Enviroment variables

You can customize it in the `.env` file. Only required for local development.