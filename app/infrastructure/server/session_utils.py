from aiohttp_session import get_session

from app.infrastructure.app_constants import SESSION_ID_KEY


async def identify_session(request):
    session = await get_session(request)
    return session.get(SESSION_ID_KEY)


async def register_session(request, identity):
    session = await get_session(request)
    session[SESSION_ID_KEY] = identity


async def forget_session(request):
    session = await get_session(request)
    session.pop(SESSION_ID_KEY, None)
