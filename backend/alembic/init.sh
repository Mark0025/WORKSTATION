#!/bin/bash

# Initialize alembic
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration" 