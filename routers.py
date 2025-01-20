
from typing import Annotated, Union

from fastapi import APIRouter, Header, HTTPException, Depends, Response
from sqlmodel import select

from database import SessionDepends
from integrations import WhatsappIntegrationBase, WhatsappIntegrationConfirmation, HelloWorldIntegrationConfirmation
from models import Account, AccountLimit, Message
from schemas import ConfirmBodySchema


router = APIRouter()


def get_confirm_integration():
    return WhatsappIntegrationConfirmation()

@router.post("/send/confirmation", tags=["sending"])
async def confirmation(session: SessionDepends,
                  body: ConfirmBodySchema,
                  confirm_integration: WhatsappIntegrationBase = Depends(get_confirm_integration),
                  access_token: Annotated[Union[str, None], Header()] = None,
                  ):

    statement = select(Account).where(Account.secret == access_token)
    account = session.exec(statement).one_or_none()

    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    statement = select(AccountLimit).where(AccountLimit.account_id == account.id)
    limits = list(session.exec(statement))

    if len(limits) > 0:
        limit = limits[0]
        statement = select(Message).where(Message.account_id == limit.account_id)
        messages = session.exec(statement)
        if len(messages) >= limit.limit_of_message:
            raise HTTPException(status_code=404, detail="Message limit reached")

    result = confirm_integration.send(body.to, {
        'text': body.text
    })

    if result.status_code == 200:
        return result.json()

    return result.json()
