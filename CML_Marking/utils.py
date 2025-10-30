from datetime import datetime

class CheckResult:
    def __init__(self, title, status_text, passed, score, raw_output="", note=None):
        self.title = title
        self.status_text = status_text
        self.passed = passed
        self.score = score
        self.raw_output = raw_output
        self.note = note

# Result List and Score Statistics
global_results = []
global_total_score = 0.00
global_max_score = 0.00

def add_check_result(title, status_text, passed, score, raw_output="", note=None):
    global global_total_score, global_max_score
    result = CheckResult(title, status_text, passed, score, raw_output, note=note)
    global_results.append(result)
    global_max_score += score
    if passed:
        global_total_score += score
    return result
