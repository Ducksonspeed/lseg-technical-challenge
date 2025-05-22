from datetime import datetime
from log_monitor import analyze_jobs

def test_long_job_error(log_capture):
    jobs = {
        '12345': {
            'start': datetime.strptime('12:00:00', '%H:%M:%S'),
            'end': datetime.strptime('12:11:00', '%H:%M:%S'),
            'desc': 'long job'
        }
    }
    analyze_jobs(jobs)
    logs = log_capture.getvalue()
    assert "exceeded time limit: 660s" in logs
    assert "ERROR" in logs
