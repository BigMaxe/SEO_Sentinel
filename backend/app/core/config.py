"""
SEO Sentinel ConfigurationCentralized Settings for easy customization
"""

import os
from pathlib import Path


class Config:
    """Main configuration class"""
    
    #Project Paths
    BASE_DIR = Path(__file__).parent
    REPORTS_DIR = BASE_DIR / 'reports'
    LOGS_DIR = BASE_DIR / 'logs'
    
    # Crawler settings
    CRAWLER = {
        'download_delay': 0.5,
        'concurrent_requests': 16,
        'concurrent_requests_per_domain': 8,
        'depth_limit': 3,
        'max_pages_default': 500,
        'timeout': 180,  # seconds
        'user_agent': 'SEO-Sentinel-Bot/1.0 (+https://seositinel.com/bot)',
        'obey_robots_txt': True,
    }
    
    # PDF Branding
    BRANDING = {
        'company_name': 'SEO Sentinel',
        'company_url': 'www.seositinel.com',
        'support_email': 'support@seositinel.com',
        'logo_path': None,  # Path to logo image (optional)
        'primary_color': '#1e40af',
        'secondary_color': '#3b82f6',
        'danger_color': '#dc2626',
        'warning_color': '#f59e0b',
        'success_color': '#16a34a',
    }
    
    # Report settings
    REPORT = {
        'max_broken_links_display': 20,
        'max_alt_text_issues_display': 25,
        'include_meta_issues': True,
        'include_recommendations': True,
    }
    
    # Email settings (for future integration)
    EMAIL = {
        'provider': 'sendgrid',  # or 'smtp', 'mailgun'
        'api_key': os.getenv('SENDGRID_API_KEY', ''),
        'from_email': 'reports@seositinel.com',
        'from_name': 'SEO Sentinel',
        'reply_to': 'support@seositinel.com',
    }
    
    # Pricing tiers
    PRICING = {
        'tier1': {
            'name': 'Starter',
            'price': 29,
            'max_sites': 1,
            'max_pages_per_site': 500,
            'scan_frequency': 'weekly',
            'features': [
                'Weekly automated scans',
                'Email PDF reports',
                'Up to 500 pages',
                'Basic support'
            ]
        },
        'tier2': {
            'name': 'Professional',
            'price': 79,
            'max_sites': 5,
            'max_pages_per_site': 1000,
            'scan_frequency': 'daily',
            'features': [
                'Daily automated scans',
                'Up to 5 websites',
                'Up to 1000 pages per site',
                'AI alt-text suggestions',
                'Priority support',
                'API access'
            ]
        },
        'enterprise': {
            'name': 'Enterprise',
            'price': 299,
            'max_sites': 'unlimited',
            'max_pages_per_site': 'unlimited',
            'scan_frequency': 'custom',
            'features': [
                'Unlimited websites',
                'Unlimited pages',
                'Custom scan frequency',
                'White-label reports',
                'Dedicated account manager',
                'SLA guarantee'
            ]
        }
    }
    
    # Notification thresholds
    ALERTS = {
        'broken_links_critical': 10,
        'broken_links_warning': 5,
        'missing_alt_text_critical': 50,
        'missing_alt_text_warning': 20,
    }
    
    # API settings (for future FastAPI integration)
    API = {
        'host': '0.0.0.0',
        'port': 8000,
        'debug': False,
        'cors_origins': ['http://localhost:3000', 'https://seositinel.com'],
        'rate_limit': '100/hour',
    }
    
    # Database (for future use)
    DATABASE = {
        'url': os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/seo_sentinel'),
        'pool_size': 10,
        'echo': False,
    }
    
    # Redis (for Celery task queue)
    REDIS = {
        'url': os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
        'max_connections': 50,
    }
    
    # Celery settings
    CELERY = {
        'broker_url': REDIS['url'],
        'result_backend': REDIS['url'],
        'task_serializer': 'json',
        'accept_content': ['json'],
        'timezone': 'UTC',
        'task_routes': {
            'tasks.crawl_website': {'queue': 'crawls'},
            'tasks.generate_report': {'queue': 'reports'},
            'tasks.send_email': {'queue': 'emails'},
        }
    }
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.REPORTS_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def get_alert_level(cls, issue_type, count):
        """Determine alert level based on issue count"""
        if issue_type == 'broken_links':
            if count >= cls.ALERTS['broken_links_critical']:
                return 'critical'
            elif count >= cls.ALERTS['broken_links_warning']:
                return 'warning'
        elif issue_type == 'missing_alt_text':
            if count >= cls.ALERTS['missing_alt_text_critical']:
                return 'critical'
            elif count >= cls.ALERTS['missing_alt_text_warning']:
                return 'warning'
        return 'ok'


class DevelopmentConfig(Config):
    """Development environment configuration"""
    API = {
        **Config.API,
        'debug': True,
    }
    CRAWLER = {
        **Config.CRAWLER,
        'max_pages_default': 50,  # Limit for testing
        'depth_limit': 2,
    }


class ProductionConfig(Config):
    """Production environment configuration"""
    API = {
        **Config.API,
        'debug': False,
    }
    CRAWLER = {
        **Config.CRAWLER,
        'download_delay': 1.0,  # More polite in production
    }


# Environment selector
def get_config():
    """Get configuration based on environment"""
    env = os.getenv('ENVIRONMENT', 'development')
    
    if env == 'production':
        return ProductionConfig
    else:
        return DevelopmentConfig


# Usage
config = get_config()
config.create_directories()
