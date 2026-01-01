"""
SEO Sentinel - Complete Integration Script
Run a full SEO audit and generate a PDF report in one command
"""

import subprocess
import sys
import os
from datetime import datetime
from app.reports.pdf_generator import SEOReportGenerator


class SEOSentinel:
    """Orchestrates the complete SEO audit workflow"""
    
    def __init__(self, domain, max_pages=500):
        self.domain = domain.replace('https://', '').replace('http://', '').strip('/')
        self.max_pages = max_pages
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.json_file = f'seo_report_{self.domain.replace(".", "_")}.json'
        self.pdf_file = f'seo_report_{self.domain.replace(".", "_")}_{self.timestamp}.pdf'
    
    def run_crawler(self):
        """Execute the Scrapy spider"""
        print(f"\n🕷️  Starting SEO crawl for: {self.domain}")
        print(f"📊 Max pages: {self.max_pages}")
        print("-" * 60)
        
        cmd = [
            'scrapy', 'runspider', 'seo_spider.py',
            '-a', f'domain={self.domain}',
            '-a', f'max_pages={self.max_pages}',
            '--nolog'  # Suppress Scrapy logs for cleaner output
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(result.stdout)
            print("✅ Crawl completed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Crawler failed: {e}")
            print(e.stderr)
            return False
    
    def generate_pdf(self):
        """Generate the PDF report"""
        print(f"\n📄 Generating PDF report...")
        print("-" * 60)
        
        if not os.path.exists(self.json_file):
            print(f"❌ JSON file not found: {self.json_file}")
            return False
        
        try:
            generator = SEOReportGenerator(self.json_file, self.pdf_file)
            generator.generate()
            print(f"✅ PDF report saved: {self.pdf_file}")
            return True
        except Exception as e:
            print(f"❌ PDF generation failed: {e}")
            return False
    
    def cleanup(self, keep_json=False):
        """Clean up temporary files"""
        if not keep_json and os.path.exists(self.json_file):
            os.remove(self.json_file)
            print(f"🗑️  Cleaned up: {self.json_file}")
    
    def run(self, cleanup_json=False):
        """Execute the complete workflow"""
        print("\n" + "=" * 60)
        print("🎯 SEO SENTINEL - Automated Website Health Check")
        print("=" * 60)
        
        # Step 1: Crawl the site
        if not self.run_crawler():
            return False
        
        # Step 2: Generate PDF
        if not self.generate_pdf():
            return False
        
        # Step 3: Cleanup
        if cleanup_json:
            self.cleanup(keep_json=False)
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ AUDIT COMPLETE!")
        print("=" * 60)
        print(f"📧 Email this report to your client: {self.pdf_file}")
        print(f"💰 Upsell opportunity: Automated weekly monitoring")
        print("=" * 60 + "\n")
        
        return True


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("\n🚀 SEO Sentinel - Usage:")
        print("-" * 60)
        print("python seo_sentinel.py <domain> [max_pages]")
        print("\nExamples:")
        print("  python seo_sentinel.py example.com")
        print("  python seo_sentinel.py shopify-store.com 1000")
        print("-" * 60 + "\n")
        sys.exit(1)
    
    domain = sys.argv[1]
    max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    
    sentinel = SEOSentinel(domain, max_pages)
    success = sentinel.run(cleanup_json=True)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()