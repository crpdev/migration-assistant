from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import subprocess
import os
import json
import re

app = FastAPI(title="Maven MCP")

class MavenRequest(BaseModel):
    project_path: str
    goals: List[str]
    profiles: Optional[List[str]] = None
    properties: Optional[Dict[str, str]] = None
    skip_tests: Optional[bool] = False

class MavenResponse(BaseModel):
    success: bool
    message: str
    output: Optional[str] = None
    errors: Optional[List[str]] = None
    test_results: Optional[Dict] = None
    build_artifacts: Optional[List[str]] = None

def parse_test_results(output: str) -> Dict:
    """Parse Maven test output to extract test results"""
    results = {
        "tests": 0,
        "failures": 0,
        "errors": 0,
        "skipped": 0,
        "failed_tests": []
    }
    
    # Extract test summary
    test_summary = re.search(r'Tests run: (\d+), Failures: (\d+), Errors: (\d+), Skipped: (\d+)', output)
    if test_summary:
        results["tests"] = int(test_summary.group(1))
        results["failures"] = int(test_summary.group(2))
        results["errors"] = int(test_summary.group(3))
        results["skipped"] = int(test_summary.group(4))
    
    # Extract failed tests
    for line in output.split('\n'):
        if line.startswith('Failed tests:'):
            failed_tests_section = True
            continue
        if failed_tests_section and line.strip() and not line.startswith('Tests '):
            results["failed_tests"].append(line.strip())
    
    return results

@app.post("/compile", response_model=MavenResponse)
async def compile_project(request: MavenRequest):
    """Compile the Maven project"""
    try:
        cmd = ["mvn", "compile"]
        if request.profiles:
            cmd.extend(["-P", ",".join(request.profiles)])
        if request.properties:
            for key, value in request.properties.items():
                cmd.append(f"-D{key}={value}")
        
        result = subprocess.run(cmd, cwd=request.project_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            return MavenResponse(
                success=True,
                message="Project compiled successfully",
                output=result.stdout
            )
        else:
            return MavenResponse(
                success=False,
                message="Compilation failed",
                errors=[result.stderr]
            )
    except Exception as e:
        return MavenResponse(
            success=False,
            message=f"Compilation failed: {str(e)}",
            errors=[str(e)]
        )

@app.post("/test", response_model=MavenResponse)
async def run_tests(request: MavenRequest):
    """Run Maven tests"""
    try:
        cmd = ["mvn", "test"]
        if request.profiles:
            cmd.extend(["-P", ",".join(request.profiles)])
        if request.properties:
            for key, value in request.properties.items():
                cmd.append(f"-D{key}={value}")
        
        result = subprocess.run(cmd, cwd=request.project_path, capture_output=True, text=True)
        test_results = parse_test_results(result.stdout)
        
        if result.returncode == 0:
            return MavenResponse(
                success=True,
                message="Tests completed successfully",
                output=result.stdout,
                test_results=test_results
            )
        else:
            return MavenResponse(
                success=False,
                message="Tests failed",
                errors=[result.stderr],
                test_results=test_results
            )
    except Exception as e:
        return MavenResponse(
            success=False,
            message=f"Tests failed: {str(e)}",
            errors=[str(e)]
        )

@app.post("/build", response_model=MavenResponse)
async def build_project(request: MavenRequest):
    """Build the Maven project"""
    try:
        cmd = ["mvn", "clean", "install"]
        if request.skip_tests:
            cmd.append("-DskipTests")
        if request.profiles:
            cmd.extend(["-P", ",".join(request.profiles)])
        if request.properties:
            for key, value in request.properties.items():
                cmd.append(f"-D{key}={value}")
        
        result = subprocess.run(cmd, cwd=request.project_path, capture_output=True, text=True)
        
        # Find build artifacts
        target_dir = os.path.join(request.project_path, "target")
        artifacts = []
        if os.path.exists(target_dir):
            for file in os.listdir(target_dir):
                if file.endswith(".jar") or file.endswith(".war"):
                    artifacts.append(os.path.join("target", file))
        
        if result.returncode == 0:
            return MavenResponse(
                success=True,
                message="Build completed successfully",
                output=result.stdout,
                build_artifacts=artifacts
            )
        else:
            return MavenResponse(
                success=False,
                message="Build failed",
                errors=[result.stderr]
            )
    except Exception as e:
        return MavenResponse(
            success=False,
            message=f"Build failed: {str(e)}",
            errors=[str(e)]
        )

@app.post("/verify-spring-boot", response_model=Dict)
async def verify_spring_boot_version(request: MavenRequest):
    """Verify Spring Boot version and determine if migration is needed"""
    try:
        # Parse pom.xml to find Spring Boot version
        pom_path = os.path.join(request.project_path, "pom.xml")
        if not os.path.exists(pom_path):
            raise HTTPException(status_code=404, detail="pom.xml not found")
        
        with open(pom_path, 'r') as f:
            pom_content = f.read()
        
        # Look for Spring Boot version
        spring_boot_version = None
        parent_version_match = re.search(r'<parent>.*?<artifactId>spring-boot-starter-parent</artifactId>.*?<version>(.*?)</version>.*?</parent>', 
                                       pom_content, re.DOTALL)
        if parent_version_match:
            spring_boot_version = parent_version_match.group(1)
        else:
            # Look in properties
            properties_match = re.search(r'<spring-boot.version>(.*?)</spring-boot.version>', pom_content)
            if properties_match:
                spring_boot_version = properties_match.group(1)
        
        if not spring_boot_version:
            return {
                "is_spring_boot": False,
                "current_version": None,
                "needs_migration": False
            }
        
        # Determine if migration is needed
        major_version = int(spring_boot_version.split('.')[0])
        needs_migration = major_version < 3
        
        return {
            "is_spring_boot": True,
            "current_version": spring_boot_version,
            "needs_migration": needs_migration,
            "recommended_version": "3.2.0" if needs_migration else None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    from config import MCP_SERVERS
    
    server_config = {
        "host": "localhost",
        "port": 8005
    }
    
    uvicorn.run(app, host=server_config["host"], port=server_config["port"]) 