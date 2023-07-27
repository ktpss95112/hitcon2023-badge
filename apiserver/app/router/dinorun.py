from datetime import datetime

from fastapi import APIRouter, BackgroundTasks

from ..dashboard import dashboard
from ..dependency import DBDep, GetDinorunDep

router = APIRouter(
    prefix="/dinorun",
    tags=["dinorun"],
)


@router.get("/")
async def get_all(db: DBDep) -> dict[str, float]:
    """
    The returned object is the mapping of card_uid to score.
    All the records of user who has a dinorun record will be returned.
    """
    all_record = await db.get_all_dinorun()
    ret = {record.card_uid: record.get_best_score() for record in all_record}
    return ret


@router.get("/{card_uid}")
async def get_score(record: GetDinorunDep) -> float:
    return record.get_best_score()


@router.post(
    "/{card_uid}",
)
async def submit_score(
    record: GetDinorunDep, db: DBDep, score: float, bg_task: BackgroundTasks
) -> bool:
    """
    The returned boolean indicates whether the submission is successful.
    """

    # be aware that the validity of score is not checked
    record.add_record(datetime.now(), score)
    await db.write_dinorun(record)

    # push to frontend
    if not dashboard.disabled:
        bg_task.add_task(
            dashboard.create_or_update_dino, record.card_uid, record.get_best_score()
        )

    return True
