# LSEG Technical Challenge - Log Monitoring Application

This script parses a log file to track job start/end times and flags jobs that exceed set thresholds. These thresholds are set to output a warning or a error based on the following conditions.

* Info: Output all job stats (must use argument `--level INFO`)
* Warning: Job took more than 5 minutes or are incomplete
* Error: Job took more than 10 minutes

## Script Usage

### CLI 

Discover available commands via the `--help` argument.

The input file can be selected via an argument `--file` or `-f`.

Output can be selected via an argument `--log-level` or `-l`  supporting the following inputs: `INFO, WARN, ERROR`.

```bash
python log_monitor.py -f logs.log
```

### Docker

#### Build CLI image
```bash
docker buildx build -t lseg-technical-challenge-cli --target cli .
```

#### Run CLI using existing `logs.log`
```bash
docker run --rm lseg-technical-challenge-cli
```

#### Run CLI using mounted file (assumed file name is `logs.log`)
Commands can be sent to the container such as 
`docker run --rm -v "$PWD":/app lseg-technical-challenge-cli -f someotherfile.log -l INFO`

```bash
docker run --rm -v "$PWD":/app lseg-technical-challenge-cli
```

## Test Cases

### CLI

#### Requirements:

```bash
pip install -r requirements.txt
```
```bash
pytest tests/
```

### Docker

#### Build test image

```bash
docker buildx build -t lseg-technical-challenge-tests --target tests .
```

#### Run tests
```bash
docker run --rm lseg-technical-challenge-tests
```