from fastapi import APIRouter

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/{card_uid}")
async def read_user(card_uid: str):
    # TODO: DB dependency
    return card_uid
