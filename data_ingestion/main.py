from fastapi import FastAPI
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Get database credentials from environment variables
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/dataflow_microservices"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)


@app.get("/")
async def read_root():
    """Default endpoint."""
    return "Hello world!"


@app.post("/load-data")
def load_data():
    """Endpoint for loading data from CSV into PostgreSQL."""
    try:
        # Read the CSV file
        df = pd.read_csv('housing_price_data.csv')

        # Preprocess boolean columns to convert 'yes'/'no' to True/False
        bool_columns = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
        for col in bool_columns:
            df[col] = df[col].map({'yes': True, 'no': False})

        # Insert data into PostgreSQL table
        df.to_sql(name='housing_price', con=engine, if_exists='replace', index=False)

        return {"message": f"Data loaded successfully.", "data_shape": df.shape}
    except SQLAlchemyError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
