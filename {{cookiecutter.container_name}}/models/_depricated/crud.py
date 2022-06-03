from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from models import models, schemas
from models.models import TrackEvent, Event_Actions
from models.schemas import CandidateImpressions, BaselineIndices, Dump


def create_session(db: Session, event: schemas.TrackEventSessionCreate):
    db_event = models.TrackEvent(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def create_event(db: Session, event: schemas.TrackEventCreate):
    db_event = models.TrackEvent(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, dataset_id: str, index: int):
    db.query(
        models.TrackEvent.id
    ).filter(and_(
        models.TrackEvent.dataset_id == dataset_id,
        models.TrackEvent.index == index,
        models.TrackEvent.action != schemas.Event_Actions.SESSION_GEN.value)
    ).delete()
    db.commit()


def stats_for_dataset(db: Session, dataset_id: str):
    # Check if valid json
    '''
    stats = {
        'dataset_id': dataset_id,
        'tests': [],
        'all': {
            'conversion_rates': {},
            Event_Actions.PAGE_VIEW.value: 0
        }        
    }
    '''
    stats = schemas.StatisticDatasetOut()
    stats.dataset_id = dataset_id

    for index, element_label, action, count in \
        db.query(models.TrackEvent.index, models.TrackEvent.element_label, models.TrackEvent.action, func.count(models.TrackEvent.action))\
        .filter(and_(models.TrackEvent.dataset_id == dataset_id, models.TrackEvent.action != schema.Event_Actions.SESSION_GEN.value))\
        .group_by(models.TrackEvent.element_label, models.TrackEvent.test_index, models.TrackEvent.action)\
        .order_by(models.TrackEvent.index)\
            .all():
        # test
        test = None  # schemas.StatisticTests()
        if len(stats['tests']) > index:
            # elemet is already added
            test = stats.tests[index]
        else:
            # adding a new test element
            test = schemas.StatisticTests()
            '''
            test = {
                'index': index,
                'element_label': '',
                schema.Event_Actions.PAGE_VIEW.value: 0,
                'conversion_rates': {}
            }
            '''
            test.page_view = 0

            stats.tests.append(test)

        print(element_label)

        if action == schema.Event_Actions.PAGE_VIEW.value:
            test.page_view = count
            stats.all.page_view = stats.all.page_view + count
            for key in test['conversion_rates']:
                test.conversion_rates[key] = test[key]/count
                stats['all']['conversion_rates'][key] = stats['all'][key] / \
                    stats['all'][schema.Event_Actions.PAGE_VIEW.value]
        else:
            test[action] = count
            test.update({'element_label': element_label})
            stats['all'][action] = stats['all'].get(action, 0) + count
            if test[schema.Event_Actions.PAGE_VIEW.value] > 0:
                test['conversion_rates'][action] = count / \
                    test[schema.Event_Actions.PAGE_VIEW.value]
                stats['all']['conversion_rates'][action] = stats['all'].get(
                    action, 0)/stats['all'][schema.Event_Actions.PAGE_VIEW.value]
            else:
                test['conversion_rates'][action] = -1
                stats['all']['conversion_rates'][action] = -1

    return jsonify(stats)


def get_stats_bandit_candidate(db: Session, dataset_id: str, row_id: int):
    query_result = db.query(
        TrackEvent.action,
        func.count(TrackEvent.action)
    ).filter(and_(
        TrackEvent.dataset_id == dataset_id,
        TrackEvent.action != Event_Actions.SESSION_GEN.value,
        TrackEvent.index == row_id)
    ).group_by(
        TrackEvent.element_label,
        TrackEvent.index,
        TrackEvent.action
    ).order_by(
        TrackEvent.index
    ).all()

    ci = CandidateImpressions()

    if not query_result:
        return ci

    for action, count in query_result:
        ci[action] += count
        # template[action] += count

    return ci


def get_stats_bandit_baseline(db: Session, dataset_id: str, indices: BaselineIndices) -> CandidateImpressions:
    indices = indices.indices

    # Query for min/max dates
    query_result = db.query(
        func.min(TrackEvent.creation_time),
        func.max(TrackEvent.creation_time),
    ).filter(and_(
        TrackEvent.dataset_id == dataset_id,
        TrackEvent.index.in_(indices),
        TrackEvent.action == 'page_view',
        TrackEvent.action != Event_Actions.SESSION_GEN.value)
    ).group_by(
        TrackEvent.element_label,
        TrackEvent.index,
        TrackEvent.action
    ).order_by(
        TrackEvent.index
    ).all()

    ci = CandidateImpressions()

    # If the query is empty
    if not query_result:
        return ci

    # Get the min/max date
    min_date, max_date = None, None
    for item in query_result:
        # Get min date
        if min_date != None:
            if item[0] < min_date:
                min_date = item[0]
        else:
            min_date = item[0]

        # Get max date
        if max_date != None:
            if item[1] > max_date:
                max_date = item[1]
        else:
            max_date = item[1]

    if min_date > max_date:
        raise Exception('Minimal date is greater then maximal date.')

    # Query for the views/clicks
    query_result = db.query(
        TrackEvent.action,
        func.count(TrackEvent.action)
    ).filter(and_(
        TrackEvent.dataset_id == dataset_id,
        TrackEvent.action != Event_Actions.SESSION_GEN.value,
        TrackEvent.index == -1,
        TrackEvent.creation_time >= min_date,
        TrackEvent.creation_time <= max_date)
    ).group_by(
        TrackEvent.element_label,
        TrackEvent.index,
        TrackEvent.action
    ).order_by(
        TrackEvent.index
    ).all()

    if not query_result:
        return ci

    for action, count in query_result:
        ci[action] += count
        # template[action] += count

    return ci


def get_dump(db: Session, dataset_id: str) -> Dump:
    query_result = db.query(
        TrackEvent.index,
        TrackEvent.element_label,
        TrackEvent.action
    ).filter(and_(
        TrackEvent.dataset_id == dataset_id,
        TrackEvent.action != Event_Actions.SESSION_GEN.value)
    ).all()
    return Dump(dump=query_result)
