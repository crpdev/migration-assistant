from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Union
import subprocess
import os
import json
import tempfile
import shutil
from enum import Enum

app = FastAPI(title="Migration Tools MCP")

class MigrationTool(str, Enum):
    OPENREWRITE = "openrewrite"
    MODERNE = "moderne"

class RecipeType(str, Enum):
    JAVA_UPGRADE = "java_upgrade"
    DEPENDENCY_UPDATE = "dependency_update"
    CODE_CLEANUP = "code_cleanup"
    CUSTOM = "custom"

class MigrationToolRequest(BaseModel):
    project_path: str
    tool: MigrationTool
    recipe_type: RecipeType
    source_version: Optional[str] = None
    target_version: Optional[str] = None
    dependencies: Optional[List[Dict[str, str]]] = None
    custom_recipe: Optional[Dict] = None

class MigrationToolResponse(BaseModel):
    success: bool
    message: str
    changes: Optional[List[Dict[str, str]]] = None
    errors: Optional[List[str]] = None
    recipe_used: Optional[Dict] = None
    command_executed: Optional[str] = None

@app.post("/analyze", response_model=Dict)
async def analyze_project(request: MigrationToolRequest):
    """Analyze the project to determine migration needs"""
    try:
        if request.tool == MigrationTool.OPENREWRITE:
            return await analyze_with_openrewrite(request)
        elif request.tool == MigrationTool.MODERNE:
            return await analyze_with_moderne(request)
        else:
            raise HTTPException(status_code=400, detail="Unsupported migration tool")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/execute", response_model=MigrationToolResponse)
async def execute_migration(request: MigrationToolRequest):
    """Execute the migration using the specified tool"""
    try:
        if request.tool == MigrationTool.OPENREWRITE:
            return await execute_with_openrewrite(request)
        elif request.tool == MigrationTool.MODERNE:
            return await execute_with_moderne(request)
        else:
            raise HTTPException(status_code=400, detail="Unsupported migration tool")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recipes", response_model=Dict[str, List[Dict]])
async def list_available_recipes():
    """List available recipes for each migration tool"""
    return {
        "openrewrite": [
            {"name": "org.openrewrite.java.migrate.UpgradeToJava21", "description": "Upgrade Java code to Java 21"},
            {"name": "org.openrewrite.java.dependencies.UpgradeDependencyVersion", "description": "Upgrade dependency versions"},
            {"name": "org.openrewrite.java.format.AutoFormat", "description": "Format Java code"},
            {"name": "org.openrewrite.java.cleanup.CommonStaticAnalysis", "description": "Apply common static analysis fixes"}
        ],
        "moderne": [
            {"name": "java-upgrade", "description": "Upgrade Java code to a newer version"},
            {"name": "dependency-update", "description": "Update dependencies to newer versions"},
            {"name": "code-cleanup", "description": "Clean up code according to best practices"}
        ]
    }

async def analyze_with_openrewrite(request: MigrationToolRequest) -> Dict:
    """Analyze project using OpenRewrite"""
    try:
        # Create a temporary directory for the analysis
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a basic recipe for analysis
            recipe = {
                "org.openrewrite.java.migrate.UpgradeToJava21": {
                    "javaVersion": request.target_version or "21"
                }
            }
            
            recipe_path = os.path.join(temp_dir, "openrewrite-recipe.json")
            with open(recipe_path, 'w') as f:
                json.dump(recipe, f)
            
            # Run OpenRewrite in dry-run mode
            cmd = [
                "mvn", "org.openrewrite.maven:rewrite-maven-plugin:run",
                "-Drewrite.activeRecipes=org.openrewrite.java.migrate.UpgradeToJava21",
                "-Drewrite.dryRun=true"
            ]
            
            result = subprocess.run(cmd, cwd=request.project_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Parse the output to extract analysis information
                changes = []
                for line in result.stdout.split('\n'):
                    if "would make the following changes" in line:
                        changes.append({"file": line.split(":")[0].strip(), "type": "would_update"})
                
                return {
                    "success": True,
                    "message": "Analysis completed successfully",
                    "changes": changes,
                    "recipe_used": recipe
                }
            else:
                return {
                    "success": False,
                    "message": "Analysis failed",
                    "errors": [result.stderr]
                }
    except Exception as e:
        return {
            "success": False,
            "message": f"Analysis failed: {str(e)}",
            "errors": [str(e)]
        }

async def analyze_with_moderne(request: MigrationToolRequest) -> Dict:
    """Analyze project using Moderne CLI"""
    try:
        # Run Moderne CLI in dry-run mode
        cmd = [
            "moderne", "analyze",
            "--source", request.project_path,
            "--dry-run"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Parse the output to extract analysis information
            changes = []
            for line in result.stdout.split('\n'):
                if "would change" in line:
                    changes.append({"file": line.split(":")[0].strip(), "type": "would_change"})
            
            return {
                "success": True,
                "message": "Analysis completed successfully",
                "changes": changes
            }
        else:
            return {
                "success": False,
                "message": "Analysis failed",
                "errors": [result.stderr]
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Analysis failed: {str(e)}",
            "errors": [str(e)]
        }

async def execute_with_openrewrite(request: MigrationToolRequest) -> MigrationToolResponse:
    """Execute migration using OpenRewrite"""
    try:
        # Create recipe based on recipe type
        recipe = create_openrewrite_recipe(request)
        
        # Save recipe to a temporary file
        recipe_path = os.path.join(request.project_path, "openrewrite-recipe.json")
        with open(recipe_path, 'w') as f:
            json.dump(recipe, f)
        
        # Build the command based on recipe type
        if request.recipe_type == RecipeType.JAVA_UPGRADE:
            cmd = [
                "mvn", "org.openrewrite.maven:rewrite-maven-plugin:run",
                "-Drewrite.activeRecipes=org.openrewrite.java.migrate.UpgradeToJava21"
            ]
        elif request.recipe_type == RecipeType.DEPENDENCY_UPDATE:
            cmd = [
                "mvn", "org.openrewrite.maven:rewrite-maven-plugin:run",
                "-Drewrite.activeRecipes=org.openrewrite.java.dependencies.UpgradeDependencyVersion"
            ]
        elif request.recipe_type == RecipeType.CODE_CLEANUP:
            cmd = [
                "mvn", "org.openrewrite.maven:rewrite-maven-plugin:run",
                "-Drewrite.activeRecipes=org.openrewrite.java.cleanup.CommonStaticAnalysis"
            ]
        else:  # CUSTOM
            # For custom recipes, we need to specify the recipe file
            cmd = [
                "mvn", "org.openrewrite.maven:rewrite-maven-plugin:run",
                f"-Drewrite.recipeFile={recipe_path}"
            ]
        
        # Execute the command
        result = subprocess.run(cmd, cwd=request.project_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            return MigrationToolResponse(
                success=True,
                message="Migration completed successfully",
                changes=[{"file": "pom.xml", "type": "updated"}],
                recipe_used=recipe,
                command_executed=" ".join(cmd)
            )
        else:
            return MigrationToolResponse(
                success=False,
                message="Migration failed",
                errors=[result.stderr],
                recipe_used=recipe,
                command_executed=" ".join(cmd)
            )
    
    except Exception as e:
        return MigrationToolResponse(
            success=False,
            message=f"Migration failed: {str(e)}",
            errors=[str(e)]
        )

async def execute_with_moderne(request: MigrationToolRequest) -> MigrationToolResponse:
    """Execute migration using Moderne CLI"""
    try:
        # Build the command based on recipe type
        if request.recipe_type == RecipeType.JAVA_UPGRADE:
            cmd = [
                "moderne", "migrate",
                "--source", request.project_path,
                "--target-version", request.target_version or "21",
                "--recipe", "java-upgrade"
            ]
        elif request.recipe_type == RecipeType.DEPENDENCY_UPDATE:
            cmd = [
                "moderne", "migrate",
                "--source", request.project_path,
                "--recipe", "dependency-update"
            ]
        elif request.recipe_type == RecipeType.CODE_CLEANUP:
            cmd = [
                "moderne", "migrate",
                "--source", request.project_path,
                "--recipe", "code-cleanup"
            ]
        else:  # CUSTOM
            # For custom recipes, we need to specify the recipe file
            recipe_path = os.path.join(request.project_path, "moderne-recipe.json")
            with open(recipe_path, 'w') as f:
                json.dump(request.custom_recipe, f)
            
            cmd = [
                "moderne", "migrate",
                "--source", request.project_path,
                "--recipe-file", recipe_path
            ]
        
        # Execute the command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return MigrationToolResponse(
                success=True,
                message="Migration completed successfully",
                changes=[{"file": "pom.xml", "type": "updated"}],
                command_executed=" ".join(cmd)
            )
        else:
            return MigrationToolResponse(
                success=False,
                message="Migration failed",
                errors=[result.stderr],
                command_executed=" ".join(cmd)
            )
    
    except Exception as e:
        return MigrationToolResponse(
            success=False,
            message=f"Migration failed: {str(e)}",
            errors=[str(e)]
        )

def create_openrewrite_recipe(request: MigrationToolRequest) -> Dict:
    """Create an OpenRewrite recipe based on the request"""
    if request.recipe_type == RecipeType.JAVA_UPGRADE:
        return {
            "org.openrewrite.java.migrate.UpgradeToJava21": {
                "javaVersion": request.target_version or "21"
            }
        }
    elif request.recipe_type == RecipeType.DEPENDENCY_UPDATE:
        # Create a recipe for updating dependencies
        deps = []
        for dep in request.dependencies or []:
            deps.append({
                "groupId": dep.get("groupId", ""),
                "artifactId": dep.get("artifactId", ""),
                "newVersion": dep.get("version", "")
            })
        
        return {
            "org.openrewrite.java.dependencies.UpgradeDependencyVersion": {
                "dependencies": deps
            }
        }
    elif request.recipe_type == RecipeType.CODE_CLEANUP:
        return {
            "org.openrewrite.java.cleanup.CommonStaticAnalysis": {}
        }
    else:  # CUSTOM
        return request.custom_recipe or {}

if __name__ == "__main__":
    import uvicorn
    from config import MCP_SERVERS
    
    # Add this server to the config
    server_config = {
        "host": "localhost",
        "port": 8004
    }
    
    uvicorn.run(app, host=server_config["host"], port=server_config["port"]) 