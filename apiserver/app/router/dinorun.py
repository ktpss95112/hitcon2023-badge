from datetime import datetime

from fastapi import APIRouter, BackgroundTasks

from ..dashboard import dashboard
from ..dependency import DBDep, GetUserDep
from ..model import DinorunRecord

router = APIRouter(
    prefix="/dinorun",
    tags=["dinorun"],
)


@router.get("/")
async def get_all_record(db: DBDep) -> list[DinorunRecord]:
    return await db.get_all_dinorun()


@router.get("/score")
async def get_all_score(db: DBDep) -> dict[str, float]:
    """
    The returned object is the mapping of card_uid to score.
    All the records of user who has a dinorun record will be returned.
    """
    return await db.get_all_dinorun_score()


@router.get("/{card_uid}/score")
async def get_score(user: GetUserDep, db: DBDep) -> float:
    return await db.get_dinorun_score_by_user(user)


@router.get("/{card_uid}/record")
async def get_record(user: GetUserDep, db: DBDep) -> list[DinorunRecord]:
    return await db.get_all_dinorun_by_user(user)


@router.post(
    "/{card_uid}",
)
async def submit_score(
    user: GetUserDep, db: DBDep, score: float, bg_task: BackgroundTasks
) -> bool:
    """
    The returned boolean indicates whether the submission is successful.
    """

    # be aware that the validity of score is not checked
    await db.new_dinorun(
        DinorunRecord(card_uid=user.card_uid, time=datetime.now(), score=score)
    )

    # push to frontend
    if not dashboard.disabled:
        score = await db.get_dinorun_score_by_user(user)
        bg_task.add_task(dashboard.create_or_update_dino, user.card_uid, score)

    return True


# TODO: endpoint for force pushing data to dashboard
