"""
Visualization components for the research proposal generation system.

This module provides components for visualizing the research proposal generation
process and results in the Streamlit application.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from datetime import datetime


def create_workflow_diagram():
    """
    Create a visualization of the research proposal generation workflow.

    Returns:
        go.Figure: Plotly figure object
    """
    # Define the workflow steps
    stages = [
        "Research Paper Finding",
        "Paper Analysis",
        "Idea Generation",
        "Idea Refinement",
        "Proposal Development"
    ]

    # Create a figure
    fig = go.Figure()

    # Add nodes for each stage
    for i, stage in enumerate(stages):
        fig.add_trace(go.Scatter(
            x=[i],
            y=[0],
            mode="markers+text",
            marker=dict(size=30, color="#3B82F6", symbol="circle"),
            text=[str(i + 1)],
            textfont=dict(color="white", size=14),
            name=stage,
            hoverinfo="text",
            hovertext=stage
        ))

    # Add connecting lines
    fig.add_trace(go.Scatter(
        x=list(range(len(stages))),
        y=[0] * len(stages),
        mode="lines",
        line=dict(width=3, color="#93C5FD"),
        hoverinfo="skip"
    ))

    # Add stage labels
    for i, stage in enumerate(stages):
        fig.add_annotation(
            x=i,
            y=-0.15,
            text=stage,
            showarrow=False,
            font=dict(size=12)
        )

    # Update layout
    fig.update_layout(
        title="Research Proposal Generation Workflow",
        showlegend=False,
        hovermode="closest",
        height=250,
        margin=dict(l=20, r=20, t=50, b=80),
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[-0.3, 0.3]
        ),
        plot_bgcolor="rgba(0,0,0,0)"
    )

    return fig


def create_workflow_status(current_stage=None):
    """
    Create a visualization of the workflow status.

    Args:
        current_stage (str, optional): Current stage in the workflow

    Returns:
        go.Figure: Plotly figure object
    """
    # Define the workflow steps
    stages = [
        "Paper Finding",
        "Paper Analysis",
        "Idea Generation",
        "Idea Refinement",
        "Proposal Development"
    ]

    # Map stage names to indices
    stage_index = {
        "paper_finding": 0,
        "paper_analysis": 1,
        "idea_generation": 2,
        "idea_refinement": 3,
        "proposal_development": 4
    }

    # Determine which stages are complete
    current_idx = stage_index.get(current_stage, -1)

    # Create a figure
    fig = go.Figure()

    # Add nodes for each stage with appropriate colors
    for i, stage in enumerate(stages):
        if i < current_idx:  # Completed stages
            color = "#22C55E"  # Green
        elif i == current_idx:  # Current stage
            color = "#3B82F6"  # Blue
        else:  # Future stages
            color = "#9CA3AF"  # Gray

        fig.add_trace(go.Scatter(
            x=[i],
            y=[0],
            mode="markers+text",
            marker=dict(size=30, color=color, symbol="circle"),
            text=[str(i + 1)],
            textfont=dict(color="white", size=14),
            name=stage,
            hoverinfo="text",
            hovertext=stage
        ))

    # Add connecting lines with appropriate colors
    for i in range(len(stages) - 1):
        if i < current_idx:  # Completed connection
            color = "#22C55E"  # Green
        elif i == current_idx:  # Current connection
            color = "#3B82F6"  # Blue
        else:  # Future connection
            color = "#9CA3AF"  # Gray

        fig.add_trace(go.Scatter(
            x=[i, i + 1],
            y=[0, 0],
            mode="lines",
            line=dict(width=3, color=color),
            hoverinfo="skip",
            showlegend=False
        ))

    # Add stage labels
    for i, stage in enumerate(stages):
        fig.add_annotation(
            x=i,
            y=-0.15,
            text=stage,
            showarrow=False,
            font=dict(size=12)
        )

    # Update layout
    fig.update_layout(
        showlegend=False,
        hovermode="closest",
        height=200,
        margin=dict(l=20, r=20, t=20, b=60),
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[-0.3, 0.3]
        ),
        plot_bgcolor="rgba(0,0,0,0)"
    )

    return fig


def create_paper_network(papers, width=700, height=500):
    """
    Create a network visualization of the related papers.

    Args:
        papers (list): List of paper dictionaries
        width (int): Width of the figure
        height (int): Height of the figure

    Returns:
        go.Figure: Plotly figure object
    """
    if not papers:
        return None

    # Create nodes for papers
    nodes = []
    for i, paper in enumerate(papers):
        nodes.append({
            "id": i,
            "title": paper.get("title", f"Paper {i}"),
            "authors": paper.get("authors", "Unknown"),
            "year": paper.get("year", "Unknown"),
            "size": 15  # Base size for all papers
        })

    # Create edges between papers (simple connections for visualization)
    edges = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            # Only connect some papers to avoid clutter
            if (i + j) % 2 == 0:
                edges.append({
                    "source": i,
                    "target": j,
                    "weight": 1
                })

    # Create a force-directed graph layout
    import networkx as nx
    G = nx.Graph()

    # Add nodes with attributes
    for node in nodes:
        G.add_node(node["id"], title=node["title"], authors=node["authors"], year=node["year"])

    # Add edges
    for edge in edges:
        G.add_edge(edge["source"], edge["target"], weight=edge["weight"])

    # Calculate layout
    pos = nx.spring_layout(G, seed=42)

    # Extract node positions
    node_x = []
    node_y = []
    node_text = []
    for node_id, position in pos.items():
        node_x.append(position[0])
        node_y.append(position[1])

        # Get node data
        node_data = next(node for node in nodes if node["id"] == node_id)
        hover_text = f"Title: {node_data['title']}<br>Authors: {node_data['authors']}<br>Year: {node_data['year']}"
        node_text.append(hover_text)

    # Create edges traces
    edge_x = []
    edge_y = []
    for edge in edges:
        source_pos = pos[edge["source"]]
        target_pos = pos[edge["target"]]
        edge_x.extend([source_pos[0], target_pos[0], None])
        edge_y.extend([source_pos[1], target_pos[1], None])

    # Create figure
    fig = go.Figure()

    # Add edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.8, color="#CBD5E1"),
        hoverinfo="none",
        mode="lines",
        showlegend=False
    ))

    # Add nodes
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode="markers",
        marker=dict(
            size=15,
            color="#3B82F6",
            line=dict(width=1, color="#1E40AF")
        ),
        text=node_text,
        hoverinfo="text",
        showlegend=False
    ))

    # Update layout
    fig.update_layout(
        title="Research Paper Network",
        width=width,
        height=height,
        showlegend=False,
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        plot_bgcolor="rgba(0,0,0,0)"
    )

    return fig


def create_methodology_comparison(proposals):
    """
    Create a radar chart comparing methodologies across proposals.

    Args:
        proposals (list): List of proposal dictionaries

    Returns:
        go.Figure: Plotly figure object
    """
    if not proposals:
        return None

    # Define methodology categories for comparison
    categories = [
        "Data Collection",
        "Computational Methods",
        "Experimental Design",
        "Analysis Techniques",
        "Validation Approaches"
    ]

    # For each proposal, score each category from 0-5 based on keyword presence
    # (This is a simplified approach - in a real system, you would use NLP)
    data = []
    for i, proposal in enumerate(proposals):
        methodology = proposal.get("methodology", "").lower()

        # Simple keyword-based scoring
        keywords = {
            "Data Collection": ["survey", "interview", "dataset", "corpus", "collection"],
            "Computational Methods": ["algorithm", "computation", "model", "simulation", "neural"],
            "Experimental Design": ["experiment", "control", "variable", "trial", "condition"],
            "Analysis Techniques": ["analysis", "statistical", "regression", "correlation", "significance"],
            "Validation Approaches": ["validation", "accuracy", "precision", "recall", "evaluation"]
        }

        scores = []
        for category, words in keywords.items():
            score = 0
            for word in words:
                if word in methodology:
                    score += 1
            scores.append(min(5, score))  # Cap at 5

        data.append({
            "Proposal": proposal.get("proposal_title", f"Proposal {i + 1}"),
            **{category: score for category, score in zip(categories, scores)}
        })

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Create radar chart
    fig = go.Figure()

    for i, row in df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=row[categories].values.tolist(),
            theta=categories,
            fill="toself",
            name=row["Proposal"]
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        title="Methodology Comparison",
        showlegend=True,
        height=500
    )

    return fig


def create_timeline_visualization(proposals):
    """
    Create a Gantt chart of the proposed research timelines.

    Args:
        proposals (list): List of proposal dictionaries

    Returns:
        go.Figure: Plotly figure object
    """
    if not proposals:
        return None

    # Extract timeline data from proposals
    # This is a simplified approach - in a real system, you would use NLP to parse timelines
    tasks = []

    for i, proposal in enumerate(proposals):
        title = proposal.get("proposal_title", f"Proposal {i + 1}")
        timeline = proposal.get("timeline", "")

        # Simple parsing for timeline phases
        # Look for patterns like "Phase 1 (Month 1-3): Description"
        import re

        # Fallback timeline if parsing fails
        default_tasks = [
            {"phase": "Literature Review", "start": 1, "end": 2},
            {"phase": "Data Collection", "start": 2, "end": 5},
            {"phase": "Analysis", "start": 5, "end": 8},
            {"phase": "Validation", "start": 8, "end": 10},
            {"phase": "Documentation", "start": 10, "end": 12}
        ]

        # Try to parse the timeline
        parsed_tasks = []

        # Simple regex to find time periods
        pattern = r"(Phase \d+|[^:.(]+).*?(\d+)[-–](\d+).*?(?:month|months|week|weeks)"
        matches = re.findall(pattern, timeline, re.IGNORECASE)

        if matches:
            for match in matches:
                phase = match[0].strip()
                start = int(match[1])
                end = int(match[2])
                parsed_tasks.append({"phase": phase, "start": start, "end": end})

        # Use parsed tasks or default
        proposal_tasks = parsed_tasks if parsed_tasks else default_tasks

        # Add to overall tasks list
        for task in proposal_tasks:
            tasks.append({
                "Proposal": title,
                "Phase": task["phase"],
                "Start": task["start"],
                "End": task["end"]
            })

    # Create DataFrame
    df = pd.DataFrame(tasks)

    # Create Gantt chart
    fig = px.timeline(
        df,
        x_start="Start",
        x_end="End",
        y="Proposal",
        color="Phase",
        title="Research Timeline Comparison"
    )

    # Update layout
    fig.update_layout(
        xaxis_title="Months",
        yaxis_title="",
        height=300 + (len(proposals) * 50),
        xaxis=dict(
            tickvals=list(range(1, 13)),
            ticktext=[f"Month {i}" for i in range(1, 13)]
        )
    )

    return fig


def display_proposal_statistics(proposals):
    """
    Display statistics about the generated proposals.

    Args:
        proposals (list): List of proposal dictionaries
    """
    if not proposals:
        return

    st.markdown("### Proposal Statistics")

    # Create metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Proposals", len(proposals))

    # Calculate average methodology length
    avg_methodology_length = sum(len(p.get("methodology", "")) for p in proposals) / len(proposals)
    with col2:
        st.metric("Avg. Methodology Length", f"{int(avg_methodology_length)} chars")

    # Calculate average number of research questions
    avg_questions = sum(len(p.get("research_questions", [])) for p in proposals) / len(proposals)
    with col3:
        st.metric("Avg. Research Questions", f"{avg_questions:.1f}")

    # Create a word cloud of the most common terms
    try:
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt

        # Combine all text from proposals
        all_text = " ".join([
            p.get("introduction", "") + " " +
            p.get("methodology", "") + " " +
            p.get("expected_outcomes", "")
            for p in proposals
        ])

        # Create word cloud
        stopwords = {"the", "and", "to", "of", "a", "in", "that", "is", "for", "this", "will", "be", "on", "an", "with",
                     "as"}
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color="white",
            stopwords=stopwords,
            max_words=100,
            contour_width=3,
            contour_color="steelblue"
        ).generate(all_text)

        # Display word cloud
        st.markdown("### Key Terms in Proposals")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

    except ImportError:
        st.info("Install wordcloud package for term visualization")