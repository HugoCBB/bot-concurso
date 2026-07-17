.PHONY: run run-scraping up down build logs logs-worker migrate refresh scrape psql

run:
	docker compose up -d

run-scraping:  
	cd app && python -m modules.workers.run_job

up:              
	docker compose up -d --build

down:            
	docker compose down

build:           
	docker compose build

logs:            
	docker compose logs -f

logs-worker:    
	docker compose logs -f worker

migrate:         
	docker compose run --rm migrate

refresh:       
	curl -X POST http://localhost:8000/api/contests/refresh

scrape:          
	docker compose run --rm worker python -m modules.workers.run_job

psql:            
	docker compose exec postgres psql -U postgres -d concursos
