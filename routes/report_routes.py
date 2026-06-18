from fastapi import APIRouter

from database.db_connection import DB_connection
from database.mission_db import MissionDB
from database.agent_db import AgentDB

from logger_config import logger

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

db = DB_connection()
mission_repository = MissionDB(db)
agent_repository = AgentDB(db)


@router.get("/summary")
def get_summary():
    summary = {
                "active_agents_count": agent_repository.count_active_agents(),
                "total_missions": mission_repository.count_all_missions(),
                "open_missions": mission_repository.count_open_missions(),
                "completed_missions": mission_repository.count_by_status("COMPLETED"),
                "failed_missions": mission_repository.count_by_status("FAILED"),
                "critical_missions": mission_repository.count_critical_missions()
                }
    
    return summary

@router.get("/missions-by-status")
def get_missions_by_status():
    summary = {
                "open": mission_repository.count_open_missions(),
                "in_progress":  mission_repository.count_by_status("IN_PROGRESS"),
                "completed": mission_repository.count_by_status("COMPLETED"),
                "failed":  mission_repository.count_by_status("FAILED"),
                "cacelled":  mission_repository.count_by_status("CANCELLED")
                }

    
    return summary

@router.get("/top-agent")
def get_top_agent():
    top_agent = mission_repository.get_top_agent()

    return top_agent
