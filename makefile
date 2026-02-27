# ==============================
# Django Project Makefile
# ==============================

VENV = .venv
PYTHON = python3
PIP = $(VENV)/bin/pip
MANAGE = $(VENV)/bin/python manage.py

# Default target
help:
	@echo "Available commands:"
	@echo "make venv        - Create virtual environment"
	@echo "make install     - Install requirements"
	@echo "make run         - Run development server"
	@echo "make makemigrations - Create migrations"
	@echo "make migrate     - Apply migrations"
	@echo "make superuser   - Create superuser"
	@echo "make collectstatic - Collect static files"
	@echo "make freeze      - Update requirements.txt"
	@echo "make clean       - Remove virtual environment"

# Create virtual environment
venv:
	$(PYTHON) -m venv $(VENV)
	@echo "Virtual environment created."

# Install dependencies
install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Dependencies installed."

# Run development server
run:
	$(MANAGE) runserver

# Create migrations
makemigrations:
	$(MANAGE) makemigrations

# Apply migrations
migrate:
	$(MANAGE) migrate

# Create superuser
superuser:
	$(MANAGE) createsuperuser

# Collect static files
collectstatic:
	$(MANAGE) collectstatic --noinput

# Freeze dependencies
freeze:
	$(PIP) freeze > requirements.txt
	@echo "requirements.txt updated."

# Remove virtual environment
clean:
	deactivate || true
	rm -rf $(VENV)
	@echo "Virtual environment removed."