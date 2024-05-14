from fastapi import APIRouter, HTTPException
from dbcat.api import open_catalog, add_mysql_source
from piicatcher.api import scan_database, OutputFormat

router = APIRouter()

@router.get("/scan")
async def scan_db():
    try:
        catalog = open_catalog(app_dir='/tmp/.config/piicatcher', path=':memory:', secret='my_secret')
        with catalog.managed_session:
            source = add_mysql_source(
                catalog=catalog,
                name="mysql_db",
                uri="127.0.0.1",
                username="root",
                password="root",
                database="newschema",
            )
            output = scan_database(
                catalog=catalog,
                source=source,
                include_schema_regex=["^newschema$"],
                exclude_schema_regex=["^sakila$", "^world$"],
                output_format=OutputFormat.json
            )
            return output
        #print(output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))