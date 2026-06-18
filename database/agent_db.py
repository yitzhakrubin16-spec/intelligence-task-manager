from database.db_connection import DB_connection


class AgentDB:
    def __init__(self, db : DB_connection):
        self.db = db

    def create_agent(self, data : dict):
        connection = self.db.get_connection()
        cursor= connection.cursor(dictionary=True)

        cursor.execute("""INSERT INTO agents(name, specialty, agent_rank)
                       VALUES (%s, %s, %s);""", (data["name"], data["specialty"], data["agent_rank"]))

        connection.commit()

        cursor.execute("""SELECT * from agents WHERE id = (SELECT max(id) from agents);""")

        agent = cursor.fetchone()
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
    
    def update_agent(self, id : int, data : dict):
        connection = self.db.get_connection()
        cursor = connection.cursor()

        cursor.execute("""UPDATE agents 
                       SET name = %s, 
                       specialty = %s, 
                       agent_rank = %s 
                       where id = %s;""", (data["name"], data["specialty"], data["agent_rank"], id))
        
        connection.commit()

        cursor.close()
        return {
            "message" : "Update was made successfully"
        }

    def deactivate_agent(self, id):
        connection = self.db.get_connection()
        cursor = connection.cursor()
        
        cursor.execute("UPDATE agents SET is_active = FALSE where id = %s", (id,))

        connection.commit()
        cursor.close()

        return{
             "message" : f"agent {id} was deactivated successfully"
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
            "message" : f"agent {id} completed missions counter successfully updated"
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
             "message" : f"agent {id} failed missions counter successfully updated"
        }
    
    def get_agent_performance(self, id):
        performance = {}

        connection = self.db.get_connection()
        cursor = connection.cursor()
        
        cursor.execute("""SELECT completed_missions 
                          from agents
                          where id = %s;""", (id,))
        
        
        completed = cursor.fetchone()[0]

        cursor.execute("""SELECT failed_missions 
                          from agents
                          where id = %s;""", (id,))
        
        
        failed = cursor.fetchone()[0]

        cursor.execute("""SELECT COUNT(*) 
                          from missions
                          where assigned_agent_id = %s
                          AND (status = %s or status = 
                          %s);""", (id, "ASSIGNED", "IN_PROGRESS"))
        open_missions = cursor.fetchone()[0]
        cursor.close()
        
        performance["completed"] = completed
        performance["failed"] = failed
        performance["total"] = completed + failed + open_missions
        if performance["total"] != 0:
            performance["success_rate"] = ((performance["completed"] / performance["total"]) * 100)
        else:
            performance["success_rate"] = 0

        return performance
    
    def count_active_agents(self):
        connection = self.db.get_connection()
        cursor = connection.cursor()
        
        cursor.execute("""SELECT COUNT(*) 
                          from agents
                          where is_active = %s;""", (True,))
        
        active_agents = cursor.fetchone()[0]
        cursor.close()
        
       
        return active_agents


        
        