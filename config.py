import os
from datetime import timedelta

import boto3


class Config:
    """Application configuration class"""

    # Base configuration
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    # AWS Configuration - use environment variables only
    AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
    AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")  # S3 Configuration
    S3_VECTOR_BUCKET = os.environ.get("S3_VECTOR_BUCKET", "gigfusion-vector-db")
    S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "gigfusion-files")

    # RDS MySQL Configuration (Optimized Setup)
    RDS_ENDPOINT = os.environ.get(
        "RDS_ENDPOINT", "gigfusion-mysql.ca5u6i2g6bg0.us-east-1.rds.amazonaws.com"
    )
    RDS_USERNAME = os.environ.get("RDS_USERNAME", "admin")
    RDS_PASSWORD = os.environ.get("RDS_PASSWORD")  # Must be set in environment
    RDS_DATABASE = os.environ.get("RDS_DATABASE", "gigfusion")
    RDS_PORT = int(os.environ.get("RDS_PORT", "3306"))

    # Gemini AI Configuration
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")  # Must be set in environment

    # S3 Prefixes within S3_BUCKET_NAME
    PROFILES_S3_PREFIX = "profiles/"
    POSTS_S3_PREFIX = "posts/"
    PROFILE_IMAGES_S3_PREFIX = "profile_images/"  # Added for profile pictures
    PROJECT_FILES_S3_PREFIX = "project_files/"  # Added for project attachments
    MESSAGES_S3_PREFIX = "messages/"  # Added for messages
    USERS_S3_PREFIX = "users/"  # Added for users
    BIDS_S3_PREFIX = "bids/"  # Added for bids
    NOTIFICATIONS_S3_PREFIX = "notifications/"  # Added for notifications
    # Added for freelancer reviews
    FREELANCER_REVIEWS_S3_PREFIX = "freelancer_reviews/"
    # Example: USER_DATA_S3_PREFIX = "user_data/"

    # Note: The following older S3 path configurations are being deprecated.
    # Use S3_BUCKET_NAME with specific prefixes (e.g., PROFILES_S3_PREFIX)
    # and S3_VECTOR_BUCKET for vector-related data.
    # S3_GENERAL_BUCKET = os.environ.get(
    #     "S3_GENERAL_BUCKET", "gigfusion-db") # DEPRECATED
    # S3_DATA_FOLDER = "app_data/"  # DEPRECATED
    # S3_UPLOAD_FOLDER = "uploads/"  # DEPRECATED
    # S3_PROFILE_IMAGES = "profile_images/" # DEPRECATED
    # S3_PROJECT_FILES = "project_files/" # DEPRECATED    # EC2 specific configurations
    # Force EC2 deployment mode
    EC2_DEPLOYMENT = True
    EC2_MEMORY_EFFICIENT = True  # Always use memory optimizations    # Memory threshold for optimization (200MB by default)
    EC2_MEMORY_THRESHOLD = 200 * 1024 * 1024
    # EC2 API URL - Updated to match correct port (5000) on server
    EC2_API_URL = "http://ec2-54-221-34-34.compute-1.amazonaws.com:5000"

    # Local mode - when True, disables EC2 API dependency and uses local fallbacks
    LOCAL_MODE = os.environ.get("LOCAL_MODE", "True").lower() == "true"

    # FAISS index configuration
    FAISS_INDEX_DIMENSION = 384  # For MiniLM-L6-v2 model
    FAISS_INDEX_TYPE = "Flat"  # Using simple flat index for t2.micro

    # Memory optimization for t2.micro
    BATCH_SIZE = 32
    MAX_VECTORS_IN_MEMORY = 1000

    # FAISS configuration
    # Use smaller model on EC2 to save memory
    EMBEDDING_MODEL = (
        "sentence-transformers/all-MiniLM-L6-v2"
        if EC2_DEPLOYMENT
        else "sentence-transformers/all-mpnet-base-v2"
    )

    # For production systems using an async task queue for embeddings
    USE_ASYNC_PROCESSING = (
        os.environ.get("USE_ASYNC_PROCESSING", "False").lower() == "true"
    )

    # Initialize S3 client
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
    )

    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # File upload configuration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max upload
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "doc", "docx"}

    # ML model path
    MODEL_PATH = os.path.join(BASE_DIR, "models")


class TestConfig(Config):
    """Testing configuration"""

    TESTING = True
    WTF_CSRF_ENABLED = False
    S3_VECTOR_BUCKET = "test-vector-bucket"
    S3_GENERAL_BUCKET = "test-general-bucket"


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # Default to memory efficient mode in production
    EC2_MEMORY_EFFICIENT = True

    # Security settings
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
