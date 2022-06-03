from fastapi import Depends, APIRouter, HTTPException, Request
from sqlalchemy.orm import Session

from classes.Log import Log
from models.db import get_db
from models import crud, schemas

# Add logger
logging = Log(__name__).logger

router = APIRouter()

@router.get('/stats/{dataset_id}', response_model=UserOut)
async def get_stats_for_dataset(dataset_id: str, db: Session = Depends(get_db)):
    try:
        stats = crud.get_stats_for_dataset(db, dataset_id)

        return stats, 200
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))
