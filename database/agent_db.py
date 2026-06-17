from database.db_connection import DB_connection
from schemas import CreateAgent, UpdateAgent

class AgentDB:
    def __init__(self, db : DB_connection):
        self.db = db

    def create_agent(self, data : CreateAgent):
        connection = self.db.get_connection()
        cursor= connection.cursor(dictionary=True)
        agent_data = data.model_dump()

        cursor.execute("""INSERT INTO agents(name, specialty, agent_rank)
                       VALUES (%s, %s, %s);""", (agent_data["name"], agent_data["specialty"], agent_data["agent_rank"]))

        connection.commit()

        cursor.execute("""SELECT * from agents WHERE id = (SELECT max(id) from agents);""")

        agent = cursor.fetchone
        cursor.close()

        return agent
    
    def get_all_agents(self):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * from agents;")
        result = cursor.fetchall()
        
        cursor.close()
        return result
    
    def get_agent_by_id(self, id : int):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("select * from agents where id = %s;",(id,))
        result = cursor.fetchone()
        
        cursor.close()
        return result
    
    def update_agent(self, id : int, data : UpdateAgent):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        agent_data = data.model_dump()

        cursor.execute("""UPDATE agents 
                       SET name = %s, 
                       specialty = %s, 
                       agent_rank = %s 
                       where id = %s;""", (agent_data["name"], agent_data["specialty"], agent_data["agent_rank"], id))
        
        connection.commit()

        cursor.close()
        return {
            "Update was made successfully"
        }

    def deactivate_agent(self, id):
        connection = self.db.get_connection()
        cursor = connection.cursor()
        
        cursor.execute("UPDATE agents SET is_active = FALSE where id = %s", (id,))

        connection.commit()
        cursor.close()

        return{
            f"agent {id} was deactivated successfully"
        }
    
    def increment_completed(self, id):
        connection = self.db.get_connection()
        cursor = connection.cursor()
        
        cursor.execute("""update agents 
                           set completed_missions = completed_missions + 1
                           where id = %s;""", (id,))
        connection.commit()
        cursor.close()

        return{
            f"agent {id} completed missions counter successfully updated"
        }

    def increment_failed(self, id):
        connection = self.db.get_connection()
        cursor = connection.cursor()
        
        cursor.execute("""update agents 
                           set failed_missions = failed_missions + 1
                           where id = %s;""", (id,))
        connection.commit()
        cursor.close()

        return{
             f"agent {id} failed missions counter successfully updated"
        }
    
    def get_agent_performance(self, id):
        performance = {}

        connection = self.db.get_connection()
        cursor = connection.cursor()
        
        cursor.execute("""SELECT completed_missions, failed_missions 
                          from agents
                          where id = %s;""", (id,))
        
        stats = cursor.fetchall()
        cursor.close()
        
        performance["completed"] = stats[0]
        performance["failes"] = stats[1]
        performance["total"] = sum(stats)
        performance["success_rate"] = ((performance["completed"] / performance["total"]) * 100)

        return performance
    
    def count_active_agents(self):
        connection = self.db.get_connection()
        cursor = connection.cursor()
        
        cursor.execute("""SELECT COUNT(*) 
                          from agents
                          where is_acrtive = %s;""", (True,))
        
        active_agents = cursor.fetcone()[0]
        cursor.close()
        
       
        return active_agents


        
        