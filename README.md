An AI-powered, microservices-based application for optimizing sales representative routes using semantic search, intelligent geocoding, and time-constrained route planning.

This project was completed as an interview task, with a strong focus on architecture, agentic data pipelines, and clean system design.

Overview
This system enables sales teams to:
- Search customers and reps using natural language
- Convert dirty addresses into geospatial coordinates
- Select customers based on semantic intent
- Generate optimal daily routes within an 8-hour workday
- Visualize routes and statistics on an interactive map

Goal

Build a microservices-based solution that:
- Ingests and enriches raw sales data
- Enables semantic intent-based customer filtering
- Plans efficient routes between specified start and end locations
- Demonstrates robust architecture and agentic pipelines

Provided Content
The system operates on synthetic data containing:
- ~12 sales representatives
- ~2,000 customer locations
- Customer → rep assignments
- Dirty, semi-structured addresses
- Customer notes with natural language context

Core Functional Requirements

A) Robust Data Pipeline (Ingestion & Geocoding)
- Parses and standardizes noisy address data
- Geocodes addresses using an external API
- Implements fallback logic for failed geocoding
- Uses local caching to avoid repeated API calls
- Tracks unprocessable records without failing the pipeline

B) "Small Transformer" Semantic Search (Embeddings)
Example:
> "Find angry customers who need urgent attention"
> 
> Ranks customers whose notes contain semantically similar urgency signals.

C) Route Planning (The Optimizer)
For a selected rep and filtered customers:
- 8-hour time budget
- 30 minutes service time per customer
- Fixed travel speed of 100 km/h
- Supports custom start and end locations
- Optimizes for maximum number of high-relevance customers

D) Frontend & Visualization
- Minimal Streamlit UI
- Semantic query inputs (rep + customer intent)
- Interactive OpenStreetMap visualization
- Route statistics:
  - Travel time
  - Service time
  - Total duration

Architecture

The system is intentionally designed with clear separation of concerns, emphasizing agentic data pipelines.

Key Architectural Principles
- Decoupled Frontend/UI and Backend Logic
- Modular services (search, geocoding, routing)
- Clear responsibility boundaries
- Pipeline-style data flow:

Ingestion → Geocoding → Embeddings → Filtering → Optimization → Visualization

Tech Stack:

Backend
- Python 3.x
- Pandas, NumPy
- Local embedding models
- Semantic similarity (cosine-based)

Frontend
- Streamlit
- Plotly for interactive maps and charts
- OpenStreetMap basemap

Infrastructure
- Docker
- Docker Compose
- Virtual environment (venv)

Data Layer
- CSV / Excel files
- File-based caching for embeddings and geocoding

Docker Setup Verification
1.Dockerfiles exist:**
   - `api/Dockerfile` 
   - `ui/Dockerfile` 

2.Compose parses correctly:**
   ```bash
   docker compose config

How to Run the Application:
How to run
1. Ensure Docker and Docker Compose are installed.
2. Clone this repo.
3. Navigate to the project root.
4. Run: `docker compose up --build`

Local Development
```bash
cd /workspaces/Route-planner
source venv/bin/activate
streamlit run app_complete.py


Known Limitations:

Docker / Deployment Limitations
- Full containerized deployment using `docker compose up --build` could not be tested due to storage limitations
- The application has not been verified to run end-to-end in a containerized environment
- While Dockerfiles and the Compose setup are included, production readiness and deployment reliability remain untested

Error Handling
- The project currently lacks comprehensive error handling
- If a data file is missing, corrupted, or improperly formatted, the scripts may fail without providing clear or graceful error messages

Data and Semantic Search
- The Small Transformer-based semantic search currently does not utilize all ~2,000 customer locations
- Representative name matching (e.g., "Jon S" → "Jonathan Smith") may be incomplete or imperfect

General Limitations
- Automated testing has not been implemented
- Multi-user support and persistent database integration are not included
- The repository includes some large local data files, which may impact portability or cloning