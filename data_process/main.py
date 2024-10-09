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
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@postgres-db:5432/{os.getenv('POSTGRES_DB')}"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)


@app.get("/")
async def read_root():
    """Default endpoint."""
    return "Welcome to the Data Transformation API!"


@app.get("/average-price-by-area")
def average_price_by_area():
    """Calculate average price by area."""
    try:
        # Load data from PostgreSQL
        df = pd.read_sql("SELECT * FROM housing_price", con=engine)

        avg_price = df.groupby("area")["price"].mean().reset_index()
        avg_price.columns = ['area', 'average_price']

        # Insert results into transformed_data table
        avg_price.to_sql(name='transformed_data', con=engine, if_exists='replace', index=False)

        return avg_price.to_dict(orient='records')
    except SQLAlchemyError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


@app.get("/price-distribution")
def price_distribution():
    """Get price distribution."""
    try:
        # Load data from PostgreSQL
        df = pd.read_sql("SELECT * FROM housing_price", con=engine)

        bins = [0, 5000000, 10000000, 15000000, 20000000, float('inf')]
        labels = ['<5M', '5M-10M', '10M-15M', '15M-20M', '>20M']

        df['price_range'] = pd.cut(df['price'], bins=bins, labels=labels)

        price_dist = df['price_range'].value_counts().reset_index()
        price_dist.columns = ['price_range', 'count']

        # Insert results into transformed_data table
        price_dist.to_sql(name='transformed_data', con=engine, if_exists='replace', index=False)

        return price_dist.to_dict(orient='records')
    except SQLAlchemyError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


@app.get("/feature-correlation")
def feature_correlation():
    """Analyze correlation between features."""
    try:
        # Load data from PostgreSQL
        df = pd.read_sql("SELECT * FROM housing_price", con=engine)

        # Drop non-numeric columns
        numeric_df = df.select_dtypes(include=['float64', 'int64'])

        # Calculate correlation
        correlation = numeric_df.corr()

        # Insert results into transformed_data table
        correlation.to_sql(name='transformed_data', con=engine, if_exists='replace', index=False)

        return correlation.to_dict(orient='records')
    except SQLAlchemyError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
