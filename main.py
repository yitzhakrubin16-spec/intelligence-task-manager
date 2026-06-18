from database.db_connection import DB_connection
from fastapi import FastAPI
from routes import agent_routes, mission_routes, report_routes
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s",
                    handlers=[logging.StreamHandler(),
                            logging.FileHandler("./logs/app.log")])


logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(agent_routes.router)
app.include_router(mission_routes.router)

db = DB_connection()

db.create_database()
db.create_tables()

