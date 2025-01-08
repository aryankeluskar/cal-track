from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from database import get_daily_totals, add_food_entry

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    totals = get_daily_totals()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "calories": totals['calories'],
            "carbs": totals['carbs'],
            "protein": totals['protein']
        }
    )

@app.post("/add_manual")
async def add_manual(
    calories: float = Form(...),
    carbs: float = Form(...),
    protein: float = Form(...)
):
    try:
        add_food_entry(calories, carbs, protein)
        return {"success": True}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 