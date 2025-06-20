# Multi-Agent Research Assistant

A sophisticated research assistant powered by LangGraph and FastAPI that performs comprehensive research on any topic using multiple specialized agents.

## Features

- Query analysis and task breakdown
- Web research with multiple sources
- Fact-checking and source credibility assessment
- Research synthesis and report generation
- Real-time progress tracking
- Beautiful React-based UI

## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/research-agent.git
cd research-agent
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```
OPENAI_API_KEY=your-api-key-here
```

4. Run the development server:
```bash
uvicorn server:app --reload
```

5. Open http://localhost:8000/app in your browser

## Deployment

This application can be deployed on Render.com:

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the following:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
4. Add your `OPENAI_API_KEY` in the environment variables section
5. Deploy!

## API Documentation

Once deployed, you can access:
- Frontend: `https://your-app.onrender.com/app`
- API docs: `https://your-app.onrender.com/docs`
- OpenAPI spec: `https://your-app.onrender.com/openapi.json`

## Architecture

The application uses a multi-agent system built with LangGraph:
- QueryAnalyzerAgent: Breaks down research queries into specific tasks
- WebResearchAgent: Conducts web searches and gathers information
- FactCheckerAgent: Verifies information and assesses source credibility
- SynthesizerAgent: Combines findings into coherent insights
- ReportGeneratorAgent: Creates the final research report

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
