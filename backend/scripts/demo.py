"""
SEO Sentinel - Demo & Testing Script
Run this to test the complete workflow with sample data
"""

import json
import os
from datetime import datetime
from pdf_generator import SEOReportGenerator


def create_sample_data(domain="demo-store.com"):
    """Generate sample crawl data for testing PDF generation"""
    
    sample_data = {
        "domain": domain,
        "stats": {
            "pages_crawled": 127,
            "broken_links": 8,
            "missing_alt_text": 23,
            "start_time": "2026-01-01T14:30:00",
            "end_time": "2026-01-01T14:35:22",
            "status": "completed"
        },
        "issues": {
            "broken_links": [
                {
                    "type": "broken_link",
                    "url": "https://demo-store.com/products/old-product-123",
                    "status": 404,
                    "referenced_from": "https://demo-store.com/categories/electronics",
                    "timestamp": "2026-01-01T14:31:15"
                },
                {
                    "type": "broken_link",
                    "url": "https://demo-store.com/blog/removed-post",
                    "status": 404,
                    "referenced_from": "https://demo-store.com/blog",
                    "timestamp": "2026-01-01T14:32:45"
                },
                {
                    "type": "broken_link",
                    "url": "https://demo-store.com/assets/old-banner.jpg",
                    "status": 404,
                    "referenced_from": "https://demo-store.com/",
                    "timestamp": "2026-01-01T14:30:22"
                },
                {
                    "type": "broken_link",
                    "url": "https://demo-store.com/sale/black-friday-2024",
                    "status": 404,
                    "referenced_from": "https://demo-store.com/promotions",
                    "timestamp": "2026-01-01T14:33:10"
                },
                {
                    "type": "broken_link",
                    "url": "https://demo-store.com/api/v1/deprecated",
                    "status": 500,
                    "referenced_from": "https://demo-store.com/checkout",
                    "timestamp": "2026-01-01T14:34:55"
                },
                {
                    "type": "broken_link",
                    "url": "https://demo-store.com/partners/old-partner",
                    "status": 404,
                    "referenced_from": "https://demo-store.com/partners",
                    "timestamp": "2026-01-01T14:31:40"
                },
                {
                    "type": "broken_link",
                    "url": "https://demo-store.com/downloads/brochure-2023.pdf",
                    "status": 404,
                    "referenced_from": "https://demo-store.com/resources",
                    "timestamp": "2026-01-01T14:32:20"
                },
                {
                    "type": "broken_link",
                    "url": "https://demo-store.com/careers/closed-position",
                    "status": 404,
                    "referenced_from": "https://demo-store.com/careers",
                    "timestamp": "2026-01-01T14:35:05"
                }
            ],
            "missing_alt_text": [
                {
                    "type": "missing_alt_text",
                    "page_url": "https://demo-store.com/products/wireless-headphones",
                    "page_title": "Premium Wireless Headphones - Best Deals",
                    "img_src": "https://demo-store.com/images/headphones-main.jpg",
                    "img_filename": "headphones-main.jpg"
                },
                {
                    "type": "missing_alt_text",
                    "page_url": "https://demo-store.com/products/laptop-stand",
                    "page_title": "Ergonomic Laptop Stand - Free Shipping",
                    "img_src": "https://demo-store.com/images/laptop-stand-1.jpg",
                    "img_filename": "laptop-stand-1.jpg"
                },
                {
                    "type": "missing_alt_text",
                    "page_url": "https://demo-store.com/",
                    "page_title": "Demo Store - Quality Products Online",
                    "img_src": "https://demo-store.com/images/hero-banner.jpg",
                    "img_filename": "hero-banner.jpg"
                },
                {
                    "type": "missing_alt_text",
                    "page_url": "https://demo-store.com/categories/electronics",
                    "page_title": "Electronics - Demo Store",
                    "img_src": "https://demo-store.com/images/category-electronics.jpg",
                    "img_filename": "category-electronics.jpg"
                },
                {
                    "type": "missing_alt_text",
                    "page_url": "https://demo-store.com/products/mechanical-keyboard",
                    "page_title": "RGB Mechanical Keyboard - Gaming",
                    "img_src": "https://demo-store.com/images/keyboard-rgb.jpg",
                    "img_filename": "keyboard-rgb.jpg"
                },
                {
                    "type": "missing_alt_text",
                    "page_url": "https://demo-store.com/products/gaming-mouse",
                    "page_title": "Pro Gaming Mouse - 16000 DPI",
                    "img_src": "https://demo-store.com/images/mouse-gaming.jpg",
                    "img_filename": "mouse-gaming.jpg"
                },
                {
                    "type": "missing_alt_text",
                    "page_url": "https://demo-store.com/blog/tech-trends-2026",
                    "page_title": "Top Tech Trends in 2026 - Blog",
                    "img_src": "https://demo-store.com/images/blog-tech-trends.jpg",
                    "img_filename": "blog-tech-trends.jpg"
                },
                {
                    "type": "missing_alt_text",
                    "page_url": "https://demo-store.com/about",
                    "page_title": "About Us - Demo Store",
                    "img_src": "https://demo-store.com/images/team-photo.jpg",
                    "img_filename": "team-photo.jpg"
                },
                {
                    "type": "missing_alt_text",
                    "page_url": "https://demo-store.com/products/usb-hub",
                    "page_title": "7-Port USB Hub - High Speed",
                    "img_src": "https://demo-store.com/images/usb-hub.jpg",
                    "img_filename": "usb-hub.jpg"
                },
                {
                    "type": "missing_alt_text",
                    "page_url": "https://demo-store.com/products/webcam-4k",
                    "page_title": "4K Ultra HD Webcam - Video Calls",
                    "img_src": "https://demo-store.com/images/webcam-4k.jpg",
                    "img_filename": "webcam-4k.jpg"
                },
                # Add more examples...
                *[{
                    "type": "missing_alt_text",
                    "page_url": f"https://demo-store.com/products/product-{i}",
                    "page_title": f"Product {i} - Demo Store",
                    "img_src": f"https://demo-store.com/images/product-{i}.jpg",
                    "img_filename": f"product-{i}.jpg"
                } for i in range(11, 24)]
            ],
            "meta_issues": [
                {
                    "type": "meta_issues",
                    "page_url": "https://demo-store.com/contact",
                    "issues": ["Missing meta description"]
                },
                {
                    "type": "meta_issues",
                    "page_url": "https://demo-store.com/privacy",
                    "issues": ["Missing or too short page title"]
                }
            ]
        }
    }
    
    return sample_data


def run_demo():
    """Run a complete demo of the SEO Sentinel workflow"""
    
    print("\n" + "=" * 70)
    print("🎬 SEO SENTINEL - DEMO MODE")
    print("=" * 70)
    print("\nThis demo will:")
    print("  1. Create sample crawl data (simulating a real website scan)")
    print("  2. Generate a professional PDF report")
    print("  3. Show you what clients will receive")
    print("\n" + "-" * 70)
    
    # Step 1: Create sample data
    print("\n📊 Creating sample data for demo-store.com...")
    sample_data = create_sample_data()
    
    json_filename = "demo_seo_report.json"
    with open(json_filename, 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    print(f"✅ Sample data created: {json_filename}")
    print(f"   - Pages crawled: {sample_data['stats']['pages_crawled']}")
    print(f"   - Broken links found: {sample_data['stats']['broken_links']}")
    print(f"   - Missing alt text: {sample_data['stats']['missing_alt_text']}")
    
    # Step 2: Generate PDF
    print("\n📄 Generating PDF report...")
    pdf_filename = f"demo_seo_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    try:
        generator = SEOReportGenerator(json_filename, pdf_filename)
        generator.generate()
        print(f"✅ PDF generated successfully: {pdf_filename}")
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return
    
    # Step 3: Show summary
    print("\n" + "=" * 70)
    print("✅ DEMO COMPLETE!")
    print("=" * 70)
    print(f"\n📧 What clients see:")
    print(f"   → Professional PDF report: {pdf_filename}")
    print(f"   → Clear issue breakdown")
    print(f"   → Actionable recommendations")
    print(f"   → Call-to-action for paid monitoring")
    
    print("\n💰 Monetization Strategy:")
    print("   → Send this as a FREE audit to prospects")
    print("   → Show first 5 issues for free")
    print("   → Charge $29/month for full access + weekly monitoring")
    print("   → Upsell to $79/month for 5 sites + AI features")
    
    print("\n📈 Math to $100/day:")
    print("   → 40 customers × $29/mo = $1,160/mo (~$40/day)")
    print("   → 10 customers × $79/mo = $790/mo (~$26/day)")
    print("   → Total: $1,950/mo (~$65/day)")
    print("   → Add 20 more tier-1 = $100+/day 🎯")
    
    print("\n🚀 Next Steps:")
    print("   1. Open the PDF: " + pdf_filename)
    print("   2. Customize branding in config.py")
    print("   3. Test on a real website:")
    print("      python seo_sentinel.py yourwebsite.com")
    print("   4. Build the FastAPI backend")
    print("   5. Add Celery for scheduling")
    print("   6. Launch landing page")
    
    print("\n" + "=" * 70)
    print("🎓 You now have a working MVP worth $50-100/day!")
    print("=" * 70 + "\n")


def test_specific_domain(domain):
    """Test the system with a specific domain (requires live crawling)"""
    print(f"\n🧪 Testing with real domain: {domain}")
    print("-" * 70)
    
    from seo_sentinel import SEOSentinel
    
    sentinel = SEOSentinel(domain, max_pages=50)
    success = sentinel.run(cleanup_json=False)
    
    if success:
        print(f"\n✅ Test successful! Check the generated PDF.")
    else:
        print(f"\n❌ Test failed. Check the logs above.")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Test with real domain
        domain = sys.argv[2] if len(sys.argv) > 2 else 'example.com'
        test_specific_domain(domain)
    else:
        # Run demo with sample data
        run_demo()