import uvicorn
from typing import List, Dict, TypedDict
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from useraccount import UserAccount, TransactionRecord, InSufficientPoints


class Message(BaseModel):
    message: str


app = FastAPI()
useracc = UserAccount()


# ROUTES -> add(PUT), balance(GET), spend(POST)

@app.get("/balance", response_model=Dict[str, int])
def balance() -> Dict[str, int]:
    return useracc.balance()


@app.put("/add", status_code=201, responses={
        200: {
            "description": "Successfully added given transactions"
        },
        405: {
            "description": "For a given payer, the spending transaction points is greater than added points",
            "model": Message,
        },
    },)
def addTransactions(transactions: List[TransactionRecord]) -> None:
    try:
        useracc.add(transactions)
    except InSufficientPoints as e:
        raise HTTPException(status_code=405, content={"message": str(e)})


@app.post(
    "/spend",
    response_model=Dict[str, int],
    responses={
        200: {
            "description": "Successfully spent the given amount",
            "model": Dict[str, int],
        },
        405: {
            "description": "InSufficient points to perform this action",
            "model": Message,
        },
    },
)
def spend(points: int):
    try:
        return useracc.spend(points)
    except InSufficientPoints as e:
        raise HTTPException(status_code=405, content={"message": str(e)})


if __name__ == "__main__":
    uvicorn.run(app, port=8001)
