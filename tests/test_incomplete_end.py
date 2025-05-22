from datetime import datetime
from log_monitor import analyze_jobs

def test_missing_end(log_capture):
    jobs = {
        '12345': {
            'start': datetime.strptime('13:00:00', '%H:%M:%S'),
            'desc': 'missing end'
        }
    }
    analyze_jobs(jobs)
    logs = log_capture.getvalue()
    assert "is incomplete (missing start or end time)" in logs
    assert "WARNING" in logs
