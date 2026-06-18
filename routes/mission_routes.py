from fastapi import APIRouter, HTTPException

from database.db_connection import DB_connection
from database.mission_db import MissionDB
from database.agent_db import AgentDB

router = APIRouter(
    prefix="/missions",
    tags=["Missions"]
)

db = DB_connection()
mission_repository = MissionDB(db)
agent_repository = AgentDB(db)

@router.get("")
def get_all():
    return mission_repository.get_all_missions()

@router.get("/{id}")
def get_by_id(id):
    if isinstance(int(id), int) == False:
        raise HTTPException(status_code=422, detail="ID must by number")
    
    id = int(id)
    mission =  mission_repository.get_mission_by_id(id)
    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission

@router.post("", status_code=201)
def create_mission(data : dict):
    if "title" not in data.keys():
        raise HTTPException(status_code=422, detail="title required for new mission")
    if "description" not in data.keys():
        raise HTTPException(status_code=422, detail="description required for new mission")
    if "location" not in data.keys():
        raise HTTPException(status_code=422, detail="location required for new mission")
    if "difficulty" not in data.keys():
        raise HTTPException(status_code=422, detail="difficulty level required for new mission")
    if "importance" not in data.keys():
        raise HTTPException(status_code=422, detail="importance level required for new mission")
    if data["difficulty"] > 10:
        raise HTTPException(status_code=400, detail="difficulty level must be between 1-10")
    if data["difficulty"] < 1:
        raise HTTPException(status_code=400, detail="difficulty level must be between 1-10")
    if data["importance"] > 10:
        raise HTTPException(status_code=400, detail="importance level must be between 1-10")
    if data["importance"] < 1:
        raise HTTPException(status_code=400, detail="importance level must be between 1-10")
    
    new_mission = mission_repository.create_mission(data)

    return new_mission


@router.put("/{id}/assign/{agent_id}")
def assign_mission_to_agent(id, agent_id):
    if isinstance(int(id), int) == False:
        raise HTTPException(status_code=422, detail="ID must by number")
    
    id = int(id)
    mission =  mission_repository.get_mission_by_id(id)
    
    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")

    
    if isinstance(int(agent_id), int) == False:
        raise HTTPException(status_code=422, detail="ID must by number")
    
    agent_id = int(agent_id)
    agent =  agent_repository.get_agent_by_id(agent_id)
    
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    
    if mission["status"] != "NEW":
        raise HTTPException(status_code=400, detail="Mission not available")
    
    if not agent["is_active"]:
        raise HTTPException(status_code=400, detail="Agent is not active")
    
    if len(mission_repository.get_open_missions_by_agent(agent_id)) == 3:
        raise HTTPException(status_code=400, detail="Agent has reached maximum missions")
    
    if mission["risk_level"] == "CRITICAL" and agent["agent_rank"] != "Commander":
        raise HTTPException(status_code=400, detail="Only Commander can handle critical missions")
    
    return mission_repository.assign_mission(id, agent_id)

