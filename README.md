## Personal project to learn Docker basics.
#### Project consists of 3 microservices - one for loading data to a Postgre database, second to process them, and third to save the processed data.
### Stack:
- Python
- FastAPI
- Pandas
- SQLAlchemy
- PostgreSQL
- Docker
## To run this application on your PC:
1) Make sure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
2) Add **.env** file to the root folder with the following:
```yaml
POSTGRES_USER=<your_username>
POSTGRES_PASSWORD=<your_password>
POSTGRES_DB=<your_db>
```
3) Execute following command (from the root folder):
```bash
docker-compose up --build
```
4) Use [Postman](https://www.postman.com/) or similar program to call the API endpoints:
```bash
[POST] http://localhost:8000/load-data
[GET] http://localhost:8001/average-price-by-area
[GET] http://localhost:8001/price-distribution
[GET] http://localhost:8001/feature-correlation
[GET] http://localhost:8002/save-data?data_type=<csv/json/xml>
```
5) Processed data will be saved in the **output_data** folder