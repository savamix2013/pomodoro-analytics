# -------------------------------
# DEFAULT GOAL
# -------------------------------
.DEFAULT_GOAL := help

# -------------------------------
# Run the application locally using uvicorn (development)
# -------------------------------
run:
	@echo "Running the application locally..."
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
	poetry run uvicorn app.main:app --reload
	$env:DB_HOST="127.0.0.1"; poetry run alembic upgrade head
# -------------------------------
# Run the application in Docker
# -------------------------------
docker-up:
	@echo "Starting Docker containers..."
	docker-compose up --build

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

# -------------------------------
# Install a dependency using poetry
# -------------------------------
install:
	@echo "Installing dependency $(LIBRARY)..."
	poetry add $(LIBRARY)

# -------------------------------
# Uninstall a dependency using poetry
# -------------------------------
uninstall:
	@echo "Uninstalling dependency $(LIBRARY)..."
	poetry remove $(LIBRARY)

migrate-create:
	@echo "Creating a new migration..."
	alembic revision --autogenerate -m "Added account table"
	alembic upgrade head

# -------------------------------
# Help command
# -------------------------------
help:
	@echo "Usage: make [command]"
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:' $(MAKEFILE_LIST) | awk 'BEGIN {FS=":"} {printf "  %-15s %s\n", $$1, $$2}'