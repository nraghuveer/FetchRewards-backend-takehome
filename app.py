import uvicorn
from typing import List, Dict, TypedDict
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from useraccount import UserAccount, TransactionRecord, InSufficientPoints


class Message(BaseModel):
    message: str


app = FastAPI()
useracc = UserAccount()


def my_schema():
    openapi_schema = get_openapi(
        title="Fetch Rewards - BackEnd - TakeHome",
        version="1.0",
        description="User Account",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# ROUTES -> add(PUT), balance(GET), spend(POST)


@app.get("/balance", response_model=Dict[str, int])
def balance() -> Dict[str, int]:
    return useracc.balance()


@app.put("/add")
def addTransactions(transactions: List[TransactionRecord]) -> None:
    useracc.add(transactions)


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
