"""
Tool for searching scientific and research content using the Tavily API.

This module provides an enhanced search tool specifically optimized for
finding academic and scientific papers and research content.
"""

import os
import logging
import json
from typing import Dict, Any, List, Optional
from tavily import TavilyClient
from langchain.tools import BaseTool
from crewai.tools import BaseTool as CrewAIBaseTool

# Import configuration
from config.settings import (
    TAVILY_API_KEY,
    SEARCH_MAX_RESULTS,
    SEARCH_MAX_PAGES
)

logger = logging.getLogger(__name__)


class TavilySearchTool(CrewAIBaseTool, BaseTool):
    """
    Tool for performing scientific and academic searches using the Tavily API.
    Optimized for finding research papers and scientific content.
    """

    name = "tavily_search"
    description = """
    Use this tool to search for scientific papers, research articles, and 
    academic content. Provides more comprehensive results than standard web search
    for academic and scientific queries.
    Input should be a search query related to scientific or research topics.
    """

    def __init__(
            self,
            api_key: Optional[str] = None,
            max_results: int = SEARCH_MAX_RESULTS,
            search_depth: str = "advanced",
            include_answer: bool = True,
            include_domains: Optional[List[str]] = None,
            exclude_domains: Optional[List[str]] = None
    ):
        """
        Initialize the Tavily search tool with custom parameters.

        Args:
            api_key: Tavily API key (defaults to environment variable)
            max_results: Maximum number of search results to return
            search_depth: Either "basic" or "advanced" search
            include_answer: Whether to include Tavily's generated answer
            include_domains: List of domains to include in search
            exclude_domains: List of domains to exclude from search
        """
        super().__init__()
        self.api_key = api_key or TAVILY_API_KEY or os.getenv("TAVILY_API_KEY")
        self.max_results = max_results
        self.search_depth = search_depth
        self.include_answer = include_answer

        # Default to academic and scientific domains if none provided
        self.include_domains = include_domains or [
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

        self.exclude_domains = exclude_domains or []

        if not self.api_key:
            logger.error("Tavily API key not found. Set TAVILY_API_KEY env variable.")
            raise ValueError("Tavily API key is required. Please set TAVILY_API_KEY environment variable.")

        self.client = TavilyClient(api_key=self.api_key)

    def _optimize_query_for_research(self, query: str) -> str:
        """
        Optimize a search query for academic and scientific results.

        Args:
            query: The original search query

        Returns:
            str: Optimized query for research papers
        """
        # Add academic qualifiers if they're not already present
        academic_terms = ["research", "paper", "study", "journal", "publication", "article"]

        # Check if any academic terms are already in the query
        has_academic_terms = any(term in query.lower() for term in academic_terms)

        if not has_academic_terms:
            # Add research paper qualifier
            optimized_query = f"{query} research papers"
        else:
            optimized_query = query

        return optimized_query

    def _process_search_results(self, results: Dict[str, Any]) -> str:
        """
        Process and format the search results for output.

        Args:
            results: Raw search results from Tavily API

        Returns:
            str: Formatted search results
        """
        output = []

        # Add Tavily's answer if available and requested
        if self.include_answer and "answer" in results and results["answer"]:
            output.append(f"Tavily Answer: {results['answer']}\n")

        # Add individual search results
        if "results" in results and results["results"]:
            output.append("Search Results:")

            for i, result in enumerate(results["results"], 1):
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

        return "\n".join(output)

    def _run(self, query: str) -> str:
        """
        Run the search tool with the given query.

        Args:
            query: The search query

        Returns:
            str: Formatted search results or error message
        """
        logger.info(f"Searching Tavily for: {query}")

        try:
            # Optimize query for research papers
            optimized_query = self._optimize_query_for_research(query)
            logger.debug(f"Optimized query: {optimized_query}")

            # Perform the search
            search_results = self.client.search(
                query=optimized_query,
                search_depth=self.search_depth,
                max_results=self.max_results,
                include_answer=self.include_answer,
                include_domains=self.include_domains,
                exclude_domains=self.exclude_domains
            )

            # Process and format results
            formatted_results = self._process_search_results(search_results)
            logger.info(f"Search completed successfully for: {query}")

            return formatted_results

        except Exception as e:
            error_msg = f"Error searching Tavily: {str(e)}"
            logger.error(error_msg)
            return error_msg

    def run(self, query: str) -> str:
        """
        Run the search tool (CrewAI compatible method).

        Args:
            query: The search query

        Returns:
            str: Formatted search results or error message
        """
        return self._run(query)