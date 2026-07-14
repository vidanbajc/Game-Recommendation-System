from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from src.pipeline.predict_pipeline import PredictPipeline

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/recommend")
def recommend(request: Request):
    return templates.TemplateResponse(request=request, name="recommend.html", context={"similar_games": []})


@app.post("/recommend")
def recommend_game(request: Request, game_name: str = Form(...)):
    
    recommendation_df = PredictPipeline.recommend(game_name)
    games = recommendation_df.to_dict(orient="records")

    return templates.TemplateResponse(request=request, name="recommend.html", context={"similar_games": games})