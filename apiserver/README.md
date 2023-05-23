# API Server using FastAPI

## Environment

* Python 3.10.6
* [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) 20.23.0

## Dev / Run

```bash
# first time: create env
cd apiserver
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
deactivate

# enter env
source venv/bin/activate  # exit using `deactivate` later
black . # formatter
uvicorn main:app --reload

# exit venv
deactivate
```
