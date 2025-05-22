from datetime import datetime
from log_monitor import analyze_jobs

def test_rollover_job(log_capture):
    jobs = {
        '12345': {
            'start': datetime.strptime('23:59:00', '%H:%M:%S'),
            'end': datetime.strptime('00:04:30', '%H:%M:%S'),
            'desc': 'overnight job test'
        }
    }

    analyze_jobs(jobs)

    logs = log_capture.getvalue()
    assert "took longer than expected: 330s" in logs
    assert "WARNING" in logs
    assert "overnight job test" in logs