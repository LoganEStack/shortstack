<!-- INTRODUCTION -->
# Short Stack
A URL shortening service.

![Product Name Screen Shot][product-screenshot]


<!-- ABOUT -->
## About the Project
This app is a simple clone of TinyURL meant to further my understanding of full stack application development.

<!-- SYSTEM DESIGN -->
## System Design

### Project Requirements
Functional Requirements:
- Accept a URL and return a shortened alias, known as a short link.
- When users access a short link, our service should redirect them to the original link.
- Users should optionally be able to pick a custom short link for their URL.
- Links will expire after a standard default timespan. Users should be able to specify the expiration time.

Non-Functional Requirements:
- High availability and fast response time.
- Security: input validation, avoid open redirects, non-predictable short links

### Tech Stack
- Frontend: React
- Backend: Flask (Python)
- Database: PostgreSQL
- Containerization: Docker
- CI/CD: GitHub Actions

### API Design
Method  |   Endpoint            |	Description
--------|-----------------------|------------------------------
POST    |	/api/shorten        |	Accepts a long URL, returns short URL
GET     |	/<short_id>         |	Redirects to original URL
GET     |	/api/analytics/<id> |	(Optional) Returns usage stats

### Database Schema
Table: urls

Column	   |   Type	         |   Description
------------|-----------------|----------------------------------
id	         |   UUID / INT    |   Primary key
short_id	   |   STRING        |   Unique shortened version
long_url	   |   TEXT          |   Full destination URL
created_at	|   TIMESTAMP     |   When the short URL was created
clicks	   |   INTEGER       |   Number of times accessed


### Data
Limits to 200 MB at one time. Each entry is roughly ~ 160 bytes per row resulting in about 1.2 million entries.


<!-- STRUCTURE -->
## Project Structure
backend/
├── app/
│   ├── __init__.py
│   ├── routes.py : handles all routing
│   ├── models.py
│   └── utils.py
├── tests/
├── Dockerfile
└── requirements.txt

frontend/
├── public/
├── src/
│   ├── components/
│   ├── pages/
│   ├── App.jsx
│   └── index.jsx
├── Dockerfile
└── package.json


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/LoganEStack/shortstack.git
   ```

### Environment
.env file
FLASK_ENV=development
DATABASE_URL=postgresql://*user*:*pass*@localhost:*port*/*db_name*
API_KEY=*key*

<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]: frontend/src/assets/product-screenshot.png


- Implement Pytest fixtures
- Resolve limiter storage warning

- Containerize with Docker.   Is it better to containerize with Docker before hosting my project?
- Add CI/CD with GitHub Actions.
