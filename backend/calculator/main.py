from fastapi import FastAPI
from fastapi.responses import JSONResponse

from backend.calculator.config import settings
from backend.calculator.web.router import router as calulator_router
from backend.calculator.domain.exceptions import (DivisionByZeroError, NegativeSquareRootError, NonFiniteResultError, ComplexResultError)


app = FastAPI(
    title=settings.app_name,
    description="REST API for basic and advanced calculations.",
    version="1.0.0",
)
app.include_router(calulator_router, prefix=settings.api_v1_prefix)

@app.exception_handler(Exception)
async def domain_exception_handler(request: Request, exc: Exception):
    domain_exceptions = (
        DivisionByZeroError,
        NegativeSquareRootError,
        NonFiniteResultError,
        ComplexResultError,
        ValueError 
    )
    
    if isinstance(exc, domain_exceptions):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc) or exc.__class__.__name__},
        )
    raise exc


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}