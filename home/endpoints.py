from starlette.endpoints import HTTPEndpoint

from settings import templates


class HomeEndpoint(HTTPEndpoint):
    async def get(self, request):
        return templates.TemplateResponse("index.html", {"request": request})
