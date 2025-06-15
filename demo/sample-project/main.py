#!/usr/bin/env python3
"""
Example Flask application for testing LLM programming setup.
"""

import logging

from flask import Flask, jsonify, request
from pydantic import BaseModel, ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


class UserModel(BaseModel):
    name: str
    email: str
    age: int = None


@app.route('/')
def home():
    """Home endpoint."""
    return jsonify({"message": "Hello from example project!"})


@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    try:
        user_data = UserModel(**request.json)
        logger.info(f"Creating user: {user_data.name}")
        return jsonify({"user": user_data.dict(), "status": "created"})
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)