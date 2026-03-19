# Quick Notes

A full-stack note-taking application built with FastAPI (backend), React (frontend), and PostgreSQL (database). Create, read, update, and delete notes with a beautiful and intuitive user interface.

## Features

- **Full CRUD Operations**: Create, read, update, and delete notes
- **Modern UI**: Beautiful gradient design with smooth animations
- **Real-time Updates**: Changes are immediately reflected in the interface
- **Timestamps**: Track when notes are created and updated
- **RESTful API**: Well-structured backend API with FastAPI
- **Dockerized**: Easy deployment with Docker Compose
- **Tested**: Comprehensive test coverage for both backend and frontend

## Tech Stack

### Backend
- **FastAPI**: Modern, fast Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Robust relational database
- **Pydantic**: Data validation using Python type annotations
- **Pytest**: Testing framework

### Frontend
- **React**: JavaScript library for building user interfaces
- **Create React App**: Toolchain for React applications
- **CSS3**: Modern styling with gradients and animations

### DevOps
- **Docker**: Containerization platform
- **Docker Compose**: Multi-container orchestration
- **Jenkins**: CI/CD pipeline (optional)

## Prerequisites

- Docker and Docker Compose installed
- Node.js 14+ (for local frontend development)
- Python 3.11+ (for local backend development)

## Quick Start

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/Zakaria-Raddaoui/quicknotes.git
cd quicknotes
```

2. Start all services:
```bash
docker compose up -d --build
```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env  # Create .env file
# Edit .env with your database credentials
```

5. Run the backend:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

6. Run tests:
```bash
pytest
```

#### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Run tests:
```bash
npm test
```

## API Endpoints

### Notes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notes` | Get all notes |
| GET | `/notes/{id}` | Get a single note by ID |
| POST | `/notes` | Create a new note |
| PUT | `/notes/{id}` | Update an existing note |
| DELETE | `/notes/{id}` | Delete a note |

### Example Request/Response

**Create a Note (POST /notes)**
```json
Request:
{
  "title": "My First Note",
  "content": "This is the content of my note"
}

Response:
{
  "id": 1,
  "title": "My First Note",
  "content": "This is the content of my note",
  "created_at": "2024-03-19T10:30:00Z",
  "updated_at": null
}
```

**Update a Note (PUT /notes/1)**
```json
Request:
{
  "title": "Updated Title",
  "content": "Updated content"
}

Response:
{
  "id": 1,
  "title": "Updated Title",
  "content": "Updated content",
  "created_at": "2024-03-19T10:30:00Z",
  "updated_at": "2024-03-19T11:00:00Z"
}
```

## Project Structure

```
quicknotes/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # Database operations
│   ├── database.py          # Database configuration
│   ├── requirements.txt     # Python dependencies
│   ├── test_main.py         # Backend tests
│   ├── pytest.ini           # Pytest configuration
│   ├── Dockerfile           # Backend Docker image
│   └── .env                 # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── App.css          # Styles
│   │   └── App.test.js      # Frontend tests
│   ├── package.json         # Node dependencies
│   └── Dockerfile           # Frontend Docker image
├── docker-compose.yml       # Docker services configuration
├── Jenkinsfile              # CI/CD pipeline
└── README.md                # This file
```

## Database Schema

### Notes Table

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT |
| title | VARCHAR(100) | NOT NULL |
| content | TEXT | NOT NULL |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | ON UPDATE NOW() |

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@host:port/database
```

### Docker Compose
The `docker-compose.yml` file includes default PostgreSQL credentials:
- **POSTGRES_USER**: postgres
- **POSTGRES_PASSWORD**: postgres
- **POSTGRES_DB**: quicknotes

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## CI/CD

The project includes a Jenkins pipeline (`Jenkinsfile`) with the following stages:
1. **Checkout**: Clone the repository
2. **Build**: Build Docker images
3. **Test**: Run backend tests
4. **Deploy**: Deploy containers

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env file
- Verify network connectivity between containers

### Frontend Can't Connect to Backend
- Ensure backend is running on port 8000
- Check CORS settings in backend/main.py
- Verify API_URL in frontend/src/App.js

### Port Already in Use
```bash
# Stop all running containers
docker compose down

# Check for processes using ports
lsof -i :3000  # Frontend
lsof -i :8000  # Backend
lsof -i :5433  # PostgreSQL
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please open an issue on GitHub.
