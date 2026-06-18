from fastapi import APIRouter, HTTPException

from database.db_connection import DB_connection
from database.agent_db import AgentDB

from logger_config import logger

router = APIRouter(
    prefix="/agents",
    tags=["Agents"]
)

db = DB_connection()
agent_repository = AgentDB(db)

@router.get("")
def get_all():
    logger.info("GET /agents called")
    try:
        logger.info("get all agents from table")
        agents = agent_repository.get_all_agents()
    except:
        logger.error("Error has occurred")
        return []
    logger.info("Return list of all agents")
    return agents

@router.get("/{id}")
def get_by_id(id):
    logger.info("GET /agents/{id} called")

    if isinstance(int(id), int) == False:
        raise HTTPException(status_code=422, detail="ID must by number")
    
    id = int(id)
    try:
        logger.info(f"get agent {id} from table")
        agent =  agent_repository.get_agent_by_id(id)
    except:
        logger.error("somthing went wrong")   
    
    if agent is None:
        logger.error(f"agent {id} does not exist")
        raise HTTPException(status_code=404, detail="Agent not found")
    
    logger.info(f"returning agent {id}")
    return agent

@router.post("", status_code=201)
def create_agent(data : dict):
    logger.info("POST /agents called")

    if "name" not in data.keys():
        logger.error("data for new agent missing")
        raise HTTPException(status_code=422, detail="name required for new agent")
    if "specialty" not in data.keys():
        logger.error("data for new agent missing")
        raise HTTPException(status_code=422, detail="specialty required for new agent")
    if "agent_rank" not in data.keys():
        logger.info("rank for new agent missing, setting default Junior")
        data["agent_rank"] = "Junior"
    
    if data["agent_rank"] not in {"Junior", "Senior", "Commander"}:
        logger.error("data for new agent: Invalid Rank")
        raise HTTPException(status_code=422, detail="Invalid Rank")
    try:
        logger.info("posting new agent")
        new_agent = agent_repository.create_agent(data)
    except:
        logger.error("Something went wrong")


    return new_agent

@router.put("/{id}")

def update_agent(id, data : dict):
    logger.info("PUT /agents/{id} called")

    if isinstance(int(id), int) == False:
        logger.error("agent id invalid")
        raise HTTPException(status_code=422, detail="ID must by number")

    id = int(id) 
    if agent_repository.get_agent_by_id(id) == None:
         logger.error(f"agent {id} does not exist")
         raise HTTPException(status_code=404, detail="Agent not found")
    
    if "name" not in data.keys():
        logger.error("data for update agent missing")
        raise HTTPException(status_code=422, detail="name required for updated agent")
    
    if "specialty" not in data.keys():
        logger.error("data for update agent missing")
        raise HTTPException(status_code=422, detail="specialty required for updated agent")
    
    if "agent_rank" not in data.keys():
        logger.error("data for update agent missing")
        raise HTTPException(status_code=422, detail="agent_rank required for updated agent")
    
    if data["agent_rank"] not in {"Junior", "Senior", "Commander"}:
        logger.error("data for update agent: Invalid Rank")
        raise HTTPException(status_code=422, detail="Invalid Rank")
    
    try:
        logger.info("Updating agent")
        agent_repository.update_agent(id, data)
    except:
        logger.error("something went wrong")
    return    

@router.put("/{id}/deactivate")
def deactivate_agent(id):
    logger.info("PUT /agents/{id}/deactivate called")
    if isinstance(int(id), int) == False:
        logger.error("agent id invalid")
        raise HTTPException(status_code=422, detail="ID must by number")

    id = int(id) 

    if agent_repository.get_agent_by_id(id) == None:
        logger.error(f"agent {id} does not exist")
        raise HTTPException(status_code=404, detail="Agent not found")
    try:
        logger.info("deactivating agent")
        agent_repository.deactivate_agent(id)
    except:
        logger.error("something went wrong")


@router.get("/{id}/performance")
def agent_performance(id):
    logger.info("PUT /agents/{id}/performance called")
    if isinstance(int(id), int) == False:
        logger.error("agent id invalid") 
        raise HTTPException(status_code=422, detail="ID must by number")
    
    id = int(id) 
    if agent_repository.get_agent_by_id(id) == None:
        logger.error(f"agent {id} does not exist")
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        logger.info("getting agent performances")
        return agent_repository.get_agent_performance(id) 
    except:
        logger.error("something went wrong")

    return