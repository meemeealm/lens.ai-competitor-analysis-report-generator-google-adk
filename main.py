import os
import sys
from pathlib import Path

# Environment setup
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")

if PROJECT_ID == "your-project-id" or not PROJECT_ID:
    print("❌ Error: GOOGLE_CLOUD_PROJECT not set")
    print("\nPlease set your Google Cloud Project ID:")
    print("  export GOOGLE_CLOUD_PROJECT='your-actual-project-id'")
    print("  export GOOGLE_API_KEY='your-api-key'")
    sys.exit(1)

os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "0"

print(f"✅ Project ID: {PROJECT_ID}")
print(f"✅ Environment configured\n")

# Import pipelines
from pipelines import OptimizedCompetitorAnalysisPipeline, BatchOptimizedPipeline


# ===================================================================
# USAGE EXAMPLES
# ===================================================================

def example_single_analysis():
    """Example: Analyze a single competitor"""
    print("="*70)
    print("EXAMPLE 1: Single Competitor Analysis")
    print("="*70)
    
    # Initialize pipeline
    pipeline = OptimizedCompetitorAnalysisPipeline()
    
    # Analyze competitor
    report = pipeline.analyze_competitor(
        company_website="https://www.stripe.com",
        company_name="Stripe"
    )
    
    # Save report
    filename = pipeline.save_report(report, "stripe_analysis.html")
    
    print(f"\n✅ Analysis complete!")
    print(f"📄 Open {filename} in your browser to view the report\n")
    
    return report


def example_batch_analysis():
    """Example: Analyze multiple competitors in one batch"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Batch Competitor Analysis (Maximum Cost Savings)")
    print("="*70)
    
    # Initialize batch pipeline
    batch_pipeline = BatchOptimizedPipeline()
    
    # Define competitors to analyze
    competitors = [
        ("https://www.stripe.com", "Stripe"),
        ("https://www.square.com", "Square"),
        ("https://www.paypal.com", "PayPal"),
    ]
    
    # Run batch analysis (SINGLE LLM CALL for all!)
    batch_reports = batch_pipeline.analyze_multiple_competitors(competitors)
    
    # Save all reports
    print("\n📁 Saving reports...")
    for company_name, html in batch_reports.items():
        filename = f"{company_name.lower().replace(' ', '_')}_analysis.html"
        batch_pipeline.save_report(html, filename)
    
    print(f"\n✅ Batch analysis complete!")
    print(f"📊 Generated {len(batch_reports)} reports")
    print(f"💰 Cost: 1 LLM call (vs {len(competitors)} individual calls)")
    print(f"💵 Savings: ~{90 - (100 // len(competitors))}%\n")
    
    return batch_reports


def example_from_file():
    """Example: Batch analysis from a file"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Batch Analysis from File")
    print("="*70)
    
    # Create sample file if it doesn't exist
    sample_file = "competitors.txt"
    if not Path(sample_file).exists():
        print(f"\n📝 Creating sample file: {sample_file}")
        with open(sample_file, 'w') as f:
            f.write("""# Payment Processing Competitors
https://www.stripe.com,Stripe
https://www.square.com,Square
https://www.paypal.com,PayPal

# E-commerce Platforms
https://www.shopify.com,Shopify
https://www.woocommerce.com,WooCommerce
""")
        print(f"✅ Created {sample_file}")
    
    # Read competitors from file
    competitors = []
    with open(sample_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split(',')
                url = parts[0].strip()
                name = parts[1].strip() if len(parts) > 1 else None
                competitors.append((url, name))
    
    print(f"\n📋 Found {len(competitors)} companies in {sample_file}")
    
    # Analyze
    batch_pipeline = BatchOptimizedPipeline()
    batch_reports = batch_pipeline.analyze_multiple_competitors(competitors)
    
    # Save reports
    for company_name, html in batch_reports.items():
        filename = f"{company_name.lower().replace(' ', '_')}_analysis.html"
        batch_pipeline.save_report(html, filename)
    
    print(f"\n✅ All reports generated from file!")
    
    return batch_reports


def interactive_mode():
    """Interactive mode: Let user choose what to analyze"""
    print("\n" + "="*70)
    print("🔍 INTERACTIVE COMPETITOR ANALYSIS")
    print("="*70)
    
    print("\nSelect mode:")
    print("  1. Analyze single competitor")
    print("  2. Batch analysis (multiple competitors)")
    print("  3. Batch from file")
    print("  4. Run all examples")
    print("  5. Exit")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == "1":
        url = input("\nEnter company website URL: ").strip()
        name = input("Enter company name (optional): ").strip() or None
        
        pipeline = OptimizedCompetitorAnalysisPipeline()
        report = pipeline.analyze_competitor(url, name)
        filename = pipeline.save_report(report)
        
        print(f"\n✅ Report saved: {filename}")
    
    elif choice == "2":
        print("\nEnter competitors (format: url,name)")
        print("Press Enter twice when done:")
        
        competitors = []
        while True:
            line = input().strip()
            if not line:
                break
            parts = line.split(',')
            url = parts[0].strip()
            name = parts[1].strip() if len(parts) > 1 else None
            competitors.append((url, name))
        
        if competitors:
            batch_pipeline = BatchOptimizedPipeline()
            reports = batch_pipeline.analyze_multiple_competitors(competitors)
            
            for company_name, html in reports.items():
                filename = f"{company_name.replace(' ', '_')}_analysis.html"
                batch_pipeline.save_report(html, filename)
    
    elif choice == "3":
        filename = input("\nEnter file path (default: competitors.txt): ").strip()
        filename = filename or "competitors.txt"
        example_from_file()
    
    elif choice == "4":
        example_single_analysis()
        example_batch_analysis()
        # example_from_file()  # Uncomment if you want to include this
    
    elif choice == "5":
        print("\n👋 Goodbye!")
        sys.exit(0)
    
    else:
        print("\n❌ Invalid choice!")


# ===================================================================
# MAIN EXECUTION
# ===================================================================

def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("🚀 COMPETITOR ANALYSIS PIPELINE")
    print("Powered by Google ADK & Gemini AI")
    print("="*70)
    
    # Check if running in interactive mode
    if len(sys.argv) > 1:
        if sys.argv[1] == "--interactive" or sys.argv[1] == "-i":
            interactive_mode()
        elif sys.argv[1] == "--batch" or sys.argv[1] == "-b":
            example_batch_analysis()
        elif sys.argv[1] == "--file" or sys.argv[1] == "-f":
            example_from_file()
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print_help()
        else:
            print(f"❌ Unknown option: {sys.argv[1]}")
            print_help()
    else:
        # Default: Run single example
        example_single_analysis()
        
        print("\n💡 TIP: For more options, run:")
        print("  python main.py --help")


def print_help():
    """Print help message"""
    print("""
Usage: python main.py [OPTIONS]

OPTIONS:
    (none)          Run single competitor analysis example
    -i, --interactive    Interactive mode
    -b, --batch         Run batch analysis example
    -f, --file          Run batch from file example
    -h, --help          Show this help message

EXAMPLES:
    # Run default single analysis
    python main.py
    
    # Interactive mode
    python main.py --interactive
    
    # Batch analysis
    python main.py --batch
    
    # Batch from file
    python main.py --file

ENVIRONMENT VARIABLES:
    GOOGLE_CLOUD_PROJECT    Your Google Cloud project ID (required)
    GOOGLE_API_KEY          Your Google API key (required)
    GOOGLE_CLOUD_LOCATION   Region (default: us-central1)

COST OPTIMIZATION:
    ✅ Single analysis: 1 LLM call (saves 67% vs traditional)
    ✅ Batch analysis:  1 LLM call for ALL companies (saves 90%+)
    
For more information, see README.md
    """)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

