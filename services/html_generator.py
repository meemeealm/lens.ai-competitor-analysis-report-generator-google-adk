"""
HTML Report Generator
Converts structured JSON data into formatted HTML reports
"""

from typing import Dict, Any
from datetime import datetime
from agents.schemas import HTML_TEMPLATE


def format_html_from_json(data: Dict[str, Any]) -> str:
    """
    Convert JSON competitor data to formatted HTML report
    
    This is a pure Python function - NO LLM CALLS
    Significantly reduces costs by avoiding unnecessary AI processing
    
    Args:
        data: Dictionary containing competitor analysis data
        
    Returns:
        Complete HTML report as string
    """
    
    # Format products/services section
    products_html = _format_products(data.get("products_services", []))
    
    # Format competitors tags
    competitors_html = _format_competitors(
        data.get("market_position", {}).get("key_competitors", [])
    )
    
    # Format strengths and weaknesses
    strengths_html = _format_list_items(data.get("strengths", []), css_class="list-item")
    weaknesses_html = _format_list_items(data.get("weaknesses", []), css_class="list-item weakness")
    
    # Format recent news
    news_html = _format_news(data.get("recent_news", []))
    
    # Format technology stack
    tech_html = _format_tags(data.get("technology_stack", []))
    
    # Format social media links
    social_html = _format_social_media(data.get("social_media_presence", {}))
    
    # Populate and return template
    return HTML_TEMPLATE.format(
        company_name=data.get("company_name", "Unknown Company"),
        website=data.get("website", "#"),
        analysis_date=data.get("analysis_date", datetime.now().strftime("%Y-%m-%d")),
        description=data.get("overview", {}).get("description", "No description available"),
        founded_year=data.get("overview", {}).get("founded_year") or "N/A",
        headquarters=data.get("overview", {}).get("headquarters") or "N/A",
        size=data.get("overview", {}).get("size") or "N/A",
        products_html=products_html,
        target_market=data.get("market_position", {}).get("target_market", "N/A"),
        market_share=data.get("market_position", {}).get("market_share") or "N/A",
        competitors_html=competitors_html,
        strengths_html=strengths_html,
        weaknesses_html=weaknesses_html,
        news_html=news_html,
        pricing_model=data.get("pricing_model") or "N/A",
        tech_html=tech_html,
        social_html=social_html
    )


def _format_products(products: list) -> str:
    """Format products/services into HTML cards"""
    if not products:
        return "<p>No product information available.</p>"
    
    html = '<div class="grid">'
    for product in products:
        html += f"""
        <div class="card">
            <h3>{product.get('name', 'N/A')}</h3>
            <p><strong>Category:</strong> {product.get('category', 'N/A')}</p>
            <p>{product.get('description', 'No description available')}</p>
        </div>
        """
    html += '</div>'
    return html


def _format_competitors(competitors: list) -> str:
    """Format competitor names as tags"""
    if not competitors:
        return "<p>No competitor information available.</p>"
    
    return "".join([f'<span class="tag">{comp}</span>' for comp in competitors])


def _format_list_items(items: list, css_class: str = "list-item") -> str:
    """Format list items with specified CSS class"""
    if not items:
        return "<p>No information available.</p>"
    
    return "".join([f'<div class="{css_class}">{item}</div>' for item in items])


def _format_news(news_items: list) -> str:
    """Format news items into styled cards"""
    if not news_items:
        return "<p>No recent news available.</p>"
    
    html = ""
    for news in news_items:
        html += f"""
        <div class="news-item">
            <h3>{news.get('title', 'No Title')}</h3>
            <p class="meta"><em>{news.get('date', 'N/A')} • {news.get('source', 'Unknown Source')}</em></p>
            <p>{news.get('summary', 'No summary available')}</p>
        </div>
        """
    return html


def _format_tags(items: list) -> str:
    """Format items as colored tags"""
    if not items:
        return "<p>No information available.</p>"
    
    return "".join([f'<span class="tag">{item}</span>' for item in items])


def _format_social_media(social: dict) -> str:
    """Format social media links"""
    if not social or not any(social.values()):
        return "<p>No social media information available.</p>"
    
    html = "<ul style='list-style: none; padding: 0;'>"
    
    platforms = {
        'linkedin': ('LinkedIn', '💼'),
        'twitter': ('Twitter/X', '🐦'),
        'facebook': ('Facebook', '📘')
    }
    
    for key, (name, emoji) in platforms.items():
        url = social.get(key)
        if url:
            html += f'<li style="margin: 10px 0;"><strong>{emoji} {name}:</strong> <a href="{url}" target="_blank">{url}</a></li>'
    
    html += "</ul>"
    return html