run: ## Run the application
	## poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --env-file .env
	poetry run gunicorn app.main:app -c app/core/gunicorn.conf.py

docker: ## Start container
	docker start weather_container

container: ## Run docker
	docker run -d -p 8000:8000 --name weather_container weather

image: ## Create image
	docker build -t weather .

migrate-create: ## Create migration
	alembic revision --autogenerate -m $(NAME)