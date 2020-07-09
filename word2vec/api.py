from pydantic import BaseModel, Field
from typing import Optional
from fastapi import FastAPI, Query, Body, BackgroundTasks

from synonym import most_similar
from worker import worker_wakati_save


app = FastAPI()


@app.get('/')
def root():
    return {
        'status': 'ok'
    }


@app.get('/synonyms')
async def get_synonyms(
    model_path: Optional[str] = Query('save.model'),
    positive: Optional[str] = Query(...),
    negative: Optional[str] = Query(None)
):
    # 類似語を返す
    results = most_similar(
        model_path,
        positive,
        negative
    )

    return {
        'results': results
    }


class ValidatedInputData(BaseModel):
    keyword: str = Field(..., min_length=1)
    count: int = Field(..., gt=1)


@app.post('/synonyms')
async def create_synonyms(
    background_tasks: BackgroundTasks,
    data: ValidatedInputData = Body(..., embed=True)
):
    keyword = data.keyword
    count = data.count

    # worker処理
    background_tasks.add_task(
        worker_wakati_save,
        keyword,
        count
    )

    return {
        'results': data
    }
