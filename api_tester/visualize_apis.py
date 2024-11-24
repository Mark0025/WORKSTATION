from graphviz import Digraph
from pathlib import Path
import json

def create_api_visualization():
    """Create a visual representation of our API ecosystem"""
    dot = Digraph(comment='API Ecosystem')
    dot.attr(rankdir='LR')
    
    # Define clusters for different API categories
    with dot.subgraph(name='cluster_ai') as c:
        c.attr(label='AI Services')
        c.node('openai', 'OpenAI API\n(Active)', color='green')
        c.node('huggingface', 'Hugging Face\n(Active)', color='green')
        c.node('crewai', 'CrewAI\n(Active)', color='green')
    
    with dot.subgraph(name='cluster_marketing') as c:
        c.attr(label='Marketing & CRM')
        c.node('ghl', 'GoHighLevel\n(Active)', color='green')
        c.node('mailgun', 'MailGun\n(Active)', color='green')
    
    with dot.subgraph(name='cluster_search') as c:
        c.attr(label='Search Services')
        c.node('serp', 'SERP API\n(Active)', color='green')
        c.node('google', 'Google Search\n(Active)', color='green')
    
    # Add connections
    dot.edge('openai', 'crewai', 'Powers')
    dot.edge('serp', 'crewai', 'Research')
    dot.edge('ghl', 'mailgun', 'Integration')
    
    # Save visualization
    dot.render('api_ecosystem', format='png', cleanup=True)

if __name__ == "__main__":
    create_api_visualization() 