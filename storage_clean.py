import json
import logging
import os
import uuid
from typing import BinaryIO, Dict, List, Optional, TypeVar

import boto3
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename

from config import Config

logger = logging.getLogger(__name__)

T = TypeVar("T")


class S3StorageService:
    """Service to handle S3 storage operations using two buckets"""

    def __init__(self):
        # Setup S3 client
        self.s3 = None
        try:
            self.s3 = boto3.client(
                "s3",
                aws_access_key_id=Config.AWS_ACCESS_KEY,
                aws_secret_access_key=Config.AWS_SECRET_KEY,
                region_name=Config.AWS_REGION,
            )
            logger.info("S3 client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {e}")
            raise RuntimeError(f"Failed to initialize S3 client: {e}")

        self.general_bucket = Config.S3_BUCKET_NAME
        self.vector_bucket = Config.S3_VECTOR_BUCKET

    def upload_file(
        self, file_obj: BinaryIO, folder: str, filename: str
    ) -> Optional[str]:
        """Upload a file to S3 general bucket"""
        filename = secure_filename(filename)

        try:
            s3_path = os.path.join(folder, filename)
            self.s3.upload_fileobj(file_obj, self.general_bucket, s3_path)
            return s3_path
        except ClientError as e:
            logger.error(f"Error uploading file to S3: {e}")
            return None

    def download_file(self, s3_path: str) -> Optional[bytes]:
        """Download a file from S3 general bucket"""
        try:
            response = self.s3.get_object(Bucket=self.general_bucket, Key=s3_path)
            return response["Body"].read()
        except ClientError as e:
            logger.error(f"Error downloading file from S3: {e}")
            return None

    def delete_file(self, s3_path: str) -> bool:
        """Delete a file from S3 general bucket"""
        try:
            self.s3.delete_object(Bucket=self.general_bucket, Key=s3_path)
            return True
        except ClientError as e:
            logger.error(f"Error deleting file from S3: {e}")
            return False

    def generate_presigned_url(
        self, s3_path: str, expiration: int = 3600
    ) -> Optional[str]:
        """Generate a presigned URL for file download"""
        try:
            url = self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.general_bucket, "Key": s3_path},
                ExpiresIn=expiration,
            )
            return url
        except ClientError as e:
            logger.error(f"Error generating presigned URL: {e}")
            return None

    def save_data(self, data: Dict, collection: str) -> Optional[str]:
        """Save data to S3 general bucket"""
        try:
            if "id" not in data:
                data["id"] = str(uuid.uuid4())

            # Determine the correct prefix based on the collection
            if collection == "profiles":
                key_prefix = Config.PROFILES_S3_PREFIX
            elif collection == "posts":
                key_prefix = Config.POSTS_S3_PREFIX
            elif collection == "users":
                key_prefix = Config.USERS_S3_PREFIX
            elif collection == "bids":
                key_prefix = Config.BIDS_S3_PREFIX
            elif collection == "notifications":
                key_prefix = Config.NOTIFICATIONS_S3_PREFIX
            elif collection == "messages":
                key_prefix = Config.MESSAGES_S3_PREFIX
            elif collection == "freelancer_profiles":
                key_prefix = Config.PROFILES_S3_PREFIX
            elif collection == "client_profiles":
                key_prefix = Config.PROFILES_S3_PREFIX
            elif collection == "freelancer_reviews":
                key_prefix = Config.FREELANCER_REVIEWS_S3_PREFIX
            else:
                # Fallback for unknown collection
                logger.warning(f"Unknown collection type: {collection}. Using root.")
                key_prefix = ""

            key = f"{key_prefix}{data['id']}.json"
            self.s3.put_object(
                Bucket=self.general_bucket, Key=key, Body=json.dumps(data)
            )
            return data["id"]
        except Exception as e:
            logger.error(f"Error saving data to S3: {e}")
            return None

    def get_data(self, collection: str, data_id: str) -> Optional[Dict]:
        """Get data from S3 general bucket"""
        try:
            # Determine the correct prefix based on the collection
            if collection == "profiles":
                key_prefix = Config.PROFILES_S3_PREFIX
            elif collection == "posts":
                key_prefix = Config.POSTS_S3_PREFIX
            elif collection == "users":
                key_prefix = Config.USERS_S3_PREFIX
            elif collection == "bids":
                key_prefix = Config.BIDS_S3_PREFIX
            elif collection == "notifications":
                key_prefix = Config.NOTIFICATIONS_S3_PREFIX
            elif collection == "messages":
                key_prefix = Config.MESSAGES_S3_PREFIX
            elif collection == "freelancer_profiles":
                key_prefix = Config.PROFILES_S3_PREFIX
            elif collection == "client_profiles":
                key_prefix = Config.PROFILES_S3_PREFIX
            elif collection == "freelancer_reviews":
                key_prefix = Config.FREELANCER_REVIEWS_S3_PREFIX
            else:
                logger.warning(f"Unknown collection type: {collection}. Using root.")
                key_prefix = ""

            key = f"{key_prefix}{data_id}.json"
            response = self.s3.get_object(Bucket=self.general_bucket, Key=key)
            return json.loads(response["Body"].read())
        except Exception as e:
            logger.error(f"Error getting data from S3: {e}")
            return None

    def delete_data(self, collection: str, data_id: str) -> bool:
        """Delete data from S3 general bucket"""
        try:
            if collection == "profiles":
                key_prefix = Config.PROFILES_S3_PREFIX
            elif collection == "posts":
                key_prefix = Config.POSTS_S3_PREFIX
            elif collection == "users":
                key_prefix = Config.USERS_S3_PREFIX
            elif collection == "bids":
                key_prefix = Config.BIDS_S3_PREFIX
            elif collection == "notifications":
                key_prefix = Config.NOTIFICATIONS_S3_PREFIX
            elif collection == "messages":
                key_prefix = Config.MESSAGES_S3_PREFIX
            elif collection == "freelancer_profiles":
                key_prefix = Config.PROFILES_S3_PREFIX
            elif collection == "client_profiles":
                key_prefix = Config.PROFILES_S3_PREFIX
            elif collection == "freelancer_reviews":
                key_prefix = Config.FREELANCER_REVIEWS_S3_PREFIX
            else:
                logger.warning(f"Unknown collection type: {collection}. Using root.")
                key_prefix = ""
            key = f"{key_prefix}{data_id}.json"
            self.s3.delete_object(Bucket=self.general_bucket, Key=key)
            return True
        except Exception as e:
            logger.error(f"Error deleting data from S3: {e}")
            return False

    def query_data(self, collection: str, query: Dict = None) -> List[Dict]:
        """Query data from S3 general bucket"""
        try:
            if collection == "profiles":
                key_prefix = Config.PROFILES_S3_PREFIX
            elif collection == "posts":
                key_prefix = Config.POSTS_S3_PREFIX
            elif collection == "users":
                key_prefix = Config.USERS_S3_PREFIX
            elif collection == "bids":
                key_prefix = Config.BIDS_S3_PREFIX
            elif collection == "notifications":
                key_prefix = Config.NOTIFICATIONS_S3_PREFIX
            elif collection == "messages":
                key_prefix = Config.MESSAGES_S3_PREFIX
            elif collection == "freelancer_profiles":
                key_prefix = Config.PROFILES_S3_PREFIX
            elif collection == "client_profiles":
                key_prefix = Config.PROFILES_S3_PREFIX
            elif collection == "freelancer_reviews":
                key_prefix = Config.FREELANCER_REVIEWS_S3_PREFIX
            else:
                logger.warning(f"Unknown collection type: {collection}. Using root.")
                key_prefix = ""

            response = self.s3.list_objects_v2(
                Bucket=self.general_bucket, Prefix=key_prefix
            )
            results = []
            if "Contents" in response:
                for obj in response["Contents"]:
                    try:
                        obj_data = json.loads(
                            self.s3.get_object(
                                Bucket=self.general_bucket, Key=obj["Key"]
                            )["Body"].read()
                        )
                        if query:
                            # Simple query matching
                            match = True
                            for key, value in query.items():
                                if obj_data.get(key) != value:
                                    match = False
                                    break
                            if match:
                                results.append(obj_data)
                        else:
                            results.append(obj_data)
                    except Exception as e:
                        logger.warning(f"Error processing object {obj}: {e}")
            return results
        except Exception as e:
            logger.error(f"Error querying data from S3: {e}")
            return []

    def update_data(self, collection: str, data_id: str, updates: Dict) -> bool:
        """Update data in S3 general bucket"""
        try:
            current_data = self.get_data(collection, data_id)
            if current_data:
                current_data.update(updates)
                return self.save_data(current_data, collection) is not None
            return False
        except Exception as e:
            logger.error(f"Error updating data in S3: {e}")
            return False

    def save_vector_embedding(self, vector_id: str, embedding: List[float]) -> bool:
        """Save vector embedding to S3 vector bucket"""
        try:
            key = f"vectors/{vector_id}.json"
            data = {"id": vector_id, "embedding": embedding}
            self.s3.put_object(
                Bucket=self.vector_bucket, Key=key, Body=json.dumps(data)
            )
            return True
        except Exception as e:
            logger.error(f"Error saving vector embedding to S3: {e}")
            return False

    def get_vector_embedding(self, vector_id: str) -> Optional[List[float]]:
        """Get vector embedding from S3 vector bucket"""
        try:
            key = f"vectors/{vector_id}.json"
            response = self.s3.get_object(Bucket=self.vector_bucket, Key=key)
            data = json.loads(response["Body"].read())
            return data.get("embedding")
        except Exception as e:
            logger.error(f"Error getting vector embedding from S3: {e}")
            return None

    def delete_vector_embedding(self, vector_id: str) -> bool:
        """Delete vector embedding from S3 vector bucket"""
        try:
            key = f"vectors/{vector_id}.json"
            self.s3.delete_object(Bucket=self.vector_bucket, Key=key)
            return True
        except Exception as e:
            logger.error(f"Error deleting vector embedding from S3: {e}")
            return False
