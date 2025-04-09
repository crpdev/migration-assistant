# Java Migration Assistant

An AI-powered tool for migrating Java/Maven projects, available as both a Python application and a VS Code extension.

## Features

- Automated Java/Maven project migration
- Spring Boot version upgrades
- Dependency analysis and updates
- Interactive migration process with user confirmation
- Detailed logging and HTML reports
- AI-powered reasoning for migration decisions
- Real-time progress tracking
- Comprehensive error handling

## Prerequisites

### For Python Mode
- Python 3.8 or higher
- Java Development Kit (JDK) 8 or higher
- Maven 3.6 or higher
- Access to MCP servers (file explorer, file parser, maven)
- Gemini API key

### For VS Code Extension Mode
- Visual Studio Code 1.60 or higher
- Java Extension Pack for VS Code
- Java Development Kit (JDK) 8 or higher
- Maven 3.6 or higher
- Access to MCP servers (file explorer, file parser, maven)
- Gemini API key

## LLM Integration

The Java Migration Assistant uses Google's Gemini LLM to provide intelligent migration strategies and reasoning. The LLM is used in both Python and VS Code extension modes for:

1. **Migration Analysis**
   - Project structure analysis
   - Dependency compatibility assessment
   - Migration path determination
   - Risk analysis

2. **Reasoning Generation**
   - Step-by-step migration reasoning
   - Potential issues identification
   - Best practices recommendations
   - Alternative approaches

3. **Error Analysis**
   - Compilation error analysis
   - Test failure interpretation
   - Migration failure diagnosis
   - Solution suggestions

### LLM Configuration

#### Python Mode
Configure the LLM in `config.py`:
```python
# Gemini API Configuration
GEMINI_API_KEY = 'your-api-key-here'

# LLM Model Settings
LLM_SETTINGS = {
    'model': 'gemini-pro',
    'temperature': 0.7,
    'max_tokens': 2048,
    'top_p': 0.95,
    'frequency_penalty': 0.0,
    'presence_penalty': 0.0
}

# Custom Prompts (optional)
CUSTOM_PROMPTS = {
    'analysis': "Analyze the following Java project for migration...",
    'reasoning': "Provide reasoning for the following migration step...",
    'error': "Analyze the following error and suggest solutions..."
}
```

#### VS Code Extension Mode
Configure the LLM through VS Code settings:
```json
{
  "javaMigrationAssistant.geminiApiKey": "your-api-key-here",
  "javaMigrationAssistant.llmSettings": {
    "model": "gemini-pro",
    "temperature": 0.7,
    "maxTokens": 2048,
    "topP": 0.95,
    "frequencyPenalty": 0.0,
    "presencePenalty": 0.0
  },
  "javaMigrationAssistant.customPrompts": {
    "analysis": "Analyze the following Java project for migration...",
    "reasoning": "Provide reasoning for the following migration step...",
    "error": "Analyze the following error and suggest solutions..."
  }
}
```

### Customizing LLM Behavior

1. **Temperature**
   - Lower values (0.1-0.3): More focused, deterministic responses
   - Higher values (0.7-0.9): More creative, diverse suggestions
   - Default: 0.7 (balanced between focus and creativity)

2. **Max Tokens**
   - Controls response length
   - Default: 2048 (sufficient for detailed analysis)
   - Increase for more detailed responses
   - Decrease for more concise outputs

3. **Custom Prompts**
   - Modify the prompts to focus on specific aspects
   - Add domain-specific context
   - Include project-specific requirements
   - Customize error analysis approach

4. **Response Format**
   - Structured JSON output for consistent parsing
   - Markdown formatting for better readability
   - HTML integration for reports
   - Custom formatting for specific needs

### LLM Usage Examples

1. **Project Analysis**
```python
# Python Mode
reasoning = await orchestrator.get_llm_reasoning({
    "step": "Project Analysis",
    "project_structure": project_structure,
    "dependencies": dependencies
})
```

2. **Migration Strategy**
```python
# Python Mode
strategy = await orchestrator.get_migration_strategy({
    "current_version": "1.5.22",
    "target_version": "2.7.0",
    "dependencies": dependencies,
    "project_type": "spring-boot"
})
```

3. **Error Analysis**
```python
# Python Mode
error_analysis = await orchestrator.get_llm_reasoning({
    "step": "Error Analysis",
    "error": compilation_error,
    "context": {
        "step": "Compilation",
        "file": "MainApplication.java",
        "line": 42
    }
})
```

### Best Practices

1. **API Key Management**
   - Store API keys securely
   - Use environment variables when possible
   - Rotate keys regularly
   - Monitor API usage

2. **Prompt Engineering**
   - Be specific in prompts
   - Include relevant context
   - Use clear instructions
   - Test and refine prompts

3. **Error Handling**
   - Implement fallback strategies
   - Log LLM responses
   - Handle API limits
   - Provide user feedback

4. **Performance Optimization**
   - Cache common responses
   - Batch similar requests
   - Optimize token usage
   - Monitor response times

## Installation

### Python Mode

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd java-migration-assistant
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the MCP servers in `config.py`:
   ```python
   MCP_SERVERS = {
       'file_explorer': {'host': 'localhost', 'port': 8001},
       'file_parser': {'host': 'localhost', 'port': 8002},
       'maven': {'host': 'localhost', 'port': 8003}
   }
   ```

5. Set up your Gemini API key in `config.py`:
   ```python
   GEMINI_API_KEY = 'your-api-key-here'
   ```

### VS Code Extension Mode

1. Install the extension from VS Code Marketplace:
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Java Migration Assistant"
   - Click Install

2. Configure the extension:
   - Open VS Code Settings (Ctrl+,)
   - Search for "Java Migration Assistant"
   - Configure the following settings:
     ```json
     {
       "javaMigrationAssistant.mcpServers": {
         "fileExplorer": { "host": "localhost", "port": 8001 },
         "fileParser": { "host": "localhost", "port": 8002 },
         "maven": { "host": "localhost", "port": 8003 }
       },
       "javaMigrationAssistant.geminiApiKey": "your-api-key-here"
     }
     ```

## Usage

### Python Mode

1. Activate your virtual environment if not already activated:
   ```bash
   # On Windows
   .\venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

2. Run the migration assistant:
   ```bash
   python main.py
   ```

3. When prompted, enter the path to your Java/Maven project.

4. Follow the interactive prompts to complete the migration.

### VS Code Extension Mode

1. Open your Java/Maven project in VS Code.

2. Start the migration:
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Start Java Migration"
   - Press Enter

3. The migration process will begin, and you can:
   - View progress in the Migration Steps view
   - See detailed information in the Migration Report view
   - Interact with confirmation dialogs
   - View the final report in a new editor

## Migration Process

The migration process includes the following steps:

1. Project Exploration
   - Analyzes project structure
   - Identifies key files and dependencies

2. POM Analysis
   - Parses pom.xml
   - Identifies dependencies and properties

3. Spring Boot Verification
   - Checks if project uses Spring Boot
   - Determines current version

4. Initial Compilation
   - Verifies project compiles successfully
   - Identifies any compilation issues

5. Test Execution
   - Runs project tests
   - Ensures test coverage

6. Migration Path Determination
   - Analyzes current state
   - Determines optimal migration path

7. Migration Execution
   - Updates dependencies
   - Modifies code as needed
   - Applies migration recipes

8. Post-migration Verification
   - Recompiles project
   - Runs tests again
   - Verifies changes

9. Report Generation
   - Creates detailed HTML report
   - Includes all steps and changes

## Requirements

### Python Dependencies
```
google.generativeai==0.1.0
httpx==0.24.0
```

### VS Code Extension Dependencies
```json
{
  "dependencies": {
    "google.generativeai": "^0.1.0",
    "httpx": "^0.24.0"
  }
}
```

### System Requirements
- Operating System: Windows 10/11, macOS 10.15+, or Linux
- Memory: 4GB RAM minimum (8GB recommended)
- Disk Space: 500MB minimum
- Internet Connection: Required for API access

### MCP Server Requirements
- File Explorer Server: Port 8001
- File Parser Server: Port 8002
- Maven Server: Port 8003

## Troubleshooting

### Common Issues

1. MCP Server Connection
   - Ensure all MCP servers are running
   - Verify correct host and port configurations
   - Check firewall settings

2. API Key Issues
   - Verify Gemini API key is correctly set
   - Ensure API key has sufficient permissions
   - Check API quota limits

3. Java/Maven Issues
   - Verify Java and Maven installations
   - Check JAVA_HOME environment variable
   - Ensure Maven is in system PATH

### Getting Help

- Check the logs in the `logs` directory
- Review the HTML report for detailed information
- Submit issues on the GitHub repository

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

### LLM Prompt Examples

Here are specific examples of LLM prompts used in different migration scenarios:

1. **Spring Boot Version Migration**
```python
SPRING_BOOT_MIGRATION_PROMPT = """
Analyze the following Spring Boot project for migration from version {current_version} to {target_version}:

Project Structure:
{project_structure}

Dependencies:
{dependencies}

Please provide:
1. Breaking changes between versions
2. Required dependency updates
3. Code modifications needed
4. Potential risks and mitigation strategies
5. Step-by-step migration plan

Format the response as JSON with the following structure:
{
    "breaking_changes": [],
    "dependency_updates": [],
    "code_modifications": [],
    "risks": [],
    "migration_steps": []
}
"""
```

2. **Java Version Upgrade**
```python
JAVA_VERSION_UPGRADE_PROMPT = """
Analyze the Java project for migration from Java {current_version} to Java {target_version}:

Source Code:
{source_code}

Build Configuration:
{build_config}

Please analyze:
1. Language feature compatibility
2. API changes and deprecations
3. Performance implications
4. Required code modifications
5. Testing requirements

Provide a detailed analysis with specific code examples and recommendations.
"""
```

3. **Dependency Conflict Resolution**
```python
DEPENDENCY_CONFLICT_PROMPT = """
Analyze the following dependency conflicts in the Maven project:

Conflicts:
{conflicts}

Current Dependencies:
{dependencies}

Please:
1. Identify the root cause of conflicts
2. Suggest compatible versions
3. Propose alternative dependencies if needed
4. Assess impact on existing functionality
5. Provide a resolution strategy

Include specific version recommendations and explain the reasoning.
"""
```

4. **Migration Error Analysis**
```python
MIGRATION_ERROR_PROMPT = """
Analyze the following migration error:

Error Message:
{error_message}

Context:
- Step: {step_name}
- File: {file_name}
- Line: {line_number}
- Previous Steps: {previous_steps}

Please provide:
1. Error root cause analysis
2. Impact assessment
3. Possible solutions with pros/cons
4. Recommended fix
5. Prevention strategies for future

Format the response with clear sections and code examples where relevant.
"""
```

5. **Test Compatibility Check**
```python
TEST_COMPATIBILITY_PROMPT = """
Analyze test compatibility for the following migration:

Current Tests:
{test_files}

Migration Changes:
{migration_changes}

Please evaluate:
1. Test framework compatibility
2. Required test modifications
3. New test cases needed
4. Test coverage gaps
5. Migration testing strategy

Provide specific recommendations for each test file and testing approach.
"""
```

6. **Performance Impact Analysis**
```python
PERFORMANCE_ANALYSIS_PROMPT = """
Analyze potential performance impacts of the following migration:

Current Metrics:
{current_metrics}

Proposed Changes:
{migration_changes}

Please assess:
1. Expected performance changes
2. Bottleneck identification
3. Optimization opportunities
4. Monitoring requirements
5. Performance testing strategy

Include specific metrics to track and benchmark recommendations.
"""
```

7. **Security Assessment**
```python
SECURITY_ASSESSMENT_PROMPT = """
Assess security implications of the following migration:

Current Security:
{security_config}

Migration Changes:
{migration_changes}

Please evaluate:
1. Security vulnerability risks
2. Dependency security updates
3. Required security configurations
4. Best practices compliance
5. Security testing requirements

Provide a comprehensive security analysis with specific recommendations.
"""
```

8. **Custom Migration Recipe**
```python
CUSTOM_RECIPE_PROMPT = """
Generate a custom migration recipe for the following scenario:

Project Type: {project_type}
Current State: {current_state}
Target State: {target_state}
Special Requirements: {requirements}

Please create:
1. Step-by-step migration instructions
2. Required code transformations
3. Validation checks
4. Rollback procedures
5. Success criteria

Format as a structured recipe with clear steps and code examples.
"""
```

These prompts can be customized based on your specific needs by:
1. Adding project-specific context
2. Including domain-specific requirements
3. Modifying the response format
4. Adding additional analysis criteria
5. Incorporating custom validation rules

Example usage in code:
```python
# Python Mode
async def analyze_migration_path(self, project_path: str, pom_analysis: Dict) -> Tuple[str, Dict]:
    prompt = SPRING_BOOT_MIGRATION_PROMPT.format(
        current_version=pom_analysis.get("spring_boot_version", "unknown"),
        target_version="2.7.0",
        project_structure=json.dumps(self.project_structure, indent=2),
        dependencies=json.dumps(pom_analysis.get("dependencies", []), indent=2)
    )
    
    response = await self.get_llm_response(prompt)
    analysis = json.loads(response)
    
    return analysis.get("migration_type"), analysis.get("migration_target")
```

### LLM Learning and Multi-turn Interactions

The Java Migration Assistant uses advanced LLM capabilities to learn from previous results and engage in multi-turn conversations to refine migration strategies.

#### Learning from Previous Results

1. **Dependency Resolution Learning**
```python
# First attempt at dependency resolution
async def resolve_dependency_conflicts(self, conflicts: List[Dict]) -> Dict:
    prompt = DEPENDENCY_CONFLICT_PROMPT.format(
        conflicts=json.dumps(conflicts, indent=2),
        dependencies=json.dumps(self.current_dependencies, indent=2)
    )
    
    response = await self.get_llm_response(prompt)
    resolution = json.loads(response)
    
    # Store the resolution attempt for learning
    self.resolution_history.append({
        "conflicts": conflicts,
        "resolution": resolution,
        "success": False  # Will be updated after verification
    })
    
    return resolution

# Second attempt with learning from previous failures
async def resolve_dependency_conflicts_with_learning(self, conflicts: List[Dict]) -> Dict:
    # Include previous resolution attempts in the prompt
    previous_attempts = self.resolution_history[-3:] if self.resolution_history else []
    
    prompt = DEPENDENCY_CONFLICT_WITH_HISTORY_PROMPT.format(
        conflicts=json.dumps(conflicts, indent=2),
        dependencies=json.dumps(self.current_dependencies, indent=2),
        previous_attempts=json.dumps(previous_attempts, indent=2)
    )
    
    response = await self.get_llm_response(prompt)
    resolution = json.loads(response)
    
    # Store the new resolution attempt
    self.resolution_history.append({
        "conflicts": conflicts,
        "resolution": resolution,
        "success": False  # Will be updated after verification
    })
    
    return resolution
```

2. **Migration Path Refinement**
```python
# Refine migration path based on previous steps
async def refine_migration_path(self, current_step: str, results: Dict) -> Dict:
    # Include previous steps and their results
    previous_steps = self.migration_history[-5:] if self.migration_history else []
    
    prompt = MIGRATION_PATH_REFINEMENT_PROMPT.format(
        current_step=current_step,
        current_results=json.dumps(results, indent=2),
        previous_steps=json.dumps(previous_steps, indent=2),
        project_context=json.dumps(self.project_context, indent=2)
    )
    
    response = await self.get_llm_response(prompt)
    refined_path = json.loads(response)
    
    # Update migration history
    self.migration_history.append({
        "step": current_step,
        "results": results,
        "refined_path": refined_path
    })
    
    return refined_path
```

3. **Error Recovery Learning**
```python
# Learn from error recovery attempts
async def recover_from_error(self, error: Dict, context: Dict) -> Dict:
    # Include previous error recovery attempts
    previous_recoveries = self.error_recovery_history[-3:] if self.error_recovery_history else []
    
    prompt = ERROR_RECOVERY_WITH_HISTORY_PROMPT.format(
        error=json.dumps(error, indent=2),
        context=json.dumps(context, indent=2),
        previous_recoveries=json.dumps(previous_recoveries, indent=2)
    )
    
    response = await self.get_llm_response(prompt)
    recovery_plan = json.loads(response)
    
    # Store the recovery attempt
    self.error_recovery_history.append({
        "error": error,
        "context": context,
        "recovery_plan": recovery_plan,
        "success": False  # Will be updated after verification
    })
    
    return recovery_plan
```

#### Multi-turn Interaction Examples

1. **Interactive Migration Planning**
```python
# Multi-turn migration planning conversation
async def interactive_migration_planning(self, project_path: str) -> Dict:
    # Initial analysis
    initial_analysis = await self.analyze_project(project_path)
    
    # Start conversation with LLM
    conversation = []
    conversation.append({
        "role": "system",
        "content": "You are a Java migration expert. Help plan the migration of this project."
    })
    conversation.append({
        "role": "user",
        "content": f"Analyze this project and suggest a migration plan: {json.dumps(initial_analysis, indent=2)}"
    })
    
    # Get initial response
    response = await self.get_llm_conversation_response(conversation)
    conversation.append({
        "role": "assistant",
        "content": response
    })
    
    # Continue conversation with user input
    while True:
        # Get user feedback
        user_feedback = await self.prompt_user(
            "Do you want to modify the migration plan? (yes/no)",
            ["Yes", "No"]
        )
        
        if user_feedback.lower() == "no":
            break
        
        # Get specific modifications
        modification_request = await self.prompt_user(
            "What aspects of the plan would you like to modify?",
            ["Dependencies", "Migration Steps", "Timeline", "Other"]
        )
        
        # Add user request to conversation
        conversation.append({
            "role": "user",
            "content": f"Please modify the {modification_request} aspect of the migration plan."
        })
        
        # Get updated plan
        response = await self.get_llm_conversation_response(conversation)
        conversation.append({
            "role": "assistant",
            "content": response
        })
    
    # Finalize the plan
    final_plan = json.loads(conversation[-1]["content"])
    return final_plan
```

2. **Iterative Problem Solving**
```python
# Multi-turn problem solving for complex migration issues
async def solve_migration_problem(self, problem: Dict) -> Dict:
    # Initialize conversation
    conversation = []
    conversation.append({
        "role": "system",
        "content": "You are a Java migration expert. Help solve this migration problem."
    })
    conversation.append({
        "role": "user",
        "content": f"Solve this migration problem: {json.dumps(problem, indent=2)}"
    })
    
    # Get initial solution
    response = await self.get_llm_conversation_response(conversation)
    conversation.append({
        "role": "assistant",
        "content": response
    })
    
    # Try the solution
    solution = json.loads(response)
    result = await self.apply_solution(solution)
    
    # If solution failed, continue conversation
    if not result["success"]:
        conversation.append({
            "role": "user",
            "content": f"The solution failed with error: {json.dumps(result['error'], indent=2)}. Please provide an alternative solution."
        })
        
        # Get alternative solution
        response = await self.get_llm_conversation_response(conversation)
        conversation.append({
            "role": "assistant",
            "content": response
        })
        
        # Try the alternative solution
        solution = json.loads(response)
        result = await self.apply_solution(solution)
    
    # Continue until success or max attempts
    attempts = 1
    while not result["success"] and attempts < 3:
        conversation.append({
            "role": "user",
            "content": f"The solution still failed with error: {json.dumps(result['error'], indent=2)}. Please provide another alternative solution."
        })
        
        response = await self.get_llm_conversation_response(conversation)
        conversation.append({
            "role": "assistant",
            "content": response
        })
        
        solution = json.loads(response)
        result = await self.apply_solution(solution)
        attempts += 1
    
    return {
        "solution": solution,
        "success": result["success"],
        "attempts": attempts,
        "conversation": conversation
    }
```

3. **Adaptive Migration Strategy**
```python
# Adaptive migration strategy based on multi-turn feedback
async def adaptive_migration_strategy(self, project_path: str) -> Dict:
    # Initial strategy
    initial_strategy = await self.get_migration_strategy({
        "project_path": project_path,
        "current_state": await self.get_project_state(project_path)
    })
    
    # Start conversation
    conversation = []
    conversation.append({
        "role": "system",
        "content": "You are a Java migration expert. Help develop an adaptive migration strategy."
    })
    conversation.append({
        "role": "user",
        "content": f"Develop a migration strategy for this project: {json.dumps(initial_strategy, indent=2)}"
    })
    
    # Get initial strategy
    response = await self.get_llm_conversation_response(conversation)
    conversation.append({
        "role": "assistant",
        "content": response
    })
    
    # Execute first phase
    strategy = json.loads(response)
    phase_result = await self.execute_migration_phase(strategy["phases"][0])
    
    # Adapt strategy based on results
    conversation.append({
        "role": "user",
        "content": f"The first phase resulted in: {json.dumps(phase_result, indent=2)}. How should we adapt the strategy?"
    })
    
    # Get adapted strategy
    response = await self.get_llm_conversation_response(conversation)
    conversation.append({
        "role": "assistant",
        "content": response
    })
    
    # Continue adapting for each phase
    adapted_strategy = json.loads(response)
    for i in range(1, len(adapted_strategy["phases"])):
        phase_result = await self.execute_migration_phase(adapted_strategy["phases"][i])
        
        conversation.append({
            "role": "user",
            "content": f"Phase {i+1} resulted in: {json.dumps(phase_result, indent=2)}. How should we adapt the remaining strategy?"
        })
        
        response = await self.get_llm_conversation_response(conversation)
        conversation.append({
            "role": "assistant",
            "content": response
        })
        
        adapted_strategy = json.loads(response)
    
    return {
        "final_strategy": adapted_strategy,
        "conversation": conversation
    }
```

#### Prompt Templates for Learning and Multi-turn Interactions

1. **Dependency Conflict with History Prompt**
```python
DEPENDENCY_CONFLICT_WITH_HISTORY_PROMPT = """
Analyze the following dependency conflicts in the Maven project, taking into account previous resolution attempts:

Conflicts:
{conflicts}

Current Dependencies:
{dependencies}

Previous Resolution Attempts:
{previous_attempts}

Please:
1. Review previous resolution attempts and their outcomes
2. Identify patterns in successful and failed resolutions
3. Suggest a new resolution strategy based on this learning
4. Explain how this strategy addresses previous failures
5. Provide a detailed implementation plan

Format the response as JSON with the following structure:
{
    "analysis": {
        "previous_successes": [],
        "previous_failures": [],
        "learned_patterns": []
    },
    "resolution_strategy": {
        "approach": "",
        "reasoning": "",
        "steps": []
    },
    "implementation": {
        "dependency_updates": [],
        "version_changes": [],
        "additional_changes": []
    }
}
"""
```

2. **Migration Path Refinement Prompt**
```python
MIGRATION_PATH_REFINEMENT_PROMPT = """
Refine the migration path based on previous steps and their results:

Current Step: {current_step}
Current Results: {current_results}

Previous Steps and Results:
{previous_steps}

Project Context:
{project_context}

Please:
1. Analyze the outcomes of previous steps
2. Identify any deviations from the expected path
3. Suggest adjustments to the remaining migration steps
4. Provide reasoning for the refinements
5. Update the migration timeline if needed

Format the response as JSON with the following structure:
{
    "analysis": {
        "previous_outcomes": [],
        "deviations": [],
        "success_patterns": []
    },
    "refined_path": {
        "adjusted_steps": [],
        "new_steps": [],
        "removed_steps": [],
        "timeline_adjustments": []
    },
    "reasoning": {
        "adjustment_reasons": [],
        "risk_assessment": [],
        "mitigation_strategies": []
    }
}
"""
```

3. **Error Recovery with History Prompt**
```python
ERROR_RECOVERY_WITH_HISTORY_PROMPT = """
Develop a recovery plan for the following error, taking into account previous recovery attempts:

Error:
{error}

Context:
{context}

Previous Recovery Attempts:
{previous_recoveries}

Please:
1. Review previous recovery attempts and their outcomes
2. Identify why previous attempts may have failed
3. Propose a new recovery strategy based on this learning
4. Explain how this strategy addresses previous failures
5. Provide a detailed implementation plan

Format the response as JSON with the following structure:
{
    "analysis": {
        "error_root_cause": "",
        "previous_attempt_analysis": [],
        "failure_patterns": []
    },
    "recovery_strategy": {
        "approach": "",
        "reasoning": "",
        "steps": []
    },
    "implementation": {
        "code_changes": [],
        "configuration_changes": [],
        "verification_steps": []
    }
}
"""
```

These examples demonstrate how the Java Migration Assistant:
1. Learns from previous migration attempts
2. Adapts strategies based on outcomes
3. Engages in multi-turn conversations to refine approaches
4. Maintains conversation history for context
5. Provides structured responses for consistent processing 