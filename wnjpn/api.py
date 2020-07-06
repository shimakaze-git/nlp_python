from typing import Optional
from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def root():
    return {
        'status': 'ok'
    }


@app.get('/synonyms')
def get_synonyms(q: Optional[str] = None):
    return {
        'q': q
    }
