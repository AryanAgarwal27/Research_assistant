import os
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
import uuid
import json
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import the research assistant from graph.py
from graph import run_research_assistant

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Multi-Agent Research Assistant API", version="1.0.0")

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class ResearchRequest(BaseModel):
    query: str
    user_id: str = "anonymous"

class ResearchSessionResponse(BaseModel):
    session_id: str
    query: str
    status: str
    
class ResearchProgress(BaseModel):
    step: str
    percentage: int
    message: Optional[str] = None

class ResearchResult(BaseModel):
    session_id: str
    query: str
    report: str
    status: str
    progress: ResearchProgress
    metadata: Dict[str, Any]
    timestamp: str

# In-memory storage for sessions (in production, use a database)
research_sessions: Dict[str, Dict[str, Any]] = {}
research_history = []

@app.get("/")
async def root():
    """Root endpoint - serves the frontend"""
    return {"message": "Multi-Agent Research Assistant API", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

async def run_research_in_background(session_id: str, query: str):
    """Run the research workflow in the background with progress updates"""
    session = research_sessions[session_id]
    
    try:
        # Update progress through the workflow
        steps = [
            ("analyzing_query", 20, "Analyzing your research query..."),
            ("conducting_research", 40, "Searching for relevant information..."),
            ("fact_checking", 60, "Verifying facts and sources..."),
            ("synthesizing", 80, "Synthesizing findings..."),
            ("generating_report", 100, "Generating final report...")
        ]
        
        for step, percentage, message in steps:
            session["progress"] = {
                "step": step,
                "percentage": percentage,
                "message": message
            }
            session["status"] = "in_progress"
            await asyncio.sleep(1)  # Simulate progress delay
        
        # Run the actual research
        print(f"🔍 Starting research for query: {query}")
        result = await run_research_assistant(query)
        
        # Update session with results
        session.update({
            "status": "completed",
            "report": result["report"],
            "metadata": result["metadata"],
            "progress": {
                "step": "completed",
                "percentage": 100,
                "message": "Research completed successfully!"
            },
            "completion_time": datetime.now().isoformat()
        })
        
        print(f"✅ Research completed successfully for: {query}")
        
    except Exception as e:
        print(f"❌ Research failed: {str(e)}")
        session.update({
            "status": "failed",
            "error": str(e),
            "progress": {
                "step": "error",
                "percentage": 0,
                "message": f"Research failed: {str(e)}"
            },
            "completion_time": datetime.now().isoformat()
        })

@app.post("/research", response_model=ResearchSessionResponse)
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    """
    Start a research session using the multi-agent workflow
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # Create new session
    session_id = str(uuid.uuid4())
    session = {
        "session_id": session_id,
        "query": request.query.strip(),
        "user_id": request.user_id,
        "status": "initializing",
        "progress": {
            "step": "initializing",
            "percentage": 0,
            "message": "Initializing research workflow..."
        },
        "start_time": datetime.now().isoformat(),
        "report": None,
        "metadata": {},
        "error": None
    }
    
    research_sessions[session_id] = session
    
    # Start research in background
    background_tasks.add_task(run_research_in_background, session_id, request.query.strip())
    
    return ResearchSessionResponse(
        session_id=session_id,
        query=request.query.strip(),
        status="initializing"
    )

@app.get("/research/{session_id}")
async def get_research_status(session_id: str):
    """
    Get the status and progress of a research session
    """
    if session_id not in research_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = research_sessions[session_id]
    
    if session["status"] == "completed":
        return ResearchResult(
            session_id=session_id,
            query=session["query"],
            report=session["report"],
            status=session["status"],
            progress=ResearchProgress(**session["progress"]),
            metadata=session["metadata"],
            timestamp=session["completion_time"]
        )
    elif session["status"] == "failed":
        return {
            "session_id": session_id,
            "status": session["status"],
            "error": session.get("error", "Unknown error"),
            "progress": session["progress"]
        }
    else:
        return {
            "session_id": session_id,
            "status": session["status"],
            "progress": session["progress"]
        }

@app.get("/research/{session_id}/download")
async def download_report(session_id: str):
    """
    Download the research report as a text file
    """
    if session_id not in research_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = research_sessions[session_id]
    
    if session["status"] != "completed":
        raise HTTPException(status_code=400, detail="Research not completed yet")
    
    report_content = f"""
Multi-Agent Research Report
===========================

Query: {session['query']}
Generated: {session['completion_time']}
Sources Consulted: {session['metadata'].get('sources_consulted', 'N/A')}

Report:
-------
{session['report']}
"""
    
    return PlainTextResponse(
        content=report_content,
        headers={
            "Content-Disposition": f"attachment; filename=research_report_{session_id[:8]}.txt"
        }
    )

@app.get("/history")
async def get_research_history():
    """Get research history"""
    return {
        "history": research_history[-10:],  # Return last 10 entries
        "total_requests": len(research_history)
    }

@app.delete("/history")
async def clear_history():
    """Clear research history"""
    global research_history
    research_history = []
    return {"message": "History cleared successfully"}

@app.get("/stats")
async def get_stats():
    """Get API statistics"""
    total_sessions = len(research_sessions)
    completed = sum(1 for session in research_sessions.values() if session["status"] == "completed")
    failed = sum(1 for session in research_sessions.values() if session["status"] == "failed")
    in_progress = sum(1 for session in research_sessions.values() if session["status"] in ["initializing", "in_progress"])
    
    success_rate = f"{(completed / total_sessions * 100):.1f}%" if total_sessions > 0 else "0.0%"
    
    return {
        "total_sessions": total_sessions,
        "completed": completed,
        "failed": failed,
        "in_progress": in_progress,
        "success_rate": success_rate
    }

# Serve static files (frontend)
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass  # static directory might not exist

@app.get("/app", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the frontend HTML"""
    try:
        with open("frontend.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Frontend not found</h1><p>Please create frontend.html</p>",
            status_code=404
        )

@app.get("/frontend.jsx", response_class=PlainTextResponse)
async def serve_jsx():
    """Serve the React JSX file"""
    try:
        with open("frontend.jsx", "r", encoding="utf-8") as f:
            return PlainTextResponse(content=f.read(), media_type="text/babel")
    except FileNotFoundError:
        return PlainTextResponse(content="// Frontend JSX not found", status_code=404)

if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ Error: OPENAI_API_KEY environment variable not found!")
        print("Please create a .env file in the project root with your OpenAI API key:")
        print("\nOPENAI_API_KEY=your-api-key-here\n")
        exit(1)
    
    print("\n🚀 Starting Multi-Agent Research Assistant Server")
    print("=" * 60)
    print("📡 API will be available at: http://localhost:8000")
    print("🌐 Frontend will be available at: http://localhost:8000/app")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000) 