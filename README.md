# Research Proposal Generation System

A multi-agent system that generates novel research proposals based on existing scientific papers using CrewAI and large language models.

## Overview

This system implements an end-to-end workflow for generating research proposals by:
1. Finding relevant research papers
2. Analyzing their content
3. Generating initial research ideas
4. Refining those ideas
5. Developing complete research proposals

The system uses a crew of specialized AI agents, each focused on a specific task in the research pipeline.

## Architecture

The project is structured around the CrewAI framework with:

- **Agents**: Specialized AI entities with specific roles in the research process
- **Tasks**: Well-defined units of work assigned to agents
- **Crew**: An orchestration layer that manages task execution

## Prerequisites

- Python 3.9+
- IBM WatsonX API access
- Tavily API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/research-proposal-generator.git
cd research-proposal-generator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Usage

Run the main script with your research paper title:

```bash
python main.py "Your Research Paper Title"
```

Or import the module in your Python code:

```python
from main import main

results = main("Advanced Machine Learning Techniques for Scientific Discovery")
```

## Components

### Agents

- **Research Paper Finder**: Searches for relevant scientific papers
- **Research Paper Analyst**: Extracts key knowledge and limitations from papers
- **Seed Idea Generator**: Generates initial research ideas
- **Idea Refinement Specialist**: Enhances and refines research ideas
- **Research Proposal Developer**: Develops complete research proposals

### Tasks

Each agent has a corresponding task that defines its work:

- **Paper Finding Task**: Find related papers
- **Paper Analysis Task**: Extract knowledge from papers
- **Idea Generation Task**: Generate research ideas
- **Idea Refinement Task**: Refine and enhance ideas
- **Proposal Development Task**: Develop complete proposals

## Configuration

Configuration is managed through:
- Environment variables (API keys, etc.)
- Settings module (`config/settings.py`)
- Prompt templates (`prompts/templates.yaml`)

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.