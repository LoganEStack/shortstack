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
Method   |   Endpoint               |	Description
---------|--------------------------|------------------------------
POST     |	/shorten                |	Accepts a long URL, returns short URL
GET      |	/<short_id>             |	Redirects to original URL
GET      |	/admin/db/stats         |	Returns usage stats
GET      |	/admin/db/urls          |	Returns all urls in db
GET      |	/admin/db/<short_code>  |	Returns data for specific short code
GET      |	/admin/db?query         |	Returns urls matching a query
DELETE   |	/admin/db/<short_code>  |	Deletes a specific short code
DELETE   |	/admin/db/<int:count>   |	Deletes X least recent short codes

### Database Schema
Table: urls

Column	         |   Type	         |   Description
------------------|-----------------|----------------------------------
id	               |   UUID / INT    |   Primary key
original_url	   |   STRING        |   Full destination URL
short_code	      |   STRING        |   Unique shortened version (not full URL)
expiration_date	|   TIMESTAMP     |   When the short URL will expire
created_at	      |   TIMESTAMP     |   When the short URL was created


### Back of Envelope Calculations
Each row is roughly ~ 160 bytes. 

The purpose of this project is primarily education. As such, I'm limiting the database storage size to 200 MB, where old entries expire after 7 days, allowing for new entries to come in.

This results in a maximum of roughly 1.2 million possible entries.


<!-- STRUCTURE -->
## Project Structure
backend/
├── app/
│   ├── __init__.py
│   ├── routes.py             # handles base routing
│   ├── routes_db.py          # handles database routing
│   ├── models.py             # database table schemas
│   ├── utils.py              # utility functions
│   ├── short_code_gen.py     # short code generation function
│   └── limiter.py            # rate limiting
├── scripts/
│   └── cleanup.py            # deletes expired short codes
├── tests/
│   └── test_routes.py        # pytest functions
├── config.py                 # contains environment variables
├── conftest.py               # for path registering
├── Dockerfile
└── requirements.txt

frontend/
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   ├── pages/
│   ├── App.jsx
│   └── main.jsx
├── Dockerfile
├── package.json
└── vite.config.js

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
Must have the following installed:
- Python
- Node.js

### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/LoganEStack/shortstack.git
   ```
2. Create a virtual environment in the backend
   ```sh
   cd backend
   python -m venv .venv
   ```
3. Activate the virtual environment
   ```sh
   backend/.venv/Scripts/Activate.ps1
   ```
4. Install backend requirements
   ```sh
   pip install requirements.txt
   ```
5. Run the backend
   ```sh
   npm install
   ```
6. Navigate to frontend
   ```sh
   cd ../frontend
   ```
7. Install npm packages
   ```sh
   npm install
   ```
8. Run the frontend
   ```sh
   npm run dev
   ```

### Environment
.env file
FLASK_ENV=development
DATABASE_URL=postgresql://*user*:*pass*@localhost:*port*/*db_name*
API_KEY=*key*


<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]: frontend/src/assets/product-screenshot.png


TODO:
- Resolve limiter storage warning
- Containerize with Docker.   Is it better to containerize with Docker before hosting my project?
- Add CI/CD with GitHub Actions.
