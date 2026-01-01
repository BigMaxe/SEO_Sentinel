"""
SEO Sentinel Spider - Production-Ready Web Crawler
Detects broken links and missing alt-text for e-commerce sites
"""

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urljoin, urlparse
import json
from datetime import datetime


class SEOSentinelSpider(CrawlSpider):
    name = 'seo_sentinel'
    
    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,  # Be polite to the server
        'CONCURRENT_REQUESTS': 16,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'SEO-Sentinel-Bot/1.0 (+https://seositinel.com/bot)',
        'DEPTH_LIMIT': 3,  # Don't go too deep on first scan
        'CLOSESPIDER_PAGECOUNT': 500,  # Max pages per scan
    }
    
    def __init__(self, domain='', max_pages=500, *args, **kwargs):
        super(SEOSentinelSpider, self).__init__(*args, **kwargs)
        
        # Clean domain input
        domain = domain.replace('https://', '').replace('http://', '').strip('/')
        
        self.allowed_domains = [domain]
        self.start_urls = [f'https://{domain}']
        self.domain = domain
        self.max_pages = int(max_pages)
        
        # Statistics
        self.stats = {
            'pages_crawled': 0,
            'broken_links': 0,
            'missing_alt_text': 0,
            'start_time': datetime.now().isoformat()
        }
        
        # Store issues
        self.issues = {
            'broken_links': [],
            'missing_alt_text': [],
            'meta_issues': []
        }

    rules = (
        Rule(
            LinkExtractor(
                allow_domains=None,  # Will be set dynamically
                deny_extensions=['pdf', 'zip', 'exe', 'dmg', 'mp4', 'avi']
            ),
            callback='parse_item',
            follow=True
        ),
    )

    handle_httpstatus_list = [404, 403, 500, 502, 503, 504]

    def parse_item(self, response):
        self.stats['pages_crawled'] += 1
        
        # 1. CHECK FOR BROKEN LINKS
        if response.status >= 400:
            self.stats['broken_links'] += 1
            referer = response.request.headers.get('Referer', b'').decode('utf-8')
            
            issue = {
                'type': 'broken_link',
                'url': response.url,
                'status': response.status,
                'referenced_from': referer or 'Direct',
                'timestamp': datetime.now().isoformat()
            }
            
            self.issues['broken_links'].append(issue)
            yield issue
            return

        # 2. CHECK FOR MISSING ALT TEXT
        images = response.css('img')
        for img in images:
            alt = img.xpath('@alt').get()
            src = img.xpath('@src').get()
            
            if not src:
                continue
                
            # Make absolute URL
            img_url = urljoin(response.url, src)
            
            if alt is None or alt.strip() == "":
                self.stats['missing_alt_text'] += 1
                
                issue = {
                    'type': 'missing_alt_text',
                    'page_url': response.url,
                    'page_title': response.css('title::text').get() or 'No Title',
                    'img_src': img_url,
                    'img_filename': src.split('/')[-1] if src else 'unknown'
                }
                
                self.issues['missing_alt_text'].append(issue)
                yield issue

        # 3. CHECK META TAGS (SEO fundamentals)
        meta_issues = []
        
        # Missing title
        title = response.css('title::text').get()
        if not title or len(title.strip()) < 10:
            meta_issues.append('Missing or too short page title')
        
        # Missing meta description
        meta_desc = response.css('meta[name="description"]::attr(content)').get()
        if not meta_desc:
            meta_issues.append('Missing meta description')
        
        if meta_issues:
            issue = {
                'type': 'meta_issues',
                'page_url': response.url,
                'issues': meta_issues
            }
            self.issues['meta_issues'].append(issue)
            yield issue

    def closed(self, reason):
        """Called when spider finishes - save summary"""
        self.stats['end_time'] = datetime.now().isoformat()
        self.stats['status'] = 'completed'
        
        # Save to JSON file
        output_data = {
            'domain': self.domain,
            'stats': self.stats,
            'issues': self.issues
        }
        
        filename = f'seo_report_{self.domain.replace(".", "_")}.json'
        with open(filename, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        self.logger.info(f'✅ Crawl completed: {self.stats["pages_crawled"]} pages')
        self.logger.info(f'🔴 Found {self.stats["broken_links"]} broken links')
        self.logger.info(f'🖼️  Found {self.stats["missing_alt_text"]} images without alt text')
        self.logger.info(f'📄 Report saved to: {filename}')