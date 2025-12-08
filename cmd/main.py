from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import auth, storage, units, orders, budgets , unit_user, user, frequency, report
import os
from dotenv import load_dotenv
load_dotenv()


app = FastAPI(
    title="UNAS Finance API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(storage.router, prefix="/storage", tags=["storage"])
app.include_router(units.router, prefix="/units", tags=["units"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(unit_user.router, prefix="/user-unit", tags=["user-unit"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
app.include_router(report.router, prefix="/reports", tags=["reports"])
app.include_router(frequency.router, prefix="/frequency", tags=["frequency"])

@app.get("/", tags=["infra"])
async def healthcheck():
    return {"status": "ok"}



@app.on_event("startup")
async def startup_event():
    if os.getenv("ENVIRONMENT")  == "prod":
        from services.auth_service import AuthService
        print("🔥 Iniciando API UNAS… verificando usuário admin...")
        await AuthService.initialize_admin_user()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("cmd.main:app", host="0.0.0.0", port=8000, reload=True)
