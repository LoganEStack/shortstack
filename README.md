<!-- INTRODUCTION -->
# Short Stack
A URL shortening service.


<!-- ABOUT -->
## About the Project
This app is a simple clone of TinyURL meant to further my understanding of full stack application development.
![Product Name Screen Shot][product-screenshot]

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
- Database: PostgreSQL (or SQLite for simplicity)
- Cache (optional): Redis for quick URL lookups
- Testing: pytest (backend), React Testing Library (frontend)
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


<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]: frontend/src/assets/product-screenshot.png




🐳 Containerize with Docker.

🧪 Add unit tests (backend first, then frontend).

🔁 Set up a dev + production config.

⚙️ Add CI/CD with GitHub Actions.