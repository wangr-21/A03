from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

load_dotenv()

from .routers import (  # noqa: E402
    analysis,
    auth,
    cultural_corridor,
    homework,
    interactive,
    question_bank,
    students,
    style_transfer,
    teaching,
    user,
)

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")

for router in (
    teaching.router,
    analysis.router,
    homework.router,
    students.router,
    interactive.router,
    question_bank.router,
    cultural_corridor.router,
    style_transfer.router,
    user.router,
):
    app.include_router(router, prefix="/api", dependencies=[auth.RequireLogin()])


@app.get("/", response_class=RedirectResponse)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104
