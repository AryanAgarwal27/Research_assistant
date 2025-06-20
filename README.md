# Multi-Agent Research Assistant

A sophisticated AI-powered research assistant built with LangGraph, FastAPI, and React that uses specialized agents for comprehensive research, fact-checking, and report generation.

![Multi-Agent Research Assistant](https://img.shields.io/badge/AI-Research%20Assistant-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-red)
![React](https://img.shields.io/badge/React-18-blue)

## 🚀 Features

- **Multi-Agent Architecture**: Specialized agents for query analysis, web research, fact-checking, synthesis, and report generation
- **Real-time Progress Tracking**: Live updates on research progress with detailed step-by-step visualization
- **Web Search Integration**: Powered by DuckDuckGo for comprehensive information gathering
- **AI-Powered Analysis**: Uses OpenAI GPT-4 for intelligent query analysis and report synthesis
- **Modern React Frontend**: Beautiful, responsive UI with real-time updates
- **RESTful API**: FastAPI backend with automatic documentation
- **Report Export**: Download comprehensive research reports as text files

## 🏗️ Architecture

### Multi-Agent Workflow

1. **Query Analyzer Agent**: Breaks down complex queries into actionable research tasks
2. **Web Research Agent**: Conducts comprehensive web searches using multiple strategies
3. **Fact Checker Agent**: Verifies information credibility and identifies potential misinformation
4. **Synthesizer Agent**: Combines findings into coherent insights and analysis
5. **Report Generator Agent**: Creates professional, structured research reports

### Tech Stack

- **Backend**: FastAPI, Python 3.8+
- **AI Framework**: LangChain, LangGraph
- **LLM**: OpenAI GPT-4
- **Search**: DuckDuckGo Search API
- **Frontend**: React 18, Tailwind CSS
- **Icons**: Lucide React

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Git

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Multi_research_agent
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set OpenAI API key**
   - Windows: `set OPENAI_API_KEY=your-api-key-here`
   - macOS/Linux: `export OPENAI_API_KEY=your-api-key-here`

6. **Run the application**
   - Windows: `run.bat`
   - macOS/Linux: `python server.py`

## 🌐 Usage

### Starting the Server

1. Run the batch script (Windows):
   ```cmd
   run.bat
   ```

2. Or start manually:
   ```bash
   python server.py
   ```

### Accessing the Application

- **Frontend UI**: http://localhost:8000/app
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Using the Research Assistant

1. **Enter your research query** in the text area
2. **Click "Start Research"** to begin the multi-agent workflow
3. **Monitor progress** with real-time updates showing each agent's work
4. **View the comprehensive report** once research is complete
5. **Download the report** as a text file for future reference

### Example Queries

- "What are the environmental impacts of cryptocurrency mining?"
- "Latest developments in gene therapy for cancer treatment"
- "Economic implications of remote work trends post-pandemic"
- "AI's impact on cybersecurity: threats and opportunities"
- "Sustainable agriculture practices and food security challenges"

## 🔧 API Reference

### Start Research Session

```http
POST /research
Content-Type: application/json

{
  "query": "Your research question here",
  "user_id": "optional-user-id"
}
```

### Check Research Progress

```http
GET /research/{session_id}
```

### Download Research Report

```http
GET /research/{session_id}/download
```

### Get System Statistics

```http
GET /stats
```

## 📁 Project Structure

```
Multi_research_agent/
├── server.py              # FastAPI server
├── graph.py               # Multi-agent workflow definition
├── frontend.jsx           # React frontend component
├── frontend.html          # HTML wrapper for React app
├── requirements.txt       # Python dependencies
├── run.bat               # Windows run script
├── setup.py              # Automated setup script
├── README.md             # This file
├── venv/                 # Virtual environment
└── __pycache__/          # Python cache files
```

## 🔍 Key Components

### Graph.py - Multi-Agent Workflow

- **StateGraph**: Manages the research workflow state
- **Agent Classes**: Specialized agents for different research tasks
- **Node Functions**: Connect agents to the workflow graph
- **Research Pipeline**: Orchestrates the entire research process

### Server.py - FastAPI Backend

- **Session Management**: Tracks research sessions and progress
- **Background Tasks**: Runs research workflows asynchronously
- **File Serving**: Serves frontend and static files
- **API Endpoints**: RESTful API for frontend communication

### Frontend.jsx - React Interface

- **Progress Visualization**: Real-time research progress tracking
- **Interactive UI**: Modern, responsive design with Tailwind CSS
- **Session Management**: Handles research sessions and results
- **Report Display**: Formatted report viewing and downloading

## 🛠️ Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Customization

- **Model Configuration**: Modify LLM settings in `graph.py`
- **UI Styling**: Customize Tailwind classes in `frontend.jsx`
- **Search Parameters**: Adjust search strategies in agent classes
- **Report Format**: Customize report templates in the ReportGenerator agent

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure virtual environment is activated
2. **OpenAI API Error**: Verify your API key is set correctly
3. **Port Already in Use**: Change the port in `server.py` if needed
4. **Search Timeouts**: Check internet connection for DuckDuckGo access

### Debug Mode

Run with debug output:
```bash
python server.py --log-level debug
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- LangChain team for the AI framework
- DuckDuckGo for search capabilities
- FastAPI and React communities

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ using LangGraph, FastAPI, and React**
