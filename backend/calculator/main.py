from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from calculator.config import settings
from calculator.web.router import router as calculator_router
from calculator.domain.exceptions import CalculatorError


app = FastAPI(
    title=settings.app_name,
    description="REST API for basic and advanced calculations.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.include_router(calculator_router, prefix=settings.api_v1_prefix)


@app.exception_handler(CalculatorError)
async def calculator_error_handler(request: Request, exc: CalculatorError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": exc.message})


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
