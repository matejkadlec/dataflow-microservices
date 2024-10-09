from fastapi import FastAPI, HTTPException
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
    return "Welcome to the Data Save API!"


@app.get("/save-data")
def save_data(data_type: str):
    """Endpoint to save transformed data to specified format."""
    # Validate format parameter
    valid_formats = ['csv', 'json', 'xml']
    if data_type not in valid_formats:
        raise HTTPException(status_code=400, detail="Invalid format. Choose from 'csv', 'json', or 'xml'.")

    try:
        # Load transformed data from PostgreSQL
        df = pd.read_sql("SELECT * FROM transformed_data", con=engine)

        # Save DataFrame to the specified format in the output directory
        output_path = os.path.join('/output_data', f'transformed_data.{data_type}')

        if data_type == 'csv':
            df.to_csv(output_path, index=False)
            return {"message": f"Transformed data saved to {output_path}"}
        elif data_type == 'json':
            df.to_json(output_path, orient='records', lines=True)
            return {"message": f"Transformed data saved to {output_path}"}
        elif data_type == 'xml':
            df.to_xml(output_path, index=False)
            return {"message": f"Transformed data saved to {output_path}"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
