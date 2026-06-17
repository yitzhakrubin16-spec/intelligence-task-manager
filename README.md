# intelligence-task-manager 

## System description

מערכת לניהול סוכנים ומשימות עבור יחידת מודיעין ShadowNet.

המערכת עובדת באמצעות מסד נתונים MySQL המכיל 2 טבלאות נתונים, אחת של סוכנים ואחת של משימות.

טבלת הסוכנים מכילה נתונים על כל סוכן:
מספר זיהוי, שם, תחום התמחות, סטטוס פעילות, מונה משימות שהצליחו, מונה משימות שנכשלו ודרגת הסוכן.

טבלת המשימות מכילה נתונים על כל משימה:
מספר זיהוי, כותרת המשימה, תיאור המשימה, מיקום המשימה, רמת קושי, רמת חשיבות, סטטוס, רמת סיכון,
ומספר זיהוי של הסוכן ששויך למשימה.

מטרת התוכנית לסייע בניהול יעיל ושמירת הנתונים על כל סוכן ועל כל משימה.


## File structure

מבנה התיקיות ההתחלתי הוא כדלהלן:

```text
intelligence-task-manager/
│
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore
```



## Tables structure


### Agent

| id | name | specialty | is_active | completed_missions | failed_missions | agent_rank |
|----|------|-----------|-----------|--------------------|-----------------|------------|
|מזהה ייחודי לכל סוכן|שם הסוכן|תחום התמחות|סטטוס פעילות|מונה המשימות שהושלמו|מונה המשימות שנכשלו|דרגת הסוכן|
|INT, AUTO_INCREMENT, PRIMARY KEY|VARCHAR|VARCHAR|BOOLEAN|INT|INT|ENUM|
|מוקצה אוטומטית ביצירת סוכן|חובה להכניס|חובה להכניס|ברירת מחדל True|ברירת מחדל 0|ברירת מחדל 0| יכול להיות רק Junior, Senior or Commander|

### Mission

| id | title | description | location | difficulty | importance | status | risk_level | assigned_agent_id |
|----|-------|-------------|----------|------------|------------|--------|------------|-------------------|
|מזהה ייחודי לכל משימה|כותרת המשימה|תיאור מפורט של המשימה|מיקום|רמת הקושי של המשימה|רמת החשיבות של המשימה|סטטוס המשימה|רמת הסיכון - מחושב לפי נוסחא על פי רמות הקושי והחשיבות|מספר מזהה של הסוכן ששויך למשימה|
|INT, AUTO_INCREMENT, PRIMARY KEY|VARCHAR|TEXT|VARCHAR|INT|INT|VARCHAR|VARCHAR|INT|
|מוקצה אוטומטית ביצירת משימה|חובה להכניס|חובה להכניס|חובה להכניס|1-10, חובה להכניס|1-10, חובה להכניס|ברירת מחדל בעת יצירה: NEW. חוקי השינוי וההגבלות יופיעו בחוקי המערכת|LOW, MEDIUM, HIGH or CRITICAL. מתחת לטבלא הגדרות לקביעת הרמה והנוסחא לחישוב|ברירת מחדל NULL|

### risk_level calculation:

#### formula:
```text
difficulty * 2 + importance = risk_level
```

#### setting:
```text
3-9 → Low | 10–17 → MEDIUM | 18–24 → HIGH | 25+ → CRITICAL
```


## Databse Classes sructure and description:

### Class DB_Connection:

המחלקה אחראית ליצירת חיבור כללי בין פייתון לdatabase וליצירה הראשונית של הdatabase והטבלאות.

| Method | Description | 
|--------|-------------|
| `get_connection()` | Checks if there is an active connection to MySQL. If so, returns it. If not, creates a new connection and returns it |
| `create_database()` | Creates Intelligence_db if it does not exist. | 
| `create_tables()` | Creates both tables if they do not exist.|

```text
המתודות שיוצרות את הdatabase והטבלאות ירוצו בעליית המערכת
```

### Class AgentDB:

בעזרת חיבור שמתקבל מDB_Connection, מעבירה פעולות SQL על טבלת agents.


| Method | Description | 
|--------|-------------|
| `create_agent(data)` | Creates a new agent and returns the new agent object. |
| `get_all_agents()` | Returns a list of all agents | 
| `get_agent_by_id(id)` | Returns one agent by ID, or None |
| `update_agent(id, data)` | UPDATE for the entire row (cannot change id). Returns a success or failure message.|
| `deactivate_agent(id)` | Sets agent inactive status. Returns a success or failure message. | 
| `increment_completed(id)` | Updates the number of tasks completed. Returns a success or failure message.|
| `increment_failed(id)` | Updates the number of failed tasks. Returns a success or failure message.|
| `get_agent_performance(id)` | Returns a dictionary with these keys: completed, failed, total, success_rate. | 
| `count_active_agents()` | Returns the number of active agents |


### Class MissionDB:

בעזרת חיבור שמתקבל מDB_Connection, מעבירה פעולות SQL על טבלת missions.


| Method | Description | 
|--------|-------------|
| `create_mission(data)` | Creates a new mission and returns the new mission object. |
| `get_all_missions()` | Returns a list of all missions | 
| `get_mission_by_id(id)` | Returns one mission by ID, or None |
| `assign_mission(m_id, a_id)` | Assigning a mission to an agent. Returns a success or failure message.|
| `update_mission_status(id, status)` | Used for any mission status change. Returns a success or failure message. | 
| `get_open_missions_by_agent(id)` | Returns agent ASSIGNED/IN_PROGRESS missions. |
| `count_all_missions()` | Returns sum of missions.|
| `count_by_status(status)` | Counts missions by a specific status. | 
| `count_open_missions()` | Counts open (ASSIGNED/IN_PROGRESS) missions. |
| `count_critical_missions()` | Counts missions with risk_level CRITICAL. | 
| `get_top_agent()` | Returns the agent with the highest completed_missions. |




## System rules

 ### 1. 
  rank must be Junior / Senior / Commander — any other value throws an error.
 
 ### 2. 
  difficulty and importance must be between 1 and 10 — otherwise an error.

  ### 3. 
  risk_level is calculated automatically when a task is created—the user does not submit it.

  ### 4. 
  An agent with is_active=False cannot accept tasks.

  ### 5. 
  An agent cannot have more than 3 open tasks (ASSIGNED / IN_PROGRESS) at the same time.

  ### 6. 
  If risk_level=CRITICAL — only an agent with the rank of Commander can accept the mission

  ### 7. 
  Only a task with a status of NEW can be assigned. After assignment: status=ASSIGNED.

  ### 8. 
  You can only start a task with the status ASSIGNED. After: status=IN_PROGRESS

  ### 9.
  Only an IN_PROGRESS task can be completed and changed to FAILED or COMPLETED status.

  ### 10.
  You can change to CANCELLED status only if the status is NEW or ASSIGNED—otherwise an error.
  
  ### Possible statuses:

  | Status | Meaning | Rules |
  |--------|---------|-------|
  | NEW | New mission | Default when creating. Can be canceled. | 
  | ASSIGNED | Associated with an agent | Can come only from NEW. Can be canceled. |
  | IN_PROGRESS | Mission in progress |  Can come only from ASSIGNED. Can not be canceled. | 
  | COMPLETED | Mission successfully completed | Can come only from IN_PROGRESS. Can not be canceled. | 
  | FAILED | Mission failed | Can come only from IN_PROGRESS. Can not be canceled. |
  | CANCELLED | Mission canceled | Can come only from ASSIGNED or NEW. | 
  

## Running Instructions

### 1. Open terminal in the project folder

Run the following commands from the main project folder:

```text
intelligence-task-manager/
```

Example:

```bash
cd intelligence-task-manager
```

---

### 2. Create a virtual environment

Run from the project root folder:

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
venv\Scripts\activate
```

---

### 3. Install requirements

Run from the project root folder:

```bash
pip install -r requirements.txt
```

---

### 4. Run MySQL with Docker

This command can be run from any terminal, but it is recommended to run it from the project root folder.

```bash
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
```

Database details:

```text
Container name: intelligence-mysql
Database name: Intelligence_db
Root password: 1234
Port: 3306
```

Make sure the database connection settings in:

```text
database/db_connection.py
```

match these Docker settings.

---

