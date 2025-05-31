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
    AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

    # S3 Configuration
    S3_VECTOR_BUCKET = os.environ.get("S3_VECTOR_BUCKET", "gigfusion-vector-db")
    S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "gigfusion-files")

    # RDS MySQL Configuration (Optimized Setup)
    RDS_ENDPOINT = os.environ.get(
        "RDS_ENDPOINT", "gigfusion-mysql.ca5u6i2g6bg0.us-east-1.rds.amazonaws.com"
    )
    RDS_USERNAME = os.environ.get("RDS_USERNAME", "admin")
    RDS_PASSWORD = os.environ.get("RDS_PASSWORD")
    RDS_DATABASE = os.environ.get("RDS_DATABASE", "gigfusion")
    RDS_PORT = int(os.environ.get("RDS_PORT", "3306"))

    # Gemini AI Configuration
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    # S3 Prefixes within S3_BUCKET_NAME
    PROFILES_S3_PREFIX = "profiles/"
    POSTS_S3_PREFIX = "posts/"
    PROFILE_IMAGES_S3_PREFIX = "profile_images/"
    PROJECT_FILES_S3_PREFIX = "project_files/"
    MESSAGES_S3_PREFIX = "messages/"
    USERS_S3_PREFIX = "users/"
    BIDS_S3_PREFIX = "bids/"
    NOTIFICATIONS_S3_PREFIX = "notifications/"
    FREELANCER_REVIEWS_S3_PREFIX = "freelancer_reviews/"

    # EC2 specific configurations
    EC2_DEPLOYMENT = True
    EC2_MEMORY_EFFICIENT = True
    EC2_MEMORY_THRESHOLD = 200 * 1024 * 1024
    EC2_API_URL = "http://ec2-54-221-34-34.compute-1.amazonaws.com:5000"

    # Local mode - when True, disables EC2 API dependency
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
