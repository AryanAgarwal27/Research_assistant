import os
import asyncio
from typing import List, Dict, Any, TypedDict, Annotated
from datetime import datetime
import json
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
import operator

# Load environment variables from .env file
load_dotenv()

# State definition for the research workflow
class ResearchState(TypedDict):
    query: str
    research_tasks: List[Dict[str, Any]]
    search_results: List[Dict[str, Any]]
    fact_check_results: List[Dict[str, Any]]
    synthesized_findings: str
    final_report: str
    messages: Annotated[List, operator.add]
    current_step: str
    metadata: Dict[str, Any]

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0.1,
    max_tokens=2000
)

# Tools setup
search_tool = DuckDuckGoSearchRun()

@tool
def web_search(query: str) -> str:
    """Search the web for information on a given query."""
    try:
        results = search_tool.run(query)
        return results
    except Exception as e:
        return f"Search failed: {str(e)}"

@tool
def fact_check_search(claim: str) -> str:
    """Search for fact-checking information about a specific claim."""
    fact_check_query = f"fact check verify {claim}"
    try:
        results = search_tool.run(fact_check_query)
        return results
    except Exception as e:
        return f"Fact check search failed: {str(e)}"

# Agent implementations
class QueryAnalyzerAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Query Analyzer Agent. Your job is to break down complex research queries into specific, actionable research tasks.

For each query, identify:
1. Main research objectives
2. Sub-topics that need investigation
3. Specific questions to answer
4. Priority levels for each task

Return your analysis as a JSON structure with research_tasks array."""),
            ("human", "Query to analyze: {query}")
        ])
    
    async def analyze_query(self, state: ResearchState) -> Dict[str, Any]:
        chain = self.prompt | self.llm
        response = await chain.ainvoke({"query": state["query"]})
        
        # Parse the response to extract research tasks
        try:
            # Extract JSON from the response
            content = response.content
            tasks_data = None
            
            # Try to find JSON in code blocks
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
                try:
                    tasks_data = json.loads(json_str)
                except:
                    pass
            
            # Try to find JSON without code blocks
            if not tasks_data:
                try:
                    tasks_data = json.loads(content)
                except:
                    pass
            
            # If no valid JSON found, create default task structure
            if not tasks_data or "research_tasks" not in tasks_data:
                tasks_data = {
                    "research_tasks": [
                        {
                            "id": 1,
                            "task": f"Research main aspects of: {state['query']}",
                            "priority": "high",
                            "search_queries": [state["query"]]
                        }
                    ]
                }
            
            # Validate task structure
            for task in tasks_data["research_tasks"]:
                if "id" not in task:
                    task["id"] = tasks_data["research_tasks"].index(task) + 1
                if "priority" not in task:
                    task["priority"] = "high"
                if "search_queries" not in task:
                    task["search_queries"] = [task.get("task", state["query"])]
                if "task" not in task:
                    task["task"] = state["query"]
            
        except Exception as e:
            print(f"Error parsing tasks: {str(e)}")
            # Fallback to basic task structure
            tasks_data = {
                "research_tasks": [
                    {
                        "id": 1,
                        "task": f"Research: {state['query']}",
                        "priority": "high",
                        "search_queries": [state["query"]]
                    }
                ]
            }
        
        return {
            "research_tasks": tasks_data["research_tasks"],
            "messages": [AIMessage(content=f"Query analyzed. Identified {len(tasks_data['research_tasks'])} research tasks.")],
            "current_step": "query_analysis_complete"
        }

class WebResearchAgent:
    def __init__(self, llm):
        self.llm = llm
        self.search_tool = web_search
    
    async def conduct_research(self, state: ResearchState) -> Dict[str, Any]:
        search_results = []
        
        try:
            for task in state["research_tasks"]:
                # Ensure task has required fields
                task_id = task.get("id", len(search_results) + 1)
                search_queries = task.get("search_queries", [task.get("task", state["query"])])
                
                for query in search_queries:
                    try:
                        result = self.search_tool.invoke(query)
                        search_results.append({
                            "task_id": task_id,
                            "query": query,
                            "results": result,
                            "timestamp": datetime.now().isoformat()
                        })
                    except Exception as e:
                        print(f"Search error for query '{query}': {str(e)}")
                        search_results.append({
                            "task_id": task_id,
                            "query": query,
                            "results": f"Search error: {str(e)}",
                            "timestamp": datetime.now().isoformat()
                        })
            
            if not search_results:
                # Fallback: try direct search with original query
                try:
                    result = self.search_tool.invoke(state["query"])
                    search_results.append({
                        "task_id": 1,
                        "query": state["query"],
                        "results": result,
                        "timestamp": datetime.now().isoformat()
                    })
                except Exception as e:
                    print(f"Fallback search error: {str(e)}")
                    search_results.append({
                        "task_id": 1,
                        "query": state["query"],
                        "results": f"Search error: {str(e)}",
                        "timestamp": datetime.now().isoformat()
                    })
        
        except Exception as e:
            print(f"Research error: {str(e)}")
            # Ensure we have at least one result
            if not search_results:
                search_results.append({
                    "task_id": 1,
                    "query": state["query"],
                    "results": f"Research error: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                })
        
        return {
            "search_results": search_results,
            "messages": [AIMessage(content=f"Completed web research. Gathered {len(search_results)} search results.")],
            "current_step": "research_complete"
        }

class FactCheckerAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Fact Checker Agent. Analyze search results and identify claims that need verification.

Your tasks:
1. Extract key factual claims from search results
2. Assess credibility of sources
3. Identify potential misinformation
4. Rate confidence levels for claims
5. Flag conflicting information

Provide structured analysis with credibility scores (1-10) and reasoning."""),
            ("human", "Search results to fact-check: {search_results}")
        ])
    
    async def fact_check(self, state: ResearchState) -> Dict[str, Any]:
        # Combine search results for analysis
        combined_results = "\n\n".join([
            f"Query: {result['query']}\nResults: {result['results']}"
            for result in state["search_results"]
        ])
        
        chain = self.prompt | self.llm
        response = await chain.ainvoke({"search_results": combined_results})
        
        # Additional fact-checking searches for suspicious claims
        fact_check_results = []
        
        # Simple implementation - extract potential claims and verify
        # In production, you'd use more sophisticated claim extraction
        try:
            additional_search = fact_check_search.invoke(state["query"])
            fact_check_results.append({
                "type": "additional_verification",
                "query": state["query"],
                "results": additional_search,
                "analysis": response.content
            })
        except Exception as e:
            fact_check_results.append({
                "type": "verification_error",
                "error": str(e),
                "analysis": response.content
            })
        
        return {
            "fact_check_results": fact_check_results,
            "messages": [AIMessage(content="Fact-checking completed. Verified key claims and assessed source credibility.")],
            "current_step": "fact_check_complete"
        }

class SynthesizerAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Synthesizer Agent. Your job is to combine research findings into coherent, well-structured insights.

Tasks:
1. Identify key themes and patterns across search results
2. Reconcile conflicting information
3. Highlight the most important findings
4. Create logical connections between different pieces of information
5. Prepare synthesized content for final report generation

Focus on accuracy, completeness, and logical flow."""),
            ("human", """
Query: {query}
Search Results: {search_results}
Fact Check Results: {fact_check_results}

Please synthesize these findings into a coherent analysis.
""")
        ])
    
    async def synthesize(self, state: ResearchState) -> Dict[str, Any]:
        # Prepare data for synthesis
        search_summary = "\n".join([
            f"- {result['query']}: {result['results'][:500]}..."
            for result in state["search_results"]
        ])
        
        fact_check_summary = "\n".join([
            f"- {result.get('analysis', 'No analysis available')}"
            for result in state["fact_check_results"]
        ])
        
        chain = self.prompt | self.llm
        response = await chain.ainvoke({
            "query": state["query"],
            "search_results": search_summary,
            "fact_check_results": fact_check_summary
        })
        
        return {
            "synthesized_findings": response.content,
            "messages": [AIMessage(content="Successfully synthesized research findings into coherent insights.")],
            "current_step": "synthesis_complete"
        }

class ReportGeneratorAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Report Generator Agent. Create comprehensive, well-structured research reports.

Report Structure:
1. Executive Summary
2. Key Findings
3. Detailed Analysis
4. Sources and Credibility Assessment
5. Conclusions and Recommendations
6. Areas for Further Research

Make the report professional, readable, and actionable. Use markdown formatting for better presentation."""),
            ("human", """
Research Query: {query}
Synthesized Findings: {synthesized_findings}
Number of Sources Consulted: {source_count}

Generate a comprehensive research report.
""")
        ])
    
    async def generate_report(self, state: ResearchState) -> Dict[str, Any]:
        source_count = len(state["search_results"])
        
        chain = self.prompt | self.llm
        response = await chain.ainvoke({
            "query": state["query"],
            "synthesized_findings": state["synthesized_findings"],
            "source_count": source_count
        })
        
        return {
            "final_report": response.content,
            "messages": [AIMessage(content="Research report generated successfully!")],
            "current_step": "complete",
            "metadata": {
                "completion_time": datetime.now().isoformat(),
                "sources_consulted": source_count,
                "report_length": len(response.content)
            }
        }

# Node functions for LangGraph
async def analyze_query_node(state: ResearchState) -> ResearchState:
    agent = QueryAnalyzerAgent(llm)
    result = await agent.analyze_query(state)
    return {**state, **result}

async def research_node(state: ResearchState) -> ResearchState:
    agent = WebResearchAgent(llm)
    result = await agent.conduct_research(state)
    return {**state, **result}

async def fact_check_node(state: ResearchState) -> ResearchState:
    agent = FactCheckerAgent(llm)
    result = await agent.fact_check(state)
    return {**state, **result}

async def synthesize_node(state: ResearchState) -> ResearchState:
    agent = SynthesizerAgent(llm)
    result = await agent.synthesize(state)
    return {**state, **result}

async def report_generation_node(state: ResearchState) -> ResearchState:
    agent = ReportGeneratorAgent(llm)
    result = await agent.generate_report(state)
    return {**state, **result}

# Build the LangGraph workflow
def create_research_workflow():
    workflow = StateGraph(ResearchState)
    
    # Add nodes
    workflow.add_node("analyze_query", analyze_query_node)
    workflow.add_node("research", research_node)
    workflow.add_node("fact_check", fact_check_node)
    workflow.add_node("synthesize", synthesize_node)
    workflow.add_node("generate_report", report_generation_node)
    
    # Define the flow
    workflow.set_entry_point("analyze_query")
    workflow.add_edge("analyze_query", "research")
    workflow.add_edge("research", "fact_check")
    workflow.add_edge("fact_check", "synthesize")
    workflow.add_edge("synthesize", "generate_report")
    workflow.add_edge("generate_report", END)
    
    return workflow.compile()

# Main execution function
async def run_research_assistant(query: str) -> Dict[str, Any]:
    """
    Run the multi-agent research assistant on a given query.
    
    Args:
        query: The research question or topic to investigate
        
    Returns:
        Dictionary containing the final report and metadata
    """
    workflow = create_research_workflow()
    
    initial_state = ResearchState(
        query=query,
        research_tasks=[],
        search_results=[],
        fact_check_results=[],
        synthesized_findings="",
        final_report="",
        messages=[HumanMessage(content=f"Research request: {query}")],
        current_step="initialized",
        metadata={"start_time": datetime.now().isoformat()}
    )
    
    # Execute the workflow
    final_state = await workflow.ainvoke(initial_state)
    
    return {
        "query": final_state["query"],
        "report": final_state["final_report"],
        "metadata": final_state["metadata"],
        "steps_completed": final_state["current_step"],
        "sources_used": len(final_state["search_results"])
    }

# Example usage and testing
async def main():
    # Example research queries
    test_queries = [
        "What are the latest developments in quantum computing and their potential impact on cybersecurity?",
        "Analyze the current state of renewable energy adoption globally and key challenges",
        "What are the health implications of artificial sweeteners based on recent studies?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Research Query: {query}")
        print(f"{'='*60}")
        
        try:
            result = await run_research_assistant(query)
            print(f"\nReport Generated:")
            print(f"Sources Consulted: {result['sources_used']}")
            print(f"\n{result['report']}")
            
        except Exception as e:
            print(f"Error during research: {str(e)}")

def run_demo():
    """Run the demo queries - only when explicitly called."""
    asyncio.run(main())

if __name__ == "__main__":
    # Only run demo if this file is executed directly
    run_demo()