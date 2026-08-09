# Game-Recommendation-System

End-to-end machine learning project for recommending video games using **content-based filtering**, without relying on user data.  
The goal of this project is to recommend games similar to a given game, based purely on the game's own characteristics.

---

## 📌 Problem Statement

Traditional recommendation systems often rely on user interaction history (ratings, clicks, purchases).  
This isn't always available, especially for new platforms or new users (cold start problem).  
This project solves that by building a content-based recommender that suggests similar games based on the attributes of the game itself.

---

## 📊 Dataset

* Game data was collected via the RAWG API and stored in a raw JSON file
* Relevant features were extracted and loaded into a MySQL database
* Features include a mix of numerical, categorical and textual attributes (genres, tags, platforms, rating...)
* Data is processed through a full ingestion → cleaning → transformation pipeline before training

---

## 🏗️ Project Structure

```bash
Game-Recommendation-System/
│
├── artifacts/             # Saved model, preprocessor, vector and dataset
├── logs/                  # Logging files
├── api/
│   └── game_api.py        # Fetches game data from RAWG API and saves it to JSON
├── db/
│   ├── connection.py      # Handles connection to the MySQL database
│   ├── load_games.py      # Loads game data from JSON into the MySQL database
│   └── schema.sql         # SQL script for creating the database and tables
├── src/
│   ├── components/        # Data ingestion, cleaning, transformation, model training
│   ├── pipeline/          # Training and prediction pipelines
│   ├── utils.py           # Utility functions
│   ├── logger.py          # Logging configuration
│   ├── exception.py       # Custom exception
│
├── templates/             # HTML templates (FastAPI frontend with Bootstrap)
├── app.py                 # FastAPI application
├── config.py              # Loads environment variables using dotenv
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Machine Learning Pipeline

### The project follows a complete ML workflow:

1. Data ingestion from MySQL
2. Data cleaning and preprocessing
3. Feature transformation (ColumnTransformer with transformer weights):
    * SimpleImputer - handling missing values
    * StandardScaler - scaling numerical features
    * OneHotEncoder - encoding categorical features
    * TfidfVectorizer - vectorizing textual features (genres, platforms, tags)
4. Model training (NearestNeighbors)
5. Saving pipeline artifacts:
    * games_arr - vectorized representation of all games
    * model - trained NearestNeighbors model
    * preprocessor - fitted transformation pipeline
    * games_meta - game IDs and names, used for mapping predictions back to titles
6. Prediction pipeline for inference

---

## 🤖 Used Model

* NearestNeighbors is used to find the top 10 most similar games to a given input game based on vector similarity

---

## 📊 Results

The system doesn't rely on a formal evaluation metric.  
Recommendations were validated logically and manually, checking that suggested games make sense in terms of genre, tags and overall theme.

---

## 🚀 Deployment

The model is deployed using **FastAPI** with a simple web interface (HTML + Bootstrap).  
It also includes rate limiting using **SlowAPI** on the prediction endpoint.

---

## ▶️ How to Run the Project

### Prerequisites
Make sure you have installed:
* Docker
* Docker Desktop

### Clone the repository and install the required libraries:
```bash
git clone https://github.com/vidanbajc/Game-Recommendation-System.git
cd Game-Recommendation-System
```

### Create a .env file in the root directory with your API key and database credentials:
```bash
RAWG_API_KEY=your_api_key_here

DB_HOST=your_db_host
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_DATABASE=your_db_name
```

### Build and start the application:
```bash
docker compose up -d --build
```

### Load game data:
```bash
docker exec -it game-recommendation-api python -m db.load_games
```

### Open the application:
Open http://localhost:8000 in your browser

### Stop the application
```bash
docker compose down
```

---

## 🔮 Future Improvements

* Hybrid approach (content-based + collaborative filtering)
* Advanced feature engineering
* Cloud deployment

---

## 👤 Author

* Name: Vidan Bajc
* Email: <vidanbajc@gmail.com>