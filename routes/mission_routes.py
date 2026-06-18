from fastapi import APIRouter, HTTPException

from database.db_connection import DB_connection
from database.mission_db import MissionDB
from database.agent_db import AgentDB

from logger_config import logger


router = APIRouter(
    prefix="/missions",
    tags=["Missions"]
)

db = DB_connection()
mission_repository = MissionDB(db)
agent_repository = AgentDB(db)

@router.get("")
def get_all():
    logger.info("GET /missions called")
    try:
        logger.info("get all missions from table")
        missions = mission_repository.get_all_missions()
    except:
        logger.error("Error has occurred")
        return []
    logger.info("Return list of all missions")
    return missions

@router.get("/{id}")
def get_by_id(id):
    logger.info("GET /missions/{id} called")
    if isinstance(int(id), int) == False:
        raise HTTPException(status_code=422, detail="ID must by number")
    
    id = int(id)
    try:
        logger.info(f"get mission {id} from table")
        mission =  mission_repository.get_mission_by_id(id)
    except:
        logger.error("Error has occurred")
        return []

    if mission is None:
        logger.error(f"mission {id} does not exist")
        raise HTTPException(status_code=404, detail="Mission not found")
    logger.info(f"returning mission {id}")
    return mission

@router.post("", status_code=201)
def create_mission(data : dict):
    logger.info("/POST /mission called")
   
    if "title" not in data.keys():
        logger.error("data for new mission missing")
        raise HTTPException(status_code=422, detail="title required for new mission")
    
    if "description" not in data.keys():
        logger.error("data for new mission missing")
        raise HTTPException(status_code=422, detail="description required for new mission")
    
    if "location" not in data.keys():
        logger.error("data for new mission missing")
        raise HTTPException(status_code=422, detail="location required for new mission")
    
    if "difficulty" not in data.keys():
        logger.error("data for new mission missing")
        raise HTTPException(status_code=422, detail="difficulty level required for new mission")
    
    if "importance" not in data.keys():
        logger.error("data for new mission missing")
        raise HTTPException(status_code=422, detail="importance level required for new mission")
    
    if data["difficulty"] > 10:
        logger.error("data for new mission invalid")
        raise HTTPException(status_code=400, detail="difficulty level must be between 1-10")
    
    if data["difficulty"] < 1:
        logger.error("data for new mission invalid")
        raise HTTPException(status_code=400, detail="difficulty level must be between 1-10")
    
    if data["importance"] > 10:
        logger.error("data for new mission invalid")
        raise HTTPException(status_code=400, detail="importance level must be between 1-10")
    
    if data["importance"] < 1:
        logger.error("data for new mission invalid")
        raise HTTPException(status_code=400, detail="importance level must be between 1-10")
    
    try:
        logger.info("posting new mission")
        new_mission = mission_repository.create_mission(data)
    except:
        logger.error("posting failed")
        return
    
    logger.info("new mission posted successfully")
    return new_mission


@router.put("/{id}/assign/{agent_id}")
def assign_mission_to_agent(id, agent_id):
    logger.info("/PUT /mission/{id}/assign/{agent_id} called")

    if isinstance(int(id), int) == False:
        logger.error("mission id invalid")
        raise HTTPException(status_code=422, detail="ID must by number")
    
    id = int(id)
    mission =  mission_repository.get_mission_by_id(id)
    
    if mission is None:
        logger.error(f"mission {id} does not exist")
        raise HTTPException(status_code=404, detail="Mission not found")

    
    if isinstance(int(agent_id), int) == False:
        logger.error("mission id invalid")
        raise HTTPException(status_code=422, detail="ID must by number")
    
    agent_id = int(agent_id)
    agent =  agent_repository.get_agent_by_id(agent_id)
    
    if agent is None:
        logger.error(f"agent {id} does not exist")
        raise HTTPException(status_code=404, detail="Agent not found")
    
    
    if mission["status"] != "NEW":
        logger.error("mission status is not New")
        raise HTTPException(status_code=400, detail="Mission not available")
    
    if not agent["is_active"]:
        logger.error("agent is not active")
        raise HTTPException(status_code=400, detail="Agent is not active")
    
    if len(mission_repository.get_open_missions_by_agent(agent_id)) == 3:
        logger.error("agents holds the max of open missions")
        raise HTTPException(status_code=400, detail="Agent has reached maximum missions")
    
    if mission["risk_level"] == "CRITICAL" and agent["agent_rank"] != "Commander":
        logger.error("agents rank is not high enough for this mission")
        raise HTTPException(status_code=400, detail="Only Commander can handle critical missions")
    try:
        logger.info("Updating mission")
        return mission_repository.assign_mission(id, agent_id)
    except:
        logger.error("somthing went wrong")

    return


@router.put("/{id}/start")
def start_mission(id:int):
    logger.info("/PUT /mission/{id}/start called")

    mission =  mission_repository.get_mission_by_id(id)
    
    if mission is None:
        logger.error(f"mission {id} does not exist")
        raise HTTPException(status_code=404, detail="Mission not found")
    
    if mission["status"] == "ASSIGNED":
        try:
            mission_repository.update_mission_status(id, "IN_PROGRESS")
        except:
            logger.error("somthing went wrong")
    else:
        logger.error("mission status is not not ASSIGNED")
        raise HTTPException(status_code=400, detail="Can only start ASSIGNED mission")


@router.put("/{id}/complete")
def complete_mission(id:int):
    logger.info("/PUT /mission/{id}/complete called")
    mission =  mission_repository.get_mission_by_id(id)
    
    if mission is None:
        logger.error(f"mission {id} does not exist")
        raise HTTPException(status_code=404, detail="Mission not found")
    
    if mission["status"] == "IN_PROGRESS":
        try:
            mission_repository.update_mission_status(id, "COMPLETED")
            agent_repository.increment_completed(mission["assigned_agent_id"])
        except:
            logger.error("somthing went wrong")
    else:
        logger.error("mission status is not not IN_PROGRESS")
        raise HTTPException(status_code=400, detail="Can only complete IN_PROGRESS mission")

@router.put("/{id}/fail")
def fail_mission(id:int):
    logger.info("/PUT /mission/{id}/fail called")
    mission =  mission_repository.get_mission_by_id(id)
    
    if mission is None:
        logger.error(f"mission {id} does not exist")
        raise HTTPException(status_code=404, detail="Mission not found")
    
    if mission["status"] == "IN_PROGRESS":
        try:
            mission_repository.update_mission_status(id, "FAILED")
            agent_repository.increment_failed(mission["assigned_agent_id"])
        except:
            logger.error("somthing went wrong")    
    else:
        logger.error("mission status is not not IN_PROGRESS")
        raise HTTPException(status_code=400, detail="Can only fail IN_PROGRESS mission")

              
                     
@router.put("/{id}/cancel")
def cancel_mission(id:int):
    logger.info("/PUT /mission/{id}/cancel called")
    mission =  mission_repository.get_mission_by_id(id)
    
    if mission is None:
        logger.error(f"mission {id} does not exist")
        raise HTTPException(status_code=404, detail="Mission not found")
    
    if mission["status"] == "NEW" or mission["status"] == "ASSIGNED":
        try:
            mission_repository.update_mission_status(id, "CANCELLED")
        except:
            logger.error("somthing went wrong")
    else:
        logger.error("mission status is not not NEW or ASSIGNED")
        raise HTTPException(status_code=400, detail="Can only cancel NEW OR ASSIGNED missions")

                     