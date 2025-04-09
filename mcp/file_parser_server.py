from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import xmltodict
import re
from typing import Dict, List, Optional
import os

app = FastAPI(title="File Parser MCP")

class ParserRequest(BaseModel):
    file_path: str
    file_type: str

class Dependency(BaseModel):
    groupId: str
    artifactId: str
    version: str
    scope: Optional[str] = None

class POMAnalysis(BaseModel):
    java_version: str
    dependencies: List[Dependency]
    properties: Dict[str, str]

class JavaFileAnalysis(BaseModel):
    imports: List[str]
    class_name: str
    package_name: str
    java_version: Optional[str] = None

@app.post("/parse/pom", response_model=POMAnalysis)
async def parse_pom(request: ParserRequest):
    try:
        if not os.path.exists(request.file_path):
            raise HTTPException(status_code=404, detail="POM file not found")
        
        with open(request.file_path, 'r') as f:
            pom_content = f.read()
        
        pom_dict = xmltodict.parse(pom_content)
        project = pom_dict['project']
        
        # Extract Java version
        java_version = None
        if 'properties' in project and 'java.version' in project['properties']:
            java_version = project['properties']['java.version']
        elif 'properties' in project and 'maven.compiler.source' in project['properties']:
            java_version = project['properties']['maven.compiler.source']
        
        # Extract dependencies
        dependencies = []
        if 'dependencies' in project and 'dependency' in project['dependencies']:
            deps = project['dependencies']['dependency']
            if not isinstance(deps, list):
                deps = [deps]
            
            for dep in deps:
                dependencies.append(Dependency(
                    groupId=dep.get('groupId', ''),
                    artifactId=dep.get('artifactId', ''),
                    version=dep.get('version', ''),
                    scope=dep.get('scope')
                ))
        
        return POMAnalysis(
            java_version=java_version,
            dependencies=dependencies,
            properties=project.get('properties', {})
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/parse/java", response_model=JavaFileAnalysis)
async def parse_java(request: ParserRequest):
    try:
        if not os.path.exists(request.file_path):
            raise HTTPException(status_code=404, detail="Java file not found")
        
        with open(request.file_path, 'r') as f:
            java_content = f.read()
        
        # Extract package name
        package_match = re.search(r'package\s+([^;]+);', java_content)
        package_name = package_match.group(1) if package_match else ""
        
        # Extract class name
        class_match = re.search(r'class\s+(\w+)', java_content)
        class_name = class_match.group(1) if class_match else ""
        
        # Extract imports
        imports = re.findall(r'import\s+([^;]+);', java_content)
        
        return JavaFileAnalysis(
            imports=imports,
            class_name=class_name,
            package_name=package_name
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    from config import MCP_SERVERS
    
    server_config = MCP_SERVERS["file_parser"]
    uvicorn.run(app, host=server_config["host"], port=server_config["port"]) 