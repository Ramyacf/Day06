
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.core.rate_limit import limiter
from app.modules.auth.router import router as auth_router
from app.modules.organizations.router import router as organizations_router
from app.modules.users.router import router as users_router
from app.modules.cases.router import router as cases_router


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

for router in (
    auth_router,
    organizations_router,
    users_router,
    cases_router,
):
    for route in router.routes:
        app.router.routes.append(route)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.app_name,
    }
