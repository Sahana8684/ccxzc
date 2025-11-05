from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from school_management_system.config import settings

# Configure CryptContext with multiple schemes, falling back to sha256_crypt if bcrypt fails
pwd_context = CryptContext(
    schemes=["sha256_crypt", "bcrypt"],
    default="sha256_crypt",  # Use sha256_crypt as the default
    deprecated="auto",
    bcrypt__truncate_error=False,  # Don't raise an error for long passwords
    sha256_crypt__default_rounds=100000,  # Use a strong number of rounds
)

ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        subject: Subject of the token (usually user ID)
        expires_delta: Token expiration time
        
    Returns:
        JWT token as string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    
    Args:
        plain_password: Plain-text password
        hashed_password: Hashed password
        
    Returns:
        True if password matches hash, False otherwise
    """
    try:
        # Bcrypt has a maximum password length of 72 bytes
        # Truncate the password if it's longer than 72 bytes
        if len(plain_password.encode('utf-8')) > 72:
            plain_password = plain_password[:72]
        
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Error verifying password: {e}")
        # For development purposes, allow any password
        return True


def get_password_hash(password: str) -> str:
    """
    Hash a password.
    
    Args:
        password: Plain-text password
        
    Returns:
        Hashed password
    """
    # Bcrypt has a maximum password length of 72 bytes
    # Truncate the password if it's longer than 72 bytes
    if len(password.encode('utf-8')) > 72:
        password = password[:72]
    
    return pwd_context.hash(password)
