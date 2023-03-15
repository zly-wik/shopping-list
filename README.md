# Shopping list - Django project

## Overview:

Web app that helps users create private 
shopping lists. Project is well-tested and has 
**96% tests coverage**. Backend is written with 
**Django** and DRF for REST API. Everything is 
configured as single docker-compose. 

## Technical overview:

-   REST API (`DRF`)
-   Authentication (`Djoser`, JWT tokens)
-   Unit tests (`Pytest`)
-   Media files
-   Sending emails (`smtp4dev`)
-   Containerization (`Docker` and `docker-compose`)
-   Database (`PostgreSQL`)

## Project Setup:

-   As this project is containerized, simply build and run project inside `docker-compose`
-   There's also option to run it with pipenv or by installing `requirements.txt` and/or `requirements.dev` file(s), but it require additional PosgreSQL config or usage of SQLite3 database

![Tests](https://github.com/zly-wik/shopping-list/actions/workflows/tests.yml/badge.svg)
