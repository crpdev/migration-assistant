import os
import google.generativeai as genai
from typing import Dict, List, Optional, Tuple
import json
import asyncio
import httpx
from config import (
    GEMINI_API_KEY, MCP_SERVERS, RESPONSE_FORMAT, 
    DEFAULT_JAVA_VERSIONS, MIGRATION_TOOLS, RECIPE_TYPES,
    MIGRATION_TARGETS
)
from mcp.logger import MigrationLogger

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

class MigrationOrchestrator:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.history = []
        self.current_state = {}
        self.logger = MigrationLogger(project_path)
        self.reasoning_chain = []
    
    async def get_llm_reasoning(self, context: Dict) -> str:
        """Get LLM reasoning for the current state and next steps"""
        prompt = f"""
        Analyze the following migration context and provide reasoning for the next steps:
        Current State: {json.dumps(context, indent=2)}
        Previous Reasoning: {self.reasoning_chain[-1] if self.reasoning_chain else 'Initial state'}
        
        Please provide:
        1. Analysis of the current state
        2. Potential risks and challenges
        3. Recommended next steps
        4. Reasoning for the recommendations
        """
        
        response = model.generate_content(prompt)
        reasoning = response.text
        self.reasoning_chain.append(reasoning)
        return reasoning

    async def prompt_user(self, message: str, options: Optional[List[str]] = None) -> str:
        """Prompt user for input with optional choices"""
        print("\n" + "="*80)
        print(message)
        if options:
            print("\nOptions:")
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")
        
        while True:
            response = input("\nYour response (or 'q' to quit): ").strip()
            if response.lower() == 'q':
                raise Exception("Migration cancelled by user")
            
            if options:
                try:
                    idx = int(response) - 1
                    if 0 <= idx < len(options):
                        return options[idx]
                except ValueError:
                    pass
                print("Please select a valid option")
            else:
                return response

    async def explore_project(self, project_path: str) -> Dict:
        """Explore project structure with user confirmation"""
        self.logger.log_step("Project Exploration", {"status": "started"})
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://{MCP_SERVERS['file_explorer']['host']}:{MCP_SERVERS['file_explorer']['port']}/explore",
                json={"path": project_path, "file_types": ["pom.xml", "java"]}
            )
            result = response.json()
            
            self.logger.log_step("Project Structure", {
                "files_found": len(result.get("files", [])),
                "directories": result.get("directories", []),
                "file_types": result.get("file_types", {})
            })
            
            await self.prompt_user(
                "Project structure has been analyzed. Would you like to proceed with the migration?",
                ["Yes", "No"]
            )
            
            return result
    
    async def analyze_pom(self, pom_path: str) -> Dict:
        """Analyze POM file with user confirmation"""
        self.logger.log_step("POM Analysis", {"status": "started", "pom_path": pom_path})
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://{MCP_SERVERS['file_parser']['host']}:{MCP_SERVERS['file_parser']['port']}/parse/pom",
                json={"file_path": pom_path, "file_type": "pom"}
            )
            result = response.json()
            
            reasoning = await self.get_llm_reasoning({
                "step": "POM Analysis",
                "result": result
            })
            
            self.logger.log_step("POM Analysis Results", {
                "dependencies": result.get("dependencies", []),
                "properties": result.get("properties", {}),
                "reasoning": reasoning
            })
            
            await self.prompt_user(
                f"POM analysis complete. Reasoning:\n{reasoning}\n\nProceed with dependency analysis?",
                ["Yes", "No"]
            )
            
            return result
    
    async def verify_spring_boot(self, project_path: str) -> Dict:
        """Verify Spring Boot version with user confirmation"""
        self.logger.log_step("Spring Boot Verification", {"status": "started"})
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://{MCP_SERVERS['maven']['host']}:{MCP_SERVERS['maven']['port']}/verify-spring-boot",
                json={"project_path": project_path}
            )
            result = response.json()
            
            reasoning = await self.get_llm_reasoning({
                "step": "Spring Boot Verification",
                "result": result
            })
            
            self.logger.log_step("Spring Boot Analysis", {
                "is_spring_boot": result.get("is_spring_boot"),
                "current_version": result.get("current_version"),
                "needs_migration": result.get("needs_migration"),
                "reasoning": reasoning
            })
            
            if result.get("is_spring_boot"):
                await self.prompt_user(
                    f"Spring Boot analysis complete. Reasoning:\n{reasoning}\n\nProceed with Spring Boot migration?",
                    ["Yes", "No"]
                )
            
            return result
    
    async def compile_project(self, project_path: str) -> Dict:
        """Compile project with user confirmation"""
        self.logger.log_step("Project Compilation", {"status": "started"})
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://{MCP_SERVERS['maven']['host']}:{MCP_SERVERS['maven']['port']}/compile",
                json={"project_path": project_path, "goals": ["compile"]}
            )
            result = response.json()
            
            reasoning = await self.get_llm_reasoning({
                "step": "Project Compilation",
                "result": result
            })
            
            self.logger.log_step("Compilation Results", {
                "success": result.get("success"),
                "output": result.get("output"),
                "errors": result.get("errors"),
                "reasoning": reasoning
            })
            
            if not result.get("success"):
                await self.prompt_user(
                    f"Compilation failed. Reasoning:\n{reasoning}\n\nWould you like to continue anyway?",
                    ["Yes", "No"]
                )
            
            return result
    
    async def run_tests(self, project_path: str) -> Dict:
        """Run tests with user confirmation"""
        self.logger.log_step("Test Execution", {"status": "started"})
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://{MCP_SERVERS['maven']['host']}:{MCP_SERVERS['maven']['port']}/test",
                json={"project_path": project_path, "goals": ["test"]}
            )
            result = response.json()
            
            reasoning = await self.get_llm_reasoning({
                "step": "Test Execution",
                "result": result
            })
            
            self.logger.log_step("Test Results", {
                "success": result.get("success"),
                "test_results": result.get("test_results"),
                "errors": result.get("errors"),
                "reasoning": reasoning
            })
            
            if not result.get("success"):
                await self.prompt_user(
                    f"Tests failed. Reasoning:\n{reasoning}\n\nWould you like to continue anyway?",
                    ["Yes", "No"]
                )
            
            return result
    
    async def build_project(self, project_path: str, skip_tests: bool = False) -> Dict:
        """Build project with user confirmation"""
        self.logger.log_step("Project Build", {"status": "started", "skip_tests": skip_tests})
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://{MCP_SERVERS['maven']['host']}:{MCP_SERVERS['maven']['port']}/build",
                json={"project_path": project_path, "goals": ["clean", "install"], "skip_tests": skip_tests}
            )
            result = response.json()
            
            reasoning = await self.get_llm_reasoning({
                "step": "Project Build",
                "result": result
            })
            
            self.logger.log_step("Build Results", {
                "success": result.get("success"),
                "output": result.get("output"),
                "errors": result.get("errors"),
                "build_artifacts": result.get("build_artifacts"),
                "reasoning": reasoning
            })
            
            if not result.get("success"):
                await self.prompt_user(
                    f"Build failed. Reasoning:\n{reasoning}\n\nWould you like to retry?",
                    ["Yes", "No"]
                )
            
            return result
    
    async def get_migration_strategy(self, analysis: Dict) -> Dict:
        prompt = f"""
        Analyze the following Java project analysis and propose a migration strategy:
        Current Java Version: {analysis.get('java_version')}
        Dependencies: {json.dumps(analysis.get('dependencies', []), indent=2)}
        
        Please provide a structured response with:
        1. Recommended target Java version
        2. Dependencies that need updating
        3. Potential migration challenges
        4. Step-by-step migration plan
        
        Format the response as a JSON object with these keys:
        - target_version
        - dependencies_to_update
        - challenges
        - migration_steps
        """
        
        response = model.generate_content(prompt)
        return json.loads(response.text)
    
    async def determine_migration_path(self, project_path: str, pom_analysis: Dict) -> Tuple[str, Dict]:
        """Determine the migration path based on project analysis"""
        # Check if it's a Spring Boot project
        spring_boot_info = await self.verify_spring_boot(project_path)
        
        if spring_boot_info.get("is_spring_boot") and spring_boot_info.get("needs_migration"):
            # Spring Boot 2.x to 3.x migration
            return "spring_boot", MIGRATION_TARGETS["spring_boot"]["2.x"]
        
        # Java version migration
        java_version = pom_analysis.get("java_version", "8")
        major_version = java_version.split('.')[0]
        
        if major_version in MIGRATION_TARGETS["java"]:
            return "java", MIGRATION_TARGETS["java"][major_version]
        
        return None, None
    
    async def analyze_with_migration_tool(self, project_path: str, tool: str, source_version: str, target_version: str) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://{MCP_SERVERS['migration_tools']['host']}:{MCP_SERVERS['migration_tools']['port']}/analyze",
                json={
                    "project_path": project_path,
                    "tool": tool,
                    "recipe_type": "java_upgrade",
                    "source_version": source_version,
                    "target_version": target_version
                }
            )
            return response.json()
    
    async def execute_migration(self, project_path: str, strategy: Dict, tool: str, recipe: str = None) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://{MCP_SERVERS['migration_tools']['host']}:{MCP_SERVERS['migration_tools']['port']}/execute",
                json={
                    "project_path": project_path,
                    "tool": tool,
                    "recipe_type": "java_upgrade",
                    "source_version": self.current_state.get("java_version"),
                    "target_version": strategy["target_version"],
                    "dependencies": strategy.get("dependencies_to_update", []),
                    "custom_recipe": {"recipe": recipe} if recipe else None
                }
            )
            return response.json()
    
    def update_history(self, step: str, result: Dict):
        self.history.append({"step": step, "result": result})
        self.current_state.update(result)
    
    async def run_migration(self, project_path: str):
        """Run the complete migration process with user interaction and reasoning"""
        try:
            # Step 1: Initial project exploration
            project_structure = await self.explore_project(project_path)
            
            # Step 2: Analyze POM
            pom_files = [f for f in project_structure["files"] if f["type"] == "xml"]
            if not pom_files:
                raise Exception("No POM files found in the project")
            
            pom_analysis = await self.analyze_pom(pom_files[0]["path"])
            
            # Step 3: Verify Spring Boot
            spring_boot_info = await self.verify_spring_boot(project_path)
            
            # Step 4: Initial compilation
            compile_result = await self.compile_project(project_path)
            
            # Step 5: Run tests
            test_result = await self.run_tests(project_path)
            
            # Step 6: Determine migration path
            migration_type, migration_target = await self.determine_migration_path(project_path, pom_analysis)
            
            if migration_type and migration_target:
                reasoning = await self.get_llm_reasoning({
                    "step": "Migration Path Determination",
                    "migration_type": migration_type,
                    "migration_target": migration_target
                })
                
                self.logger.log_step("Migration Path", {
                    "type": migration_type,
                    "target": migration_target,
                    "reasoning": reasoning
                })
                
                await self.prompt_user(
                    f"Migration path determined. Reasoning:\n{reasoning}\n\nProceed with migration?",
                    ["Yes", "No"]
                )
                
                # Step 7: Execute migration
                migration_result = await self.execute_migration(
                    project_path,
                    {"target_version": migration_target["target"]},
                    "openrewrite",
                    migration_target["recipe"]
                )
                
                # Step 8: Post-migration verification
                post_compile = await self.compile_project(project_path)
                post_tests = await self.run_tests(project_path)
                final_build = await self.build_project(project_path)
                
                # Generate final report
                report_path = self.logger.generate_html_report()
                
                return {
                    "success": True,
                    "message": "Migration completed successfully",
                    "report_path": report_path,
                    "history": self.history,
                    "final_state": self.current_state
                }
            
            else:
                reasoning = await self.get_llm_reasoning({
                    "step": "Migration Path Determination",
                    "result": "No predetermined migration path found"
                })
                
                self.logger.log_step("Migration Analysis", {
                    "status": "no_path_found",
                    "reasoning": reasoning
                })
                
                return {
                    "success": False,
                    "message": "No migration path found",
                    "reasoning": reasoning,
                    "history": self.history
                }
        
        except Exception as e:
            self.logger.log_step("Migration Error", {
                "error": str(e),
                "status": "error"
            })
            
            return {
                "success": False,
                "error": str(e),
                "history": self.history
            }

async def main():
    # Get project path from user
    project_path = input("Enter the path to your Java/Maven project: ")
    
    # Initialize orchestrator
    orchestrator = MigrationOrchestrator(project_path)
    
    # Run migration
    result = await orchestrator.run_migration(project_path)
    
    # Print results
    if result["success"]:
        print("\nMigration completed successfully!")
        print(f"Detailed report generated at: {result['report_path']}")
    else:
        print("\nMigration failed!")
        print(f"Error: {result.get('error') or result.get('message')}")
        if result.get('reasoning'):
            print(f"\nReasoning:\n{result['reasoning']}")

if __name__ == "__main__":
    asyncio.run(main()) 