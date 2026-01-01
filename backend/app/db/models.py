"""
SEO Sentinel Database Models
SQLAlchemy ORM models for user management, scans, and reports
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()


class SubscriptionTier(enum.Enum):
    """Subscription tier enumeration"""
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class ScanStatus(enum.Enum):
    """Scan status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class User(Base):
    """User account model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255))
    company_name = Column(String(255))
    hashed_password = Column(String(255), nullable=False)
    
    # Subscription details
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE)
    subscription_status = Column(String(50), default='trial')  # trial, active, cancelled, expired
    stripe_customer_id = Column(String(255), unique=True, index=True)
    stripe_subscription_id = Column(String(255), unique=True)
    
    # Limits based on tier
    max_websites = Column(Integer, default=1)
    max_pages_per_scan = Column(Integer, default=50)
    scan_frequency = Column(String(50), default='manual')  # manual, weekly, daily
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    trial_ends_at = Column(DateTime(timezone=True))
    
    # Relationships
    websites = relationship("Website", back_populates="user", cascade="all, delete-orphan")
    scans = relationship("Scan", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, tier={self.subscription_tier})>"


class Website(Base):
    """Website model - each user can have multiple websites"""
    __tablename__ = 'websites'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # Website details
    domain = Column(String(255), nullable=False, index=True)
    name = Column(String(255))  # Friendly name
    url = Column(String(500), nullable=False)  # Full URL with protocol
    
    # Monitoring settings
    is_active = Column(Boolean, default=True)
    scan_frequency = Column(String(50), default='weekly')  # manual, weekly, daily
    max_pages = Column(Integer, default=500)
    last_scan_at = Column(DateTime(timezone=True))
    next_scan_at = Column(DateTime(timezone=True))
    
    # Notification settings
    notify_on_errors = Column(Boolean, default=True)
    notification_email = Column(String(255))
    alert_threshold = Column(Integer, default=5)  # Alert if issues exceed this
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="websites")
    scans = relationship("Scan", back_populates="website", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Website(id={self.id}, domain={self.domain})>"


class Scan(Base):
    """Scan model - each website has multiple scan records"""
    __tablename__ = 'scans'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    website_id = Column(Integer, ForeignKey('websites.id', ondelete='CASCADE'), nullable=False)
    
    # Scan execution details
    status = Column(Enum(ScanStatus), default=ScanStatus.PENDING, index=True)
    celery_task_id = Column(String(255), unique=True, index=True)
    
    # Scan statistics
    pages_crawled = Column(Integer, default=0)
    pages_found = Column(Integer, default=0)
    broken_links_count = Column(Integer, default=0)
    missing_alt_text_count = Column(Integer, default=0)
    meta_issues_count = Column(Integer, default=0)
    
    # Timing
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Float)
    
    # Results storage
    report_pdf_path = Column(String(500))
    report_json_path = Column(String(500))
    report_url = Column(String(500))  # Public URL to view report
    
    # Error tracking
    error_message = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="scans")
    website = relationship("Website", back_populates="scans")
    issues = relationship("Issue", back_populates="scan", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Scan(id={self.id}, website_id={self.website_id}, status={self.status})>"


class Issue(Base):
    """Issue model - stores individual SEO issues found during scans"""
    __tablename__ = 'issues'
    
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey('scans.id', ondelete='CASCADE'), nullable=False)
    
    # Issue classification
    issue_type = Column(String(50), nullable=False, index=True)  # broken_link, missing_alt_text, meta_issue
    severity = Column(String(20), default='medium')  # low, medium, high, critical
    
    # Issue details
    page_url = Column(String(1000))
    page_title = Column(String(500))
    
    # For broken links
    broken_url = Column(String(1000))
    status_code = Column(Integer)
    referenced_from = Column(String(1000))
    
    # For missing alt text
    image_url = Column(String(1000))
    image_filename = Column(String(500))
    suggested_alt_text = Column(Text)  # AI-generated suggestion
    
    # For meta issues
    meta_issue_description = Column(Text)
    
    # Resolution tracking
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime(timezone=True))
    resolution_note = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    scan = relationship("Scan", back_populates="issues")
    
    def __repr__(self):
        return f"<Issue(id={self.id}, type={self.issue_type}, severity={self.severity})>"


class ApiKey(Base):
    """API Key model for programmatic access"""
    __tablename__ = 'api_keys'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # Key details
    key = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255))  # Human-readable name
    
    # Permissions
    is_active = Column(Boolean, default=True)
    can_create_scans = Column(Boolean, default=True)
    can_view_reports = Column(Boolean, default=True)
    
    # Usage tracking
    last_used_at = Column(DateTime(timezone=True))
    usage_count = Column(Integer, default=0)
    
    # Rate limiting
    rate_limit = Column(Integer, default=100)  # Requests per hour
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<ApiKey(id={self.id}, name={self.name}, active={self.is_active})>"


class Payment(Base):
    """Payment history model"""
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # Stripe details
    stripe_payment_id = Column(String(255), unique=True, index=True)
    stripe_invoice_id = Column(String(255))
    
    # Payment details
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default='USD')
    status = Column(String(50))  # succeeded, failed, pending, refunded
    
    # Plan details
    plan_name = Column(String(100))
    billing_period_start = Column(DateTime(timezone=True))
    billing_period_end = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Payment(id={self.id}, amount={self.amount}, status={self.status})>"


class EmailLog(Base):
    """Email log for tracking sent emails"""
    __tablename__ = 'email_logs'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    scan_id = Column(Integer, ForeignKey('scans.id', ondelete='SET NULL'))
    
    # Email details
    recipient = Column(String(255), nullable=False)
    subject = Column(String(500))
    email_type = Column(String(50))  # report, alert, welcome, password_reset
    
    # Delivery status
    status = Column(String(50))  # sent, failed, bounced
    provider_message_id = Column(String(255))
    error_message = Column(Text)
    
    # Timestamps
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<EmailLog(id={self.id}, recipient={self.recipient}, type={self.email_type})>"