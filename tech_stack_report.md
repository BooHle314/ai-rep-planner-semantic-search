# Tech Stack Report - Route Planner Application

## 🏗️ Architecture
- **Pattern**: Microservices with Orchestrator
- **Containerization**: Docker + Docker Compose
- **Deployment**: Container-ready structure

## 💻 Backend Stack
$(python --version | awk '{print "- **Python**: " $2}')
$(pip list 2>/dev/null | grep -E "(streamlit|pandas|numpy|plotly)" | awk '{print "- **" $1 "**: " $2}')

## 🌐 Frontend Stack
- **Framework**: Streamlit (Python-based web app)
- **Charts**: Plotly interactive visualizations
- **Maps**: Likely Plotly/Mapbox or similar

## ��️ Data Layer
$(ls data/* 2>/dev/null | head -3 | awk '{print "- **Data files**: " $0}')
$(grep -r "import.*sql" . --include="*.py" 2>/dev/null | head -1 && echo "- **Database**: SQL-based" || echo "- **Database**: File-based (CSV/JSON)")

## 🔧 DevOps & Tools
$( [ -f "docker-compose.yml" ] && echo "- **Orchestration**: Docker Compose" )
$( [ -f "api/Dockerfile" ] && echo "- **Containerization**: Docker" )
$( [ -d ".git" ] && echo "- **Version Control**: Git" )

## 📈 ML/AI Components
$(grep -r "similarity\|embedding\|model" services/ --include="*.py" 2>/dev/null | head -1 && echo "- **AI**: Semantic search capabilities" || echo "- **AI**: Rule-based optimization")
