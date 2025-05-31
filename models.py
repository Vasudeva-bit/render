from datetime import datetime
from typing import Dict, List, Optional

from werkzeug.security import check_password_hash, generate_password_hash

from storage import S3StorageService

storage_service = S3StorageService()


class User:
    """User model for authentication and basic profile info"""

    def __init__(self, data: Dict):
        # Store user data directly as instance variables
        self.user_id = data.get("id")
        self.user_username = data.get("username")
        self.user_email = data.get("email")
        self.user_password_hash = data.get("password_hash")
        self.user_role = data.get("role")
        self.user_date_joined = data.get("date_joined")
        self.user_last_login = data.get("last_login")
        self.user_profile_pic = data.get("profile_pic", "butterfly.png")
        self.user_active = data.get("is_active", True)

        # Cache for related data
        self._client_profile = None
        self._freelancer_profile = None
        self._posts = None
        self._bids = None

    # Implement methods required by Flask-Login
    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.user_active

    def is_anonymous(self):
        return False

    # Access attributes directly
    def username(self):
        return self.user_username

    def email(self):
        return self.user_email

    def password_hash(self):
        return self.user_password_hash

    def role(self):
        return self.user_role

    def date_joined(self):
        return self.user_date_joined

    def last_login(self):
        return self.user_last_login

    def profile_pic(self):
        return self.user_profile_pic if self.user_profile_pic else "butterfly.png"

    # Setters for mutable attributes
    def set_last_login(self, value):
        self.user_last_login = value

    def set_profile_pic(self, value):
        self.user_profile_pic = value

    # Custom methods
    def set_password(self, password: str):
        self.user_password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if not self.user_password_hash:
            return False
        return check_password_hash(self.user_password_hash, password)

    def to_dict(self) -> Dict:
        return {
            "id": self.user_id,
            "username": self.user_username,
            "email": self.user_email,
            "password_hash": self.user_password_hash,
            "role": self.user_role,
            "date_joined": self.user_date_joined,
            "last_login": self.user_last_login,
            "profile_pic": self.user_profile_pic,
            "is_active": self.user_active,
        }

    @staticmethod
    def from_dict(data: Dict) -> "User":
        return User(data)

    # Enhanced methods for accessing related data
    def client_profile(self):
        """Get user's client profile with lazy loading"""
        if self.user_role != "client":
            return None

        if self._client_profile is None:
            profiles = storage_service.query_data(
                "client_profiles", {"user_id": self.user_id}
            )
            self._client_profile = (
                ClientProfile.from_dict(profiles[0]) if profiles else None
            )

        return self._client_profile

    def freelancer_profile(self):
        """Get user's freelancer profile with lazy loading"""
        if self.user_role != "freelancer":
            return None

        if self._freelancer_profile is None:
            profiles = storage_service.query_data(
                "freelancer_profiles", {"user_id": self.user_id}
            )
            self._freelancer_profile = (
                FreelancerProfile.from_dict(profiles[0]) if profiles else None
            )

        return self._freelancer_profile

    def posts(self):
        """Get posts created by this user (for clients)"""
        if self.user_role != "client" or not self.client_profile():
            return []

        if self._posts is None:
            posts_data = storage_service.query_data(
                "posts", {"client_id": self.client_profile().id}
            )
            self._posts = [Post.from_dict(post) for post in posts_data]

        return self._posts

    def bids(self):
        """Get bids submitted by this user (for freelancers)"""
        if self.user_role != "freelancer" or not self.freelancer_profile():
            return []

        if self._bids is None:
            bids_data = storage_service.query_data(
                "bids", {"freelancer_id": self.freelancer_profile().id}
            )
            self._bids = [Bid.from_dict(bid) for bid in bids_data]

        return self._bids


class FreelancerProfile:
    """Profile for freelancer users"""

    def __init__(self, data: Dict):
        self.id = data.get("id")
        self.user_id = data.get("user_id")
        self.domain = data.get("domain")
        self.skills = data.get("skills", "")
        self.bio = data.get("bio", "")
        self.experience = data.get("experience", "")
        self.experience_years = data.get("experience_years", 0)
        self.location = data.get("location", "")
        self.hourly_rate = data.get("hourly_rate", 0)
        self.rating = data.get("rating", 0.0)
        self.project_history = data.get("project_history", "New Freelancer")
        self.linkedin = data.get("linkedin", "")
        self.portfolio_url = data.get("portfolio_url", "")
        self.created_at = data.get("created_at", datetime.utcnow().isoformat())
        self.updated_at = data.get("updated_at", datetime.utcnow().isoformat())

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "domain": self.domain,
            "skills": self.skills,
            "bio": self.bio,
            "experience": self.experience,
            "experience_years": self.experience_years,
            "location": self.location,
            "hourly_rate": self.hourly_rate,
            "rating": self.rating,
            "project_history": self.project_history,
            "linkedin": self.linkedin,
            "portfolio_url": self.portfolio_url,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(data: Dict) -> "FreelancerProfile":
        return FreelancerProfile(data)


class ClientProfile:
    """Profile for client users"""

    def __init__(self, data: Dict):
        self.id = data.get("id")
        self.user_id = data.get("user_id")
        self.company_name = data.get("company_name", "")
        self.industry = data.get("industry", "")
        self.website = data.get("website", "")
        self.description = data.get("description", "")
        self.location = data.get("location", "")
        self.created_at = data.get("created_at", datetime.utcnow().isoformat())
        self.updated_at = data.get("updated_at", datetime.utcnow().isoformat())

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "company_name": self.company_name,
            "industry": self.industry,
            "website": self.website,
            "description": self.description,
            "location": self.location,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(data: Dict) -> "ClientProfile":
        return ClientProfile(data)


class Post:
    """Project/job posting by clients"""

    def __init__(self, data: Dict):
        self.id = data.get("id")
        self.client_id = data.get("client_id")
        self.title = data.get("title", "")
        self.description = data.get("description", "")
        self.skills = data.get("skills", "")
        self.keywords = data.get("keywords", "")
        self.budget = float(data.get("budget", 0))
        self.duration = data.get("duration", "")
        self.recommended_domain = data.get("recommended_domain", "")
        self.status = data.get("status", "open")
        self.created_at = data.get("created_at", datetime.utcnow().isoformat())
        self.updated_at = data.get("updated_at", datetime.utcnow().isoformat())
        self.attachments = data.get("attachments", [])

        # Handle created_at - convert string to datetime if needed
        created_at_value = data.get("created_at")
        if isinstance(created_at_value, str):
            try:
                self.created_at = datetime.fromisoformat(
                    created_at_value.replace("Z", "+00:00")
                )
            except ValueError:
                self.created_at = datetime.utcnow()
        else:
            self.created_at = created_at_value or datetime.utcnow()

        # Handle updated_at - convert string to datetime if needed
        updated_at_value = data.get("updated_at")
        if isinstance(updated_at_value, str):
            try:
                self.updated_at = datetime.fromisoformat(
                    updated_at_value.replace("Z", "+00:00")
                )
            except ValueError:
                self.updated_at = datetime.utcnow()
        else:
            self.updated_at = updated_at_value or datetime.utcnow()

        # Additional properties that will be set by view methods
        self.client = None
        self.bids = []
        self.similarity_score = None

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "client_id": self.client_id,
            "title": self.title,
            "description": self.description,
            "skills": self.skills,
            "keywords": self.keywords,
            "budget": self.budget,
            "duration": self.duration,
            "recommended_domain": self.recommended_domain,
            "status": self.status,
            "created_at": (
                self.created_at.isoformat()
                if isinstance(self.created_at, datetime)
                else self.created_at
            ),
            "updated_at": (
                self.updated_at.isoformat()
                if isinstance(self.updated_at, datetime)
                else self.updated_at
            ),
            "attachments": self.attachments,
        }

    @staticmethod
    def from_dict(data: Dict) -> "Post":
        return Post(data)


class Bid:
    """Bids placed by freelancers on posts"""

    def __init__(self, data: Dict):
        self.id = data.get("id")
        self.post_id = data.get("post_id")
        self.freelancer_id = data.get("freelancer_id")
        self.amount = float(data.get("amount", 0))
        self.proposal = data.get("proposal", "")
        self.delivery_time = data.get("delivery_time", "")
        self.created_at = data.get("created_at", datetime.utcnow().isoformat())
        self.updated_at = data.get("updated_at", datetime.utcnow().isoformat())
        self.status = data.get("status", "pending")

        # References that will be populated by view methods
        self.freelancer = data.get("freelancer")
        self.post = None

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "post_id": self.post_id,
            "freelancer_id": self.freelancer_id,
            "amount": self.amount,
            "proposal": self.proposal,
            "delivery_time": self.delivery_time,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: Dict) -> "Bid":
        return Bid(data)


class FreelancerReview:
    """Reviews for freelancers by clients"""

    def __init__(self, data: Dict):
        self.id = data.get("id")
        self.freelancer_id = data.get("freelancer_id")
        self.client_id = data.get("client_id")
        self.post_id = data.get("post_id")
        self.rating = data.get("rating", 0)
        self.comment = data.get("comment", "")
        self.created_at = data.get("created_at", datetime.utcnow().isoformat())

        # Populated by view methods
        self.freelancer = None
        self.client = None
        self.post = None

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "freelancer_id": self.freelancer_id,
            "client_id": self.client_id,
            "post_id": self.post_id,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data: Dict) -> "FreelancerReview":
        return FreelancerReview(data)


class Notification:
    """System notifications for users"""

    def __init__(self, data: Dict):
        self.id = data.get("id")
        self.user_id = data.get("user_id")
        self.title = data.get("title", "")
        self.message = data.get("message", "")
        self.is_read = data.get("is_read", False)
        self.created_at = data.get("created_at", datetime.utcnow().isoformat())

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "message": self.message,
            "is_read": self.is_read,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data: Dict) -> "Notification":
        return Notification(data)


class Message:
    """Messages between clients and freelancers"""

    def __init__(self, data: Dict):
        self.id = data.get("id")
        self.sender_id = data.get("sender_id")
        self.receiver_id = data.get("receiver_id")
        self.post_id = data.get("post_id")
        self.content = data.get("content", "")
        self.is_read = data.get("is_read", False)
        self.created_at = data.get("created_at", datetime.utcnow().isoformat())

        # References that will be populated by view methods
        self.sender = None
        self.receiver = None
        self.post = None

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "post_id": self.post_id,
            "content": self.content,
            "is_read": self.is_read,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data: Dict) -> "Message":
        return Message(data)


class AIChatMessage:
    """AI chat messages with Gemini"""

    def __init__(self, data: Dict):
        self.id = data.get("id")
        self.user_id = data.get("user_id")
        self.message = data.get("message", "")
        self.response = data.get("response", "")
        self.session_id = data.get("session_id", "")
        self.created_at = data.get("created_at", datetime.utcnow().isoformat())

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "message": self.message,
            "response": self.response,
            "session_id": self.session_id,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data: Dict) -> "AIChatMessage":
        return AIChatMessage(data)
