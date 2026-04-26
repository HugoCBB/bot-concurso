run:
	fastapi dev app/main.py

run-scraping:
	PYTHONPATH=./app python3 ./app/modules/workers/run_job.py