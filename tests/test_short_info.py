from datetime import datetime
from log_monitor import analyze_jobs

def test_short_job_info(log_capture):
    jobs = {
        '12345': {
            'start': datetime.strptime('10:00:00', '%H:%M:%S'),
            'end': datetime.strptime('10:02:30', '%H:%M:%S'),
            'desc': 'short job'
        }
    }
    analyze_jobs(jobs)
    logs = log_capture.getvalue()
    assert "completed in 150s" in logs
    assert "INFO" in logs