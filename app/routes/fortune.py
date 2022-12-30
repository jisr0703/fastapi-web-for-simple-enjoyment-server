import random
from fastapi import APIRouter, Depends, Response, Request
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models.common import Feeling
from app.database.schema import IPs, Feelings, FeelingsLog
from app.database.conn import db
router = APIRouter()


@router.get('/')
async def fortune_index():
    return dict(message='here is fortune')


@router.get('/checking')
async def fortune_checking(response: Response, request: Request):
    return dict(key='hi', val='here is fortune checking')


@router.get('/checking/test/{feeling_id}')
async def fortune_checking(response: Response, request: Request, feeling_id: Feeling):
    feeling = Feelings().get(id=feeling_id.Happiness)
    return dict(id=f'{feeling.id}', feeling=f'{feeling.feeling}')

#
# @router.get('/result/{ip}', status_code=201)
# async def fortune_result(response: Response, request: Request, ip: str, session: Session = Depends(db.session)):
#     ip_row = IPs.get(ip=ip)
#     if ip_row is None:
#         ip_row = IPs.create(session, auto_commit=True, ip=ip)
#     feelings_res_row = FeelingsLog.get(ip_id=ip_row.id)
#     if feelings_res_row is None:
#         feel = random.choices(range(1, 4), weights=[6.8, 1.2, 2.0])[0]
#         feelings_res_row = FeelingsLog.create(session, auto_commit=True, ip_id=ip_row.id, feeling_id=feel)
#         if is_feeling_exist(feel):
#             return dict(feeling=f'feeling_id: {feelings_res_row.feeling_id}', exist=False)
#     if is_feeling_exist(feelings_res_row.feeling_id):
#         return dict(feeling=f'feeling_id: {feelings_res_row.feeling_id}', exist=True)
#     return JSONResponse(status_code=400, content=dict(msg="INVALID_REQUEST"))
#
#
# def is_feeling_exist(response: Response, request: Request, feeling: int) -> bool:
#     for f in Feeling:
#         if f.value == feeling:
#             return True
#     return False
