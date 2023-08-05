from datetime import datetime

from fastapi import APIRouter, HTTPException

from ..dependency import DBDep, GetUserDep
from ..model import ActivityDate, CryptoRedeemRecord

router = APIRouter(
    prefix="/crypto",
    tags=["crypto"],
)


@router.get("/")
async def get_all_record(db: DBDep) -> list[CryptoRedeemRecord]:
    return await db.get_all_crypto_redeem()


@router.get("/user/{card_uid}/date/{date}")
async def get_record_by_user_and_date(
    user: GetUserDep, db: DBDep, date: ActivityDate
) -> CryptoRedeemRecord | None:
    return await db.get_crypto_redeem_by_user_and_date(user, date)


@router.post("/user/{card_uid}/date/{date}")
async def redeem_award(user: GetUserDep, db: DBDep, date: ActivityDate) -> bool:
    record = await db.get_crypto_redeem_by_user_and_date(user, date)
    if record is not None:
        raise HTTPException(400, "Already redeemed!")

    record = CryptoRedeemRecord(card_uid=user.card_uid, date=date, time=datetime.now())
    await db.new_crypto_redeem(record)
    return True
