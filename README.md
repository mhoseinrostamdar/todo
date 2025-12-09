# 📝 ToDoList -- Project & Task Management API

### Developed in Three Phases (Phase 1 → Phase 3)

The **ToDoList** project is a complete backend application built
step-by-step through three development phases.\
It evolves from simple object-oriented classes, to a multi-layer
architecture, and finally into a fully functional **RESTful Web API**
using **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

## 📌 Table of Contents

-   Overview
-   Development Phases
-   Features
-   Project Structure
-   Environment Variables
-   Setup & Installation
-   Running Database Migrations
-   API Documentation
-   Sample API Requests
-   Tech Stack
-   Future Improvements
-   License

## Overview

ToDoList is a backend system that manages **Projects** and **Tasks**,
supporting CRUD operations, validation, database storage, and modern API
documentation.

## Development Phases

### Phase 1 --- Object Models

Basic object-oriented classes: - Project - Task

### Phase 2 --- Repository and Service Layers

Introduces multi-layer architecture: - Repository layer (data access) -
Service layer (business logic)

### Phase 3 --- Full REST API

Implements: - FastAPI routers/controllers - SQLAlchemy ORM -
PostgreSQL - Alembic migrations - OpenAPI documentation

## Features

-   Full CRUD for projects & tasks
-   Validation & constraints
-   Layered architecture
-   Async database operations
-   Auto-generated API docs
-   Alembic migrations

## Project Structure

    app/
    ├── api/
    ├── core/
    ├── services/
    ├── repositories/
    ├── models.py
    ├── db.py
    main.py
    alembic/

## Environment Variables

    DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/todo_db
    MAX_NUMBER_OF_PROJECT=10
    MAX_NUMBER_OF_TASK=50
    TITLE_MAX=100
    DESC_MAX=500
    STATUS_VALUES=todo,in_progress,done

## Setup & Installation

    git clone <repo>
    pip install -r requirements.txt
    alembic upgrade head
    uvicorn main:app --reload

## API Documentation

-   `/api/v1/docs`
-   `/api/v1/redoc`

## Sample API Requests

### Create Project

    POST /api/v1/projects
    {
      "title": "My Project",
      "description": "Description"
    }

## Tech Stack

-   Python\
-   FastAPI\
-   SQLAlchemy\
-   PostgreSQL\
-   Alembic


