
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dbcat.api import open_catalog, add_mysql_source
from piicatcher.api import scan_database, OutputFormat
from typing import List, Dict
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MySQL connection configuration
db_config = {
    'host':"sql6.freesqldatabase.com",
    'user':'sql6706356',
    'password':'DhhH9b8dbU',
    'database':'sql6706356'
    #'host': '127.0.0.1',
    #'user': 'root',
    #'password': 'root',
    #'database': 'crm'  
}

# Function to fetch all databases
def get_databases():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES")
    databases = [row[0] for row in cursor.fetchall() if row[0] not in ('information_schema', 'performance_schema')]
    connection.close()
    return databases


# Function to fetch all tables in a database
def get_tables(database):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(f"USE {database}")
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    connection.close()
    return tables

    
class DatabaseItem(BaseModel):
    database: str
    table: str
    field: str
    PIILevel: str
    Class: str

class ScanSettings(BaseModel):
    include_schema_regex:  str
    include_table_regex:  str
    #exclude_schema_regex: list =  ["^salika$", "^world$"]
    
            
# API endpoint to fetch all databases
@app.get("/databases")
def fetch_databases():
    databases = get_databases()
    return {"databases": databases}
            
# API endpoint to fetch all tables in a selected database
@app.get("/tables/{database}")
def fetch_tables(database: str):
    tables = get_tables(database)
    return {"tables": tables}

# API endpoint to fetch all columns of a specific table in a chosen database
@app.get("/columns/{database}/{table}")
def fetch_columns(database: str, table: str):
    columns = get_columns(database, table)
    return {"columns": columns}

# Function to get all columns of a specific table in a database
def get_columns(database: str, table: str):
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(f"USE {database}")
        cursor.execute(f"SHOW COLUMNS FROM {table}")
        columns = [row[0] for row in cursor.fetchall()]
        connection.close()
        return columns
    

@app.post("/scan",response_model=List[DatabaseItem])
async def scan_database_endpoint(settings: ScanSettings):
    # Open the catalog
    catalog = open_catalog(app_dir='/tmp/.config/piicatcher', path=':memory:', secret='my_secret')
    with catalog.managed_session:
        # Add the MySQL source
        source = add_mysql_source(
            catalog=catalog,
            name="mysql_db",
            #uri="127.0.0.1",
            #username="root",
            #password="root",
            uri="sql6.freesqldatabase.com",  # The hostname of your MySQL server
            username="sql6706356",  # Your MySQL username
            password="DhhH9b8dbU",  # Your MySQL password
            database="sql6706356",
            port=3306,
            #database=settings.include_schema_regex
        )
        # Perform the scan using hardcoded regex patterns
        output = scan_database(
            catalog=catalog,
            source=source,
            include_schema_regex=[f"^{settings.include_schema_regex}$"],
            exclude_schema_regex=[f"^(?!{settings.include_schema_regex}$).*$"],
            include_table_regex=[f"^{settings.include_table_regex}$"],
            exclude_table_regex=[f"^(?!{settings.include_table_regex}$).*$"],
            output_format=OutputFormat.tabular  # Assuming tabular output can be converted to JSON-like structure
            
        )
        #return output

   # print(output)

    return [DatabaseItem(database=item[0], table=item[1], field=item[2], PIILevel=item[3], Class=item[4]) for item in output]
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)