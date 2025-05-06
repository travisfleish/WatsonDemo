"""
Tool for scraping website content.
"""
import logging
import requests
from bs4 import BeautifulSoup
import time
from typing import Dict, Any, Optional, List

# Import from the base_tool module directly to avoid circular imports
from tools.base_tool import create_tool

# Import configuration
from config.settings import (
    SCRAPE_TIMEOUT,
    SCRAPE_MAX_RETRIES,
    SCRAPE_USER_AGENT
)

logger = logging.getLogger(__name__)

def scrape_website_func(url: str) -> str:
    """
    Extract text content from a website URL.
    Particularly useful for scientific papers, research articles, and academic websites.

    Args:
        url: The URL to scrape

    Returns:
        str: Extracted content or error message
    """
    logger.info(f"Scraping website: {url}")

    # Define headers
    headers = {
        'User-Agent': SCRAPE_USER_AGENT
    }

    def extract_main_content(soup):
        """Extract the main content from a webpage"""
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

    def extract_metadata(soup):
        """Extract metadata from an academic paper or website"""
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

    # Main execution
    try:
        # Make the request
        response = requests.get(url, headers=headers, timeout=SCRAPE_TIMEOUT)
        response.raise_for_status()

        # Check if content is HTML
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type and 'application/xhtml+xml' not in content_type:
            return f"URL does not contain HTML content. Content-Type: {content_type}"

        # Parse HTML
        soup = BeautifulSoup(response.content, 'lxml')

        # Extract content and metadata
        content = extract_main_content(soup)
        metadata = extract_metadata(soup)

        # Format the output
        output = ""

        if metadata:
            if "title" in metadata:
                output += f"Title: {metadata['title']}\n\n"

            if "authors" in metadata:
                output += f"Authors: {metadata['authors']}\n\n"

            if "publication_date" in metadata:
                output += f"Publication Date: {metadata['publication_date']}\n\n"

        # Limit content length to avoid token limits
        if content:
            if len(content) > 8000:
                output += f"Content (truncated):\n{content[:8000]}...\n\n"
                output += f"[Content truncated, full text is {len(content)} characters]"
            else:
                output += f"Content:\n{content}"

        logger.info(f"Successfully scraped website: {url}")
        return output

    except requests.exceptions.Timeout:
        return f"Timeout occurred while scraping {url}"

    except requests.exceptions.HTTPError as e:
        return f"HTTP error {e.response.status_code} while scraping {url}: {str(e)}"

    except requests.exceptions.RequestException as e:
        return f"Error requesting {url}: {str(e)}"

    except Exception as e:
        error_msg = f"Unexpected error scraping {url}: {str(e)}"
        logger.error(error_msg)
        return error_msg

# Create the tool
scrape_website = create_tool(
    func=scrape_website_func,
    name="scrape_website",
    description="Extract text content from a website URL. Particularly useful for scientific papers and research articles."
)