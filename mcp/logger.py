import logging
import os
from datetime import datetime
from typing import Dict, List, Any
import json

class MigrationLogger:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.log_dir = os.path.join(project_path, "migration_logs")
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"migration_{self.timestamp}.log")
        self.report_file = os.path.join(self.log_dir, f"migration_report_{self.timestamp}.html")
        self.migration_steps = []
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        os.makedirs(self.log_dir, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("MigrationLogger")

    def log_step(self, step_name: str, details: Dict[str, Any], status: str = "info"):
        """Log a migration step with details"""
        step_data = {
            "timestamp": datetime.now().isoformat(),
            "step": step_name,
            "details": details,
            "status": status
        }
        self.migration_steps.append(step_data)
        
        if status == "error":
            self.logger.error(f"{step_name}: {json.dumps(details)}")
        elif status == "warning":
            self.logger.warning(f"{step_name}: {json.dumps(details)}")
        else:
            self.logger.info(f"{step_name}: {json.dumps(details)}")

    def generate_html_report(self) -> str:
        """Generate HTML report from migration steps"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Migration Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .step { margin-bottom: 20px; padding: 10px; border: 1px solid #ddd; }
                .success { background-color: #dff0d8; }
                .error { background-color: #f2dede; }
                .warning { background-color: #fcf8e3; }
                .details { margin-left: 20px; }
                .timestamp { color: #666; font-size: 0.8em; }
                pre { background-color: #f5f5f5; padding: 10px; }
            </style>
        </head>
        <body>
            <h1>Migration Report</h1>
            <p>Project: {project_path}</p>
            <p>Migration completed at: {timestamp}</p>
            <h2>Migration Steps</h2>
            {steps}
        </body>
        </html>
        """

        steps_html = ""
        for step in self.migration_steps:
            status_class = step["status"]
            details_html = ""
            for key, value in step["details"].items():
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, indent=2)
                details_html += f"<p><strong>{key}:</strong> <pre>{value}</pre></p>"

            steps_html += f"""
            <div class="step {status_class}">
                <h3>{step['step']}</h3>
                <p class="timestamp">{step['timestamp']}</p>
                <div class="details">
                    {details_html}
                </div>
            </div>
            """

        html_content = html_template.format(
            project_path=self.project_path,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            steps=steps_html
        )

        with open(self.report_file, 'w') as f:
            f.write(html_content)

        return self.report_file 