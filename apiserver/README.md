# API Server using FastAPI

## Environment

* Python 3.10.6
* [pdm](https://pdm.fming.dev/latest/#recommended-installation-method) 2.8.2

deprecated:
* [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) 20.23.0

## Run

```bash
# install dependencies
cd apiserver
pdm install

# start local dev server
cp .env.example .env  # and do some modification if needed
pdm run dev

# run staging server
pdm run staging

# run production server
pdm run prod

# run scripts in script/
# example:
#   pdm run python -m script.create_db
pdm run python -m script.FILENAME_WITHOUT_PY
```

## Dev

```bash
# add dependency
pdm add xxx

# formatter
pdm run lint

# pytest
pdm run test

# run any python scripts
pdm run python xxx.py
```

## Optional Commands

Please refer to `pyproject.toml` for all the available commands. (`pdm run create-db`, `pdm run build-docs`, ...)

```bash
# enter virtual env (but generally you don't need to)
eval `pdm venv activate`

# generate requirements.txt
pdm export -o requirements.txt --without-hashes
```
