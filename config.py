import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# MCP Server Configuration
MCP_SERVERS = {
    "file_explorer": {
        "host": "localhost",
        "port": 8001
    },
    "file_parser": {
        "host": "localhost",
        "port": 8002
    },
    "migration_executor": {
        "host": "localhost",
        "port": 8003
    },
    "migration_tools": {
        "host": "localhost",
        "port": 8004
    },
    "maven": {
        "host": "localhost",
        "port": 8005
    }
}

# Response Format
RESPONSE_FORMAT = {
    "explicit_reasoning": True,
    "structured_output": True,
    "tool_separation": True,
    "conversation_loop": True,
    "instructional_framing": True,
    "internal_self_checks": False,
    "reasoning_type_awareness": False,
    "fallbacks": False,
    "overall_clarity": "Excellent structure, but could improve with self-checks and error fallbacks."
}

# Migration Tools
MIGRATION_TOOLS = {
    "openrewrite": "openrewrite",
    "moderne": "moderne"
}

# Default Java versions for migration
DEFAULT_JAVA_VERSIONS = {
    "source": ["8", "11", "17"],
    "target": "21"
}

# Recipe Types
RECIPE_TYPES = {
    "java_upgrade": "Upgrade Java version",
    "dependency_update": "Update dependencies",
    "code_cleanup": "Clean up code",
    "custom": "Custom recipe"
}

# Migration Targets
MIGRATION_TARGETS = {
    "java": {
        "8": {
            "target": "17",
            "recipe": "org.openrewrite.java.migrate.UpgradeToJava17"
        },
        "11": {
            "target": "17",
            "recipe": "org.openrewrite.java.migrate.UpgradeToJava17"
        },
        "17": {
            "target": "21",
            "recipe": "org.openrewrite.java.migrate.UpgradeToJava21"
        }
    },
    "spring_boot": {
        "2.x": {
            "target": "3.2.0",
            "recipe": "org.openrewrite.java.spring.boot3.SpringBoot2To3Migration"
        }
    }
} 