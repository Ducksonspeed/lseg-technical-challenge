from datetime import datetime
from log_monitor import analyze_jobs

def test_missing_start(log_capture):
    jobs = {
        '12345': {
            'end': datetime.strptime('13:10:00', '%H:%M:%S'),
            'desc': 'missing start'
        }
    }
    analyze_jobs(jobs)
    logs = log_capture.getvalue()
    assert "is incomplete (missing start or end time)" in logs
    assert "WARNING" in logs