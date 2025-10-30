import os
from datetime import datetime

# Configuration Information
CML_USERNAME = 'admin'
CML_PASSWORD = 'Skills39'
CML_CONTROLLER = '192.168.159.250'  # IP CML
ENABLE_SECRET = 'Skill39!'
LAB_NAME = 'Module_C'

# HTML Report Configuration
HTML_OUTPUT_DIR = "./html_reports"
HTML_FILENAME = f"AutoMakringReport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
HTML_FILEPATH = os.path.join(HTML_OUTPUT_DIR, HTML_FILENAME)
