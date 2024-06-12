#!/bin/bash

if [[ "$OSTYPE" == "msys" ]]; then
    python -m venv venv
    source venv\Scripts\activate
else
    python -m venv venv
    source venv/bin/activate
fi

pip install -r requirements.txt

python app/database.py

uvicorn app.main:app --reload