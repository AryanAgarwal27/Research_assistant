import os
import asyncio
from typing import List, Dict, Any, TypedDict, Annotated
from datetime import datetime
import json

from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
import operator

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

# Simple research assistant function
async def simple_research_assistant(query: str) -> Dict[str, Any]:
    """
    A simplified version of the multi-agent research assistant.
    """
    print(f"🔍 Starting research for: {query}")
    
    # Step 1: Web Research
    print("📡 Conducting web research...")
    search_results = []
    
    # Create multiple search queries for comprehensive research
    search_queries = [
        query,
        f"{query} latest developments 2024",
        f"{query} expert analysis"
    ]
    
    for search_query in search_queries:
        try:
            result = web_search.invoke(search_query)
            search_results.append({
                "query": search_query,
                "results": result,
                "timestamp": datetime.now().isoformat()
            })
            print(f"✅ Search completed for: {search_query[:50]}...")
        except Exception as e:
            print(f"❌ Search failed for {search_query}: {e}")
    
    # Step 2: Generate report using LLM
    print("🤖 Generating comprehensive report...")
    
    # Combine search results
    combined_results = "\n\n".join([
        f"Search Query: {result['query']}\nResults: {result['results']}"
        for result in search_results
    ])
    
    # Create report generation prompt
    report_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional research analyst. Create a comprehensive, well-structured research report based on the provided search results.

Report Structure:
1. Executive Summary
2. Key Findings
3. Detailed Analysis
4. Current Trends and Developments
5. Conclusions and Recommendations
6. Areas for Further Research

Make the report professional, readable, and actionable. Use markdown formatting for better presentation."""),
        ("human", """
Research Query: {query}
Search Results: {search_results}

Generate a comprehensive research report based on this information.
""")
    ])
    
    try:
        chain = report_prompt | llm
        response = await chain.ainvoke({
            "query": query,
            "search_results": combined_results
        })
        
        report = response.content
        print("✅ Report generated successfully!")
        
        return {
            "query": query,
            "report": report,
            "sources_used": len(search_results),
            "metadata": {
                "completion_time": datetime.now().isoformat(),
                "report_length": len(report)
            }
        }
        
    except Exception as e:
        return {
            "query": query,
            "report": f"Error generating report: {str(e)}",
            "sources_used": len(search_results),
            "metadata": {
                "completion_time": datetime.now().isoformat(),
                "error": str(e)
            }
        }

async def run_research_demo():
    """Run a demonstration of the research assistant."""
    print("🚀 Multi-Agent Research Assistant Demo")
    print("=" * 60)
    
    # Demo queries
    demo_queries = [
        "What are the latest developments in artificial intelligence in 2024?",
        "What is the current state of electric vehicle adoption?",
        "What are the benefits and risks of remote work?"
    ]
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n📋 Demo {i}/3")
        print("-" * 40)
        
        try:
            result = await simple_research_assistant(query)
            
            print(f"\n✅ Research completed for: {query}")
            print(f"📊 Sources consulted: {result['sources_used']}")
            print(f"📝 Report length: {result['metadata']['report_length']} characters")
            
            print("\n📋 RESEARCH REPORT:")
            print("=" * 60)
            print(result['report'])
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Error during research: {e}")
        
        if i < len(demo_queries):
            print("\n⏳ Waiting 3 seconds before next query...")
            await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(run_research_demo()) 