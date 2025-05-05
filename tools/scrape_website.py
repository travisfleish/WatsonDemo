"""
Tool for scraping website content.

This module provides a tool for extracting content from websites, specifically
designed for scraping research papers and related scientific content.
"""

import logging
import requests
from bs4 import BeautifulSoup
import time
from typing import Dict, Any, Optional, List
from langchain.tools import BaseTool
from crewai.tools import BaseTool as CrewAIBaseTool

# Import configuration
from config.settings import (
    SCRAPE_TIMEOUT,
    SCRAPE_MAX_RETRIES,
    SCRAPE_USER_AGENT
)

logger = logging.getLogger(__name__)


class ScrapeWebsiteTool(CrewAIBaseTool, BaseTool):
    """
    Tool for scraping website content, particularly useful for extracting
    information from scientific papers and research articles.
    """

    name = "scrape_website"
    description = """
    Use this tool to extract text content from a website URL.
    Particularly useful for scientific papers, research articles, and academic websites.
    Input should be a valid URL.
    """

    def __init__(self):
        """Initialize the scraping tool with default parameters."""
        super().__init__()
        self.timeout = SCRAPE_TIMEOUT
        self.max_retries = SCRAPE_MAX_RETRIES
        self.user_agent = SCRAPE_USER_AGENT
        self.headers = {
            'User-Agent': self.user_agent
        }

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """
        Extract the main content from a webpage, with special handling for
        common academic and scientific paper formats.

        Args:
            soup: BeautifulSoup object of the parsed HTML

        Returns:
            str: Extracted main content
        """
        # Try to find common content containers in academic sites
        content_candidates = []

        # Look for article or main content tags
        article_tags = soup.find_all(['article', 'main', 'div'])

        for tag in article_tags:
            # Check for common article class/id names
            if tag.get('class') and any(c in str(tag.get('class')) for c in [
                'article', 'content', 'paper', 'research', 'abstract', 'body', 'text', 'main'
            ]):
                content_candidates.append(tag)

            # Check for common article IDs
            if tag.get('id') and any(c in str(tag.get('id')) for c in [
                'article', 'content', 'paper', 'research', 'abstract', 'body', 'text', 'main'
            ]):
                content_candidates.append(tag)

        # If we found potential content containers, use the longest one
        if content_candidates:
            content_candidates.sort(key=lambda x: len(str(x)), reverse=True)
            return content_candidates[0].get_text(separator=' ', strip=True)

        # Fallback to common academic paper sections
        sections = []

        # Try to extract paper sections
        for section_tag in soup.find_all(['section', 'div', 'h1', 'h2', 'h3']):
            # Check for common section headers in papers
            if any(header in section_tag.get_text().lower() for header in [
                'abstract', 'introduction', 'method', 'methodology', 'result',
                'discussion', 'conclusion', 'reference'
            ]):
                # Get the section and its content
                sections.append(f"\n\n{section_tag.get_text(strip=True)}")

                # Try to get the content following this section header
                next_el = section_tag.find_next_sibling()
                if next_el:
                    sections.append(next_el.get_text(separator=' ', strip=True))

        if sections:
            return "\n".join(sections)

        # Last resort: get all paragraphs
        paragraphs = soup.find_all('p')
        if paragraphs:
            return "\n".join(p.get_text(strip=True) for p in paragraphs)

        # If all else fails, return the whole body content
        return soup.get_text(separator=' ', strip=True)

    def _extract_metadata(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extract metadata from an academic paper or website.

        Args:
            soup: BeautifulSoup object of the parsed HTML

        Returns:
            Dict[str, str]: Dictionary of metadata
        """
        metadata = {}

        # Try to extract title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text(strip=True)

        # Try to extract publication date
        date_tags = soup.find_all(['time', 'meta'])
        for tag in date_tags:
            if tag.name == 'meta' and tag.get('name') in ['date', 'pubdate', 'publication_date']:
                metadata['publication_date'] = tag.get('content')
                break
            if tag.name == 'time' and tag.get('datetime'):
                metadata['publication_date'] = tag.get('datetime')
                break

        # Try to extract authors
        author_tags = soup.find_all(['meta', 'a', 'span', 'div'])
        authors = []

        for tag in author_tags:
            # Check meta tags
            if tag.name == 'meta' and tag.get('name') in ['author', 'citation_author']:
                authors.append(tag.get('content'))

            # Check for author links or spans
            if tag.name in ['a', 'span', 'div'] and tag.get('class'):
                if any(c in str(tag.get('class')) for c in ['author', 'creator', 'contributor']):
                    authors.append(tag.get_text(strip=True))

        if authors:
            metadata['authors'] = ', '.join(list(set(authors)))

        return metadata

    def _process_url(self, url: str, retries: int = 0) -> Dict[str, Any]:
        """
        Process a URL to extract content and metadata with retry logic.

        Args:
            url: The URL to scrape
            retries: Current retry count

        Returns:
            Dict[str, Any]: Dictionary containing content and metadata
        """
        if retries >= self.max_retries:
            logger.error(f"Max retries ({self.max_retries}) exceeded for URL: {url}")
            return {"error": f"Failed to scrape URL after {self.max_retries} attempts."}

        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()

            # Check if content is HTML
            content_type = response.headers.get('Content-Type', '')
            if 'text/html' not in content_type and 'application/xhtml+xml' not in content_type:
                return {
                    "error": f"URL does not contain HTML content. Content-Type: {content_type}",
                    "raw_content": response.text[:1000]  # First 1000 chars for inspection
                }

            # Parse HTML
            soup = BeautifulSoup(response.content, 'lxml')

            # Extract content and metadata
            content = self._extract_main_content(soup)
            metadata = self._extract_metadata(soup)

            return {
                "content": content,
                "metadata": metadata,
                "url": url
            }

        except requests.exceptions.Timeout:
            logger.warning(f"Timeout occurred for URL: {url}. Retrying ({retries + 1}/{self.max_retries})...")
            time.sleep(2 ** retries)  # Exponential backoff
            return self._process_url(url, retries + 1)

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            logger.error(f"HTTP error {status_code} for URL: {url}")

            if status_code in [429, 503]:  # Rate limiting or service unavailable
                if retries < self.max_retries:
                    wait_time = 2 ** retries  # Exponential backoff
                    logger.info(f"Rate limited or service unavailable. Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    return self._process_url(url, retries + 1)

            return {"error": f"HTTP error {status_code}: {str(e)}"}

        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception for URL {url}: {str(e)}")
            return {"error": f"Failed to fetch URL: {str(e)}"}

        except Exception as e:
            logger.error(f"Unexpected error processing URL {url}: {str(e)}")
            return {"error": f"Unexpected error: {str(e)}"}

    def _run(self, url: str) -> str:
        """
        Run the scraping tool on a URL.

        Args:
            url: The URL to scrape

        Returns:
            str: Extracted content or error message
        """
        logger.info(f"Scraping website: {url}")
        result = self._process_url(url)

        if "error" in result:
            logger.error(f"Error scraping {url}: {result['error']}")
            return f"Failed to scrape website: {result['error']}"

        # Format the output
        output = ""

        if "metadata" in result:
            metadata = result["metadata"]
            if "title" in metadata:
                output += f"Title: {metadata['title']}\n\n"

            if "authors" in metadata:
                output += f"Authors: {metadata['authors']}\n\n"

            if "publication_date" in metadata:
                output += f"Publication Date: {metadata['publication_date']}\n\n"

        if "content" in result:
            # Limit content length to avoid token limits
            content = result["content"]
            if len(content) > 8000:
                output += f"Content (truncated):\n{content[:8000]}...\n\n"
                output += f"[Content truncated, full text is {len(content)} characters]"
            else:
                output += f"Content:\n{content}"

        logger.info(f"Successfully scraped website: {url}")
        return output

    def run(self, url: str) -> str:
        """
        Run the scraping tool (CrewAI compatible method).

        Args:
            url: The URL to scrape

        Returns:
            str: Extracted content or error message
        """
        return self._run(url)