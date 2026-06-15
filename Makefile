# -------------------------------
# DEFAULT GOAL
# -------------------------------
.DEFAULT_GOAL := help

# -------------------------------
# Run the application using uvicorn
# -------------------------------
run:
	@echo "Running the application..."
	poetry run uvicorn main:app --host 0.0.0.0 --port 8008 --reload --env-file $(ENV_FILE)

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

# -------------------------------
# Help command
# -------------------------------
help:
	@echo "Usage: make [command]"
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:' $(MAKEFILE_LIST) | awk 'BEGIN {FS=":"} {printf "  %-15s %s\n", $$1, $$2}'