# API Server using FastAPI

## Environment

* Python 3.10.6
* [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) 20.23.0
* [pdm](https://pdm.fming.dev/latest/#recommended-installation-method)

## Run

```bash
# install dependencies
cd apiserver
pdm install

# start local dev server
pdm run dev

# run staging server
pdm run staging
```

## Dev

```bash
# add dependency
pdm add xxx

# formatter
pdm run lint

# run any python scripts
pdm run python xxx.py
```

## Optional Commands
```bash
# enter virtual env (you don't need to)
eval `pdm venv activate`

# generate requirements.txt
pdm export -o requirements.txt --without-hashes
```
