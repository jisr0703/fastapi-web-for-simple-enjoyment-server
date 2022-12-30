from fastapi import APIRouter
from fastapi.responses import HTMLResponse
router = APIRouter()


@router.get('/', status_code=200)
async def index():
    print("index")
    return {'message': 'welcome to Web For Simple Enjoy'}
    # return HTMLResponse('<body><a href="/oauth/kakao">Log In</a></body>')