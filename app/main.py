from fastapi import FastAPI, Request, Form
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.templating import Jinja2Templates
from src.pipeline.predict_pipeline import PredictPipeline

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
templates = Jinja2Templates(directory="app/frontend/templates")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/recommend")
def recommend(request: Request):
    return templates.TemplateResponse(request=request, name="recommend.html", context={"similar_games": []})


@app.post("/recommend")
@limiter.limit("50/minute")
def recommend_game(request: Request, game_name: str = Form(...)):

    try:
        recommendation_df = PredictPipeline.recommend(game_name)
        games = recommendation_df.to_dict(orient="records")

        return templates.TemplateResponse(request=request, name="recommend.html", context={"similar_games": games, "error":None, "game_name": game_name})
    
    except ValueError as e:
        return templates.TemplateResponse(request=request, name="recommend.html", context={"similar_games": [], "error":str(e), "game_name": game_name})
    