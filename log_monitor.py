# log_monitor.py
import csv
from datetime import datetime, timedelta
import logging
from collections import defaultdict

# Setup logging configuration to print to stdout
def configure_logging(level):
    """

    Configures the logging level based on the provided string to filter output.

    """
    level_map = {
        'INFO': logging.INFO,
        'WARN': logging.WARNING,
        'ERROR': logging.ERROR
    }
    logging.basicConfig(
        level=level_map.get(level.upper(), logging.INFO),
        format='%(levelname)s - %(message)s'
    )

def parse_log_file(filepath):
    """

    Parses log file and returns dictionary mapping PIDs to their start/end times and description.

    """
    jobs = defaultdict(dict)

    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for time_str, description, status, pid in reader:
            # Parse and normalize each CSV field:
            # - Convert time string to datetime object
            # - Strip whitespace from job description, status, and PID
            # - These fields are then used to map START and END times to each PID
            timestamp = datetime.strptime(time_str.strip(), "%H:%M:%S")
            description = description.strip()
            status = status.strip()
            pid = pid.strip()

            # Record start time and description
            if status == 'START':
                jobs[pid]['start'] = timestamp
                jobs[pid]['desc'] = description
            # Record end time
            elif status == 'END':
                jobs[pid]['end'] = timestamp

    return jobs

def analyze_jobs(jobs):
    """
    Analyzes job durations and logs messages based on thresholds statically set via requirements.

    Args:
        jobs (dict): Dictionary of job data with start and end times.
    """
    incomplete = []
    messages = []

    for pid, data in jobs.items():
        start = data.get('start')
        end = data.get('end')
        desc = data.get('desc', f"PID {pid}")

        # Capture jobs missing start or end timestamps - handle as errors
        if not start or not end:
            incomplete.append((logging.WARNING, f"Job '{desc}' (PID {pid}) is incomplete (missing start or end time)."))
            continue

        # Handle jobs that span past midnight (assuming timestamps are in 24-hour format)
        if end < start:
            end += timedelta(days=1)

        # Calculate job duration in seconds
        duration = (end - start).total_seconds()

        # Build formatted message
        if duration > 600:
            message = f"Job '{desc}' (PID {pid}) exceeded time limit: {duration:.0f}s (>10 minutes)"
            level = logging.ERROR
        elif duration > 300:
            message = f"Job '{desc}' (PID {pid}) took longer than expected: {duration:.0f}s (>5 minutes)"
            level = logging.WARNING
        else:
            message = f"Job '{desc}' (PID {pid}) completed in {duration:.0f}s"
            level = logging.INFO

        messages.append((level, message))

    # Sort logs into order by severity, then pass incomplete logs last (Show as a warning as they may still be inflight jobs)
    severity_order = {logging.ERROR: 0, logging.WARNING: 1, logging.INFO: 2}
    messages.sort(key=lambda x: severity_order.get(x[0], 3))
    all_messages = messages + incomplete

    for level, message in all_messages:
        logging.log(level, message)

def main():
    """

    CLI entrypoint that parses arguments, reads the log file, and analyzes job durations.

    """
    import argparse

    parser = argparse.ArgumentParser(description="Monitor job durations from a log file.")
    parser.add_argument('-f', '--file', default='logs.log', help="Path to the CSV file. Default: logs.log")
    parser.add_argument('-l', '--log-level', default='WARN', help="Set the logging verbosity level (INFO, WARN, ERROR). Default: WARN")
    args = parser.parse_args()

    configure_logging(args.log_level)  # Setup logging level
    job_data = parse_log_file(args.file)  # Parse the log file
    analyze_jobs(job_data)  # Analyze durations and log based on configured level

if __name__ == "__main__":
    main()