from fastapi import Depends, APIRouter, HTTPException, Request
from sqlalchemy.orm import Session
import uuid

from classes.Log import Log
from models.db import get_db
from models import crud, schemas

# Add logger
logging = Log(__name__).logger

router = APIRouter()

@router.get('/track/session_id/{dataset_id}')
async def get_sessionid(dataset_id: str, request: Request, db: Session = Depends(get_db)):
    try:

        session_id = str(uuid.uuid1())

        event = schemas.TrackEventSessionCreate(
            dataset_id=dataset_id,
            session_id=session_id,
            action=schemas.Event_Actions.SESSION_GEN.value,
            remote_addr=request.client.host
        )
        db_event = crud.create_session(db, event)

        return {
            'dataset_id': dataset_id,
            'session_id': session_id
        }, 200

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/track/view')
async def track_view(event: schemas.TrackEventViewCreate, request: Request, db: Session = Depends(get_db)):
    try:
        # Check if valid json
        event.remote_addr = request.client.host
        event.action = schemas.Event_Actions.PAGE_VIEW.value
        db_event = crud.create_event(db, event)

        return {'messages': 'o.k.'}, 200
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/track/click')
async def track_click(event: schemas.TrackEventCreate, request: Request, db: Session = Depends(get_db)):
    """ Track a click event

    Args:
        dataset_id: ID of the dataset
        event: TrackEventCreate

    Returns:
        200: Message: ok
        500: Message: error
    """
    try:
        event.remote_addr = request.client.host
        event.action = schemas.Event_Actions.CLICK.value
        db_event = crud.create_event(db, event)

        return {'message': 'ok'}, 200
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/track/{dataset_id}/{row_id}')
async def remove_track(dataset_id: str, row_id: int, db: Session = Depends(get_db)):
    """ Removes the entry of the given dataset and row

    Args:
        dataset_id: ID of the dataset
        row_id: row number of the dataset

    Returns:
        200: Message: ok
        500: Message: error
    """
    try:

        crud.delete_event(db, dataset_id, int(row_id))

        return {'message': 'ok'}, 200
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))
