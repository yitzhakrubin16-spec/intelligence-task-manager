from fastapi import APIRouter, HTTPException

from database.db_connection import DB_connection
from database.agent_db import AgentDB

router = APIRouter(
    prefix="/agents",
    tags=["Agents"]
)

db = DB_connection()
agent_repository = AgentDB(db)

@router.get("")
def get_all():
    return agent_repository.get_all_agents()

@router.get("/{id}")
def get_by_id(id):
    if isinstance(int(id), int) == False:
        raise HTTPException(status_code=422, detail="ID must by number")
    
    id = int(id)
    agent =  agent_repository.get_agent_by_id(id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.post("", status_code=201)
def create_agent(data : dict):
    if "name" not in data.keys():
        raise HTTPException(status_code=422, detail="name required for new agent")
    if "specialty" not in data.keys():
        raise HTTPException(status_code=422, detail="specialty required for new agent")
    if "agent_rank" not in data.keys():
        data["agent_rank"] = "Junior"
    if data["agent_rank"] not in {"Junior", "Senior", "Commander"}:
        raise HTTPException(status_code=422, detail="Invalid Rank")
    
    new_agent = agent_repository.create_agent(data)

    return new_agent

@router.put("/{id}")
def update_agent(id, data : dict):
    if isinstance(int(id), int) == False:
        raise HTTPException(status_code=422, detail="ID must by number")

    id = int(id) 
    if agent_repository.get_agent_by_id(id) == None:
         raise HTTPException(status_code=404, detail="Agent not found")
    
    if "name" not in data.keys():
        raise HTTPException(status_code=422, detail="name required for updated agent")
    
    if "specialty" not in data.keys():
        raise HTTPException(status_code=422, detail="specialty required for updated agent")
    
    if "agent_rank" not in data.keys():
        raise HTTPException(status_code=422, detail="agent_rank required for updated agent")
    
    if data["agent_rank"] not in {"Junior", "Senior", "Commander"}:
        raise HTTPException(status_code=422, detail="Invalid Rank")
    
    
    agent_repository.update_agent(id, data)

@router.put("/{id}/deactivate")
def deactivate_agent(id):
    if isinstance(int(id), int) == False:
        raise HTTPException(status_code=422, detail="ID must by number")

    id = int(id) 
    if agent_repository.get_agent_by_id(id) == None:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent_repository.deactivate_agent(id)

@router.get("/{id}/performance")
def agent_performance(id):
    if isinstance(int(id), int) == False:
        raise HTTPException(status_code=422, detail="ID must by number")
    
    id = int(id) 
    if agent_repository.get_agent_by_id(id) == None:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return agent_repository.get_agent_performance(id)   