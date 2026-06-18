from database.db_connection import DB_connection


class MissionDB:
    def __init__(self, db : DB_connection):
        self.db = db

    def create_mission(self, data: dict):
        connection = self.db.get_connection()
        cursor= connection.cursor(dictionary=True)

        risk_score =  data["difficulty"] * 2 + data["importance"]

        if risk_score <= 9:
            data["risk_level"] = "LOW"
        elif 10 <= risk_score <= 17:
            data["risk_level"] = "MEDIUM"
        elif 18 <= risk_score <= 24:
            data["risk_level"] = "HIGH "
        else:
            data["risk_level"] = "CRITICAL"       


        cursor.execute("""INSERT INTO missions (title, description, location,
                       difficulty, importance, risk_level)
                       VALUES (%s, %s, %s, %s, %s, %s);""",
                    (data["title"], data["description"],
                    data["location"], data["difficulty"], 
                    data["importance"], data["risk_level"]))

        connection.commit()

        cursor.execute("""SELECT * from missions WHERE id = (SELECT max(id) from missions);""")

        mission = cursor.fetchone()
        cursor.close()

        return mission
    
    def get_all_missions(self):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * from missions;")
        result = cursor.fetchall()
        
        cursor.close()
        return result
    
    def get_mission_by_id(self, id : int):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("select * from missions where id = %s;",(id,))
        result = cursor.fetchone()
        
        cursor.close()
        return result
    
    def assign_mission(self, m_id:int, a_id:int):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""update missions
                        set assigned_agent_id = %s
                       where id = %s;""",(a_id, m_id))
        
        connection.commit()
        cursor.close()
        
        return {
            "assigning was made successfully"
        }
    

    def update_mission_status(self, id : int, status : str):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
       
        match status.upper():

            case "ASSIGNED":
                if self.get_mission_by_id(id) == "NEW":
                    cursor.execute("""update missions
                                    set status = %s
                                    where id = %s;""",(status.upper(), id))
                    connection.commit()
                    cursor.close()
                    return {f"status updated successfully to {status.upper()}"}
                else:
                    return {f"status can not by updated to {status.upper()}"}
            
            case "IN_PROGRESS":
                if self.get_mission_by_id(id) == "ASSIGNED":
                    cursor.execute("""update missions
                                    set status = %s
                                    where id = %s;""",(status.upper(), id))
                    connection.commit()
                    cursor.close()
                    return {f"status updated successfully to {status.upper()}"}
                else:
                    return {f"status can not by updated to {status.upper()}"}
            
            case "COMPLETED":
                if self.get_mission_by_id(id) == "IN_PROGRESS":
                    cursor.execute("""update missions
                                    set status = %s
                                    where id = %s;""",(status.upper(), id))
                    connection.commit()
                    cursor.close()
                    return {f"status updated successfully to {status.upper()}"}
                else:
                    return {f"status can not by updated to {status.upper()}"}    
            
            case "FAILED":
                if self.get_mission_by_id(id) == "IN_PROGRESS":
                    cursor.execute("""update missions
                                    set status = %s
                                    where id = %s;""",(status.upper(), id))
                    connection.commit()
                    cursor.close()
                    return {f"status updated successfully to {status.upper()}"}
                else:
                    return {f"status can not by updated to {status.upper()}"}    
            
            case "CANCELLED":
                if self.get_mission_by_id(id) in ["NEW", "ASSIGNED"]:
                    cursor.execute("""update missions
                                    set status = %s
                                    where id = %s;""",(status.upper(), id))
                    connection.commit()
                    cursor.close()
                    return {f"status updated successfully to {status.upper()}"}
                else:
                    return {f"status can not by updated to {status.upper()}"}    
            
            case _:
                cursor.close()
                return {f"{status.upper()} is invalid"}
            
            
    def get_open_missions_by_agent(self, id : int):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("select * from missions where assigned_agent_id = %s and status = %s or status = %s;",(id, "ASSIGNED", "IN_PROGRESS"))
        result = cursor.fetchall()
        
        cursor.close()
        return result
    
    def count_all_missions(self):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("COUNT(*) FROM missions;")
        result = cursor.fetchone()[0]
        
        cursor.close()
        return result
    

    def count_by_status(self, status : str):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("COUNT(*) FROM missions where status = %s;", (status,))
        result = cursor.fetchone()[0]
        
        cursor.close()
        return result
    
    def count_open_missions(self):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("COUNT(*) FROM missions where status = %s or status = %s;", ("ASSIGNED", "IN_PROGRESS"))
        result = cursor.fetchone()[0]
        
        cursor.close()
        return result
        
  
    def count_critical_missions(self):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("COUNT(*) FROM missions where risk_level = %s;", ("CRITICAL",))
        result = cursor.fetchone()[0]
        
        cursor.close()
        return result
        

    def get_top_agent(self):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("select (*) FROM agents where completed_missions = (SELECT MAX(completed_missions) FROM agents);")
        result = cursor.fetchone()[0]
        
        cursor.close()
        return result
        
    