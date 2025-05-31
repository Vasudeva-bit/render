"""
API client for connecting Render frontend to EC2 backend
"""

import logging
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


class EC2APIClient:
    """Client for communicating with EC2 backend API"""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

    def login(
        self, username: str, password: str, remember: bool = False
    ) -> Dict[str, Any]:
        """Login user via EC2 API"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/auth/login",
                json={"username": username, "password": password, "remember": remember},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Login API error: {e}")
            return {"error": "Login failed. Please try again."}

    def register(
        self, username: str, email: str, password: str, role: str
    ) -> Dict[str, Any]:
        """Register user via EC2 API"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/auth/register",
                json={
                    "username": username,
                    "email": email,
                    "password": password,
                    "role": role,
                },
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Registration API error: {e}")
            return {"error": "Registration failed. Please try again."}

    def get_posts(
        self, page: int = 1, filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Get posts from EC2 API"""
        try:
            params = {"page": page}
            if filters:
                params.update(filters)

            response = self.session.get(
                f"{self.base_url}/api/posts", params=params, timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Get posts API error: {e}")
            return {"error": "Failed to load posts"}

    def get_user_dashboard(self, token: str) -> Dict[str, Any]:
        """Get dashboard data for authenticated user"""
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = self.session.get(
                f"{self.base_url}/api/dashboard", headers=headers, timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Dashboard API error: {e}")
            return {"error": "Failed to load dashboard"}

    def health_check(self) -> bool:
        """Check if EC2 API is healthy"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
