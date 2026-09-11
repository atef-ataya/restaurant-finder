# 🍽️ Restaurant Finder

AI-powered restaurant discovery 
## Quick Start

1. Clone and setup:
```bash
git clone [your-repo-url]
cd restaurant-finder

Backend:

bashcd backend
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
uvicorn src.restaurant_finder.main:app --reload

Frontend:

bashcd frontend
npm install
npm run dev

Test CrewAI:

bashcd backend
crewai run

CodeRabbit review:

bashcoderabbit review --plain
