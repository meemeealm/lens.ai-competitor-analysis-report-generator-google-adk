"""
Data schemas and HTML templates for competitor analysis
"""

# JSON Schema for competitor analysis data
COMPETITOR_ANALYSIS_SCHEMA = {
    "company_name": "string",
    "website": "string",
    "analysis_date": "string (ISO format: YYYY-MM-DD)",
    "overview": {
        "description": "string - brief company description",
        "founded_year": "integer or null - year company was founded",
        "headquarters": "string or null - location of headquarters",
        "size": "string or null - number of employees"
    },
    "products_services": [
        {
            "name": "string - product/service name",
            "description": "string - what it does",
            "category": "string - product category"
        }
    ],
    "market_position": {
        "target_market": "string - primary market segment",
        "market_share": "string or null - market share percentage if available",
        "key_competitors": ["string - competitor names"]
    },
    "strengths": ["string - competitive advantages"],
    "weaknesses": ["string - competitive disadvantages"],
    "recent_news": [
        {
            "title": "string - news headline",
            "date": "string - ISO format date",
            "summary": "string - brief summary",
            "source": "string - news source"
        }
    ],
    "pricing_model": "string or null - pricing strategy",
    "technology_stack": ["string - technologies used"],
    "social_media_presence": {
        "linkedin": "string or null - LinkedIn URL",
        "twitter": "string or null - Twitter/X URL",
        "facebook": "string or null - Facebook URL"
    }
}

# HTML Template for report generation
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Competitor Analysis - {company_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            line-height: 1.6; 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px; 
            background-color: #f5f5f5; 
        }}
        .header {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 40px 30px; 
            border-radius: 10px; 
            margin-bottom: 30px; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header h2 {{ font-size: 1.8em; margin: 15px 0; border: none; color: white; }}
        .header a {{ color: white; text-decoration: underline; }}
        .section {{ 
            background: white; 
            padding: 30px; 
            margin-bottom: 20px; 
            border-radius: 8px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
        }}
        h2 {{ 
            color: #667eea; 
            border-bottom: 3px solid #667eea; 
            padding-bottom: 10px; 
            margin-bottom: 20px;
        }}
        h3 {{ color: #764ba2; margin: 20px 0 10px 0; }}
        .grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
            gap: 20px; 
            margin: 20px 0;
        }}
        .card {{ 
            background: #f8f9fa; 
            padding: 20px; 
            border-radius: 8px; 
            border-left: 4px solid #667eea; 
            transition: transform 0.2s;
        }}
        .card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        .tag {{ 
            display: inline-block; 
            background: #667eea; 
            color: white; 
            padding: 6px 12px; 
            border-radius: 20px; 
            margin: 5px; 
            font-size: 0.9em; 
        }}
        .list-item {{ 
            background: #f8f9fa; 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 5px; 
            border-left: 4px solid #28a745;
        }}
        .weakness {{ border-left-color: #dc3545; }}
        .news-item {{ 
            background: #fff9e6; 
            border-left: 4px solid #ffc107; 
            padding: 20px; 
            margin: 15px 0; 
            border-radius: 5px; 
        }}
        .news-item h3 {{ margin-top: 0; }}
        .meta {{ opacity: 0.9; font-size: 0.95em; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Competitor Analysis Report</h1>
        <h2>{company_name}</h2>
        <div class="meta">
            <p><strong>Website:</strong> <a href="{website}" target="_blank">{website}</a></p>
            <p><strong>Analysis Date:</strong> {analysis_date}</p>
        </div>
    </div>

    <div class="section">
        <h2>📋 Company Overview</h2>
        <p><strong>Description:</strong> {description}</p>
        <div class="grid">
            <div class="card">
                <h3>🏢 Founded</h3>
                <p>{founded_year}</p>
            </div>
            <div class="card">
                <h3>📍 Headquarters</h3>
                <p>{headquarters}</p>
            </div>
            <div class="card">
                <h3>👥 Company Size</h3>
                <p>{size}</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>🛍️ Products & Services</h2>
        {products_html}
    </div>

    <div class="section">
        <h2>📊 Market Position</h2>
        <p><strong>Target Market:</strong> {target_market}</p>
        <p><strong>Market Share:</strong> {market_share}</p>
        <h3>Key Competitors</h3>
        <div>
            {competitors_html}
        </div>
    </div>

    <div class="section">
        <h2>⚡ SWOT Analysis</h2>
        <div class="grid">
            <div>
                <h3>💪 Strengths</h3>
                {strengths_html}
            </div>
            <div>
                <h3>⚠️ Weaknesses</h3>
                {weaknesses_html}
            </div>
        </div>
    </div>

    <div class="section">
        <h2>📰 Recent News & Updates</h2>
        {news_html}
    </div>

    <div class="section">
        <h2>💻 Technology & Pricing</h2>
        <p><strong>Pricing Model:</strong> {pricing_model}</p>
        <h3>Technology Stack</h3>
        <div>
            {tech_html}
        </div>
    </div>

    <div class="section">
        <h2>🌐 Social Media Presence</h2>
        {social_html}
    </div>
</body>
</html>
"""