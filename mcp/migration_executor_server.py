from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import subprocess
import os
import json

app = FastAPI(title="Migration Executor MCP")

class MigrationRequest(BaseModel):
    project_path: str
    source_version: str
    target_version: str
    tool: str  # "openrewrite" or "moderne"
    dependencies: List[Dict[str, str]]

class MigrationResponse(BaseModel):
    success: bool
    message: str
    changes: Optional[List[Dict[str, str]]] = None
    errors: Optional[List[str]] = None

@app.post("/execute", response_model=MigrationResponse)
async def execute_migration(request: MigrationRequest):
    try:
        if request.tool == "openrewrite":
            return await execute_openrewrite_migration(request)
        elif request.tool == "moderne":
            return await execute_moderne_migration(request)
        else:
            raise HTTPException(status_code=400, detail="Unsupported migration tool")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def execute_openrewrite_migration(request: MigrationRequest):
    try:
        # Create OpenRewrite recipe
        recipe = {
            "org.openrewrite.java.migrate.UpgradeToJava21": {
                "javaVersion": request.target_version
            }
        }
        
        recipe_path = os.path.join(request.project_path, "openrewrite-recipe.json")
        with open(recipe_path, 'w') as f:
            json.dump(recipe, f)
        
        # Execute OpenRewrite migration
        cmd = [
            "mvn", "org.openrewrite.maven:rewrite-maven-plugin:run",
            "-Drewrite.activeRecipes=org.openrewrite.java.migrate.UpgradeToJava21"
        ]
        
        result = subprocess.run(cmd, cwd=request.project_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            return MigrationResponse(
                success=True,
                message="Migration completed successfully",
                changes=[{"file": "pom.xml", "type": "updated"}]
            )
        else:
            return MigrationResponse(
                success=False,
                message="Migration failed",
                errors=[result.stderr]
            )
    
    except Exception as e:
        return MigrationResponse(
            success=False,
            message="Migration failed",
            errors=[str(e)]
        )

async def execute_moderne_migration(request: MigrationRequest):
    try:
        # Execute Moderne CLI migration
        cmd = [
            "moderne", "migrate",
            "--source", request.project_path,
            "--target-version", request.target_version
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return MigrationResponse(
                success=True,
                message="Migration completed successfully",
                changes=[{"file": "pom.xml", "type": "updated"}]
            )
        else:
            return MigrationResponse(
                success=False,
                message="Migration failed",
                errors=[result.stderr]
            )
    
    except Exception as e:
        return MigrationResponse(
            success=False,
            message="Migration failed",
            errors=[str(e)]
        )

if __name__ == "__main__":
    import uvicorn
    from config import MCP_SERVERS
    
    server_config = MCP_SERVERS["migration_executor"]
    uvicorn.run(app, host=server_config["host"], port=server_config["port"]) 