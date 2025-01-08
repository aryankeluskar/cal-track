from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from database import get_daily_totals, add_food_entry, get_food_entries, get_local_timezone
from datetime import datetime, timedelta

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/sprinkles-calories.svg")

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

@app.get("/get_food_log")
async def get_log():
    entries = get_food_entries()
    return entries

@app.get("/get_history")
async def get_history():
    # Get entries for the last 7 days
    entries = get_food_entries(limit=1000)  # Get more entries for aggregation
    
    # Group entries by date
    daily_totals = {}
    for entry in entries:
        date = entry['timestamp'].strftime('%Y-%m-%d')
        if date not in daily_totals:
            daily_totals[date] = {'calories': 0, 'date': date}
        daily_totals[date]['calories'] += entry['calories']
    
    # Get last 7 days
    today = datetime.now(get_local_timezone()).date()
    result = []
    for i in range(7):
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        result.append({
            'date': date,
            'calories': daily_totals.get(date, {'calories': 0})['calories']
        })
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 