# Java Migration Assistant with Gemini LLM

This tool helps you migrate Java/Maven projects to newer versions using AI-powered analysis and automated migration tools. It integrates with Gemini LLM to provide intelligent migration strategies and uses OpenRewrite or Moderne CLI for actual code migration.

## Features

- Project structure analysis
- POM file parsing and dependency analysis
- AI-powered migration strategy generation
- Automated migration execution
- Step-by-step migration process with user confirmation
- Support for both OpenRewrite and Moderne CLI
- Detailed migration history and reporting

## Prerequisites

- Python 3.8+
- Java 8 or higher
- Maven
- Gemini API key
- OpenRewrite or Moderne CLI (depending on your choice)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd java-migration-assistant
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Gemini API key:
Create a `.env` file in the project root and add:
```
GEMINI_API_KEY=your_api_key_here
```

4. Install OpenRewrite or Moderne CLI (your choice):
- For OpenRewrite: Follow the [OpenRewrite documentation](https://docs.openrewrite.org/getting-started)
- For Moderne: Follow the [Moderne CLI documentation](https://docs.moderne.io/cli)

## Usage

1. Start the MCP servers:
```bash
# In separate terminals:
python mcp/file_explorer_server.py
python mcp/file_parser_server.py
python mcp/migration_executor_server.py
```

2. Run the migration assistant:
```bash
python main.py
```

3. Follow the prompts to:
   - Enter your project path
   - Review the analysis
   - Confirm migration steps
   - Choose migration tool (OpenRewrite or Moderne)

## Project Structure

```
.
├── main.py                 # Main orchestration script
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── mcp/                   # MCP servers
│   ├── file_explorer_server.py
│   ├── file_parser_server.py
│   └── migration_executor_server.py
└── README.md
```

## How It Works

1. **Project Exploration**: The tool scans your project structure to identify POM files and Java sources.

2. **POM Analysis**: It analyzes your POM file to understand:
   - Current Java version
   - Dependencies and their versions
   - Project properties

3. **AI Strategy**: Gemini LLM analyzes the project state and proposes:
   - Target Java version
   - Dependencies to update
   - Potential challenges
   - Step-by-step migration plan

4. **Migration Execution**: The tool executes the migration using your chosen tool (OpenRewrite or Moderne CLI).

5. **History Tracking**: All steps and their results are tracked and reported.

## Response Format

The tool uses a structured JSON format for responses:
```json
{
    "explicit_reasoning": true,
    "structured_output": true,
    "tool_separation": true,
    "conversation_loop": true,
    "instructional_framing": true,
    "internal_self_checks": false,
    "reasoning_type_awareness": false,
    "fallbacks": false,
    "overall_clarity": "Excellent structure, but could improve with self-checks and error fallbacks."
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 