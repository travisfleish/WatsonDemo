"""
Tool for searching scientific and research content using the Tavily API.
"""
import os
import logging
import json
from typing import Dict, Any, List, Optional
from tavily import TavilyClient

# Import from the base_tool module directly to avoid circular imports
from tools.base_tool import create_tool

# Import configuration
from config.settings import (
    TAVILY_API_KEY,
    SEARCH_MAX_RESULTS,
    SEARCH_MAX_PAGES
)

logger = logging.getLogger(__name__)

def tavily_search_func(query: str) -> str:
    """
    Search for scientific papers, research articles, and academic content.

    Args:
        query: The search query

    Returns:
        str: Formatted search results
    """
    logger.info(f"Searching Tavily for: {query}")

    # Get API key
    api_key = TAVILY_API_KEY or os.getenv("TAVILY_API_KEY")

    if not api_key:
        error_msg = "Tavily API key not found. Set TAVILY_API_KEY env variable."
        logger.error(error_msg)
        return error_msg

    # Configuration
    max_results = SEARCH_MAX_RESULTS
    search_depth = "advanced"
    include_answer = True

    # Include domains focused on academic sources
    include_domains = [
        "scholar.google.com",
        "arxiv.org",
        "academia.edu",
        "researchgate.net",
        "sciencedirect.com",
        "nature.com",
        "science.org",
        "pubmed.ncbi.nlm.nih.gov",
        "ieee.org",
        "acm.org",
        "jstor.org"
    ]

    # Optimize query for research papers if needed
    academic_terms = ["research", "paper", "study", "journal", "publication", "article"]
    has_academic_terms = any(term in query.lower() for term in academic_terms)
    optimized_query = f"{query} research papers" if not has_academic_terms else query

    try:
        # Initialize client
        client = TavilyClient(api_key=api_key)

        # Perform the search
        search_results = client.search(
            query=optimized_query,
            search_depth=search_depth,
            max_results=max_results,
            include_answer=include_answer,
            include_domains=include_domains
        )

        # Process results
        output = []

        # Add Tavily's answer if available and requested
        if include_answer and "answer" in search_results and search_results["answer"]:
            output.append(f"Tavily Answer: {search_results['answer']}\n")

        # Add individual search results
        if "results" in search_results and search_results["results"]:
            output.append("Search Results:")

            for i, result in enumerate(search_results["results"], 1):
                title = result.get("title", "No Title")
                content = result.get("content", "No Content")
                url = result.get("url", "No URL")
                score = result.get("score", 0)

                result_text = f"\n{i}. {title}\n"
                result_text += f"   URL: {url}\n"
                result_text += f"   Relevance Score: {score:.2f}\n"
                result_text += f"   Summary: {content[:300]}...\n"

                output.append(result_text)
        else:
            output.append("No search results found.")

        logger.info(f"Search completed successfully for: {query}")
        return "\n".join(output)

    except Exception as e:
        error_msg = f"Error searching Tavily: {str(e)}"
        logger.error(error_msg)
        return error_msg

# Create the tool
tavily_search = create_tool(
    func=tavily_search_func,
    name="tavily_search",
    description="Search for scientific papers, research articles, and academic content."
)