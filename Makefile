# Run application locally

dev-run: ## Run the application with uvicorn
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --env-file .env --log-level debug

run: ## Run the application
	poetry run gunicorn app.main:app -c app/core/gunicorn.conf.py

# OR run it by Docker

image: ## Create image
	docker build -t weather_image .

container: ## Run docker
	docker run -d -p 8000:8000 --name weather_container weather_image

docker: ## Start container
	docker start weather_container
