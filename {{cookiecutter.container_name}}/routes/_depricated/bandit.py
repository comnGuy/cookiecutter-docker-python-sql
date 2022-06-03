from fastapi import Depends, APIRouter, HTTPException, Request
from sqlalchemy.orm import Session

from classes.Log import Log
from models.db import get_db
from models import crud, schemas
from models.schemas import CandidateImpressions, Dump

# Add logger
logging = Log(__name__).logger

router = APIRouter()


@router.get('/bandit/{dataset_id}/{row_id}', response_model=CandidateImpressions)
async def get_stats_bandit_candidate(dataset_id: str, row_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_stats_bandit_candidate(db, dataset_id, row_id), 200
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/bandit/baseline/{dataset_id}', response_model=CandidateImpressions)
async def get_stats_bandit_baseline(dataset_id: str, indices: schemas.BaselineIndices, db: Session = Depends(get_db)):
    try:
        return crud.get_stats_bandit_baseline(db, dataset_id, indices)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/dump/{dataset_id}', response_model=Dump)
async def get_dump(dataset_id: str, db: Session = Depends(get_db)):
    try:
        return crud.get_dump(db, dataset_id)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))
