"""
Authentication router for FastAPI
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import structlog

from .database import get_db
from .models import User
from .schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
    Token,
    RefreshTokenRequest,
)
from .jwt import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from .dependencies import get_current_user

logger = structlog.get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["authentication"],
)


@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Register a new user account with email and password",
)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        JWT tokens for the new user

    Raises:
        HTTPException: If email already exists or validation fails
    """
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password
        password_hash = get_password_hash(user_data.password)

        # Create new user
        new_user = User(
            email=user_data.email,
            password_hash=password_hash,
            name=user_data.name,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info("user_registered", user_id=new_user.id, email=new_user.email)

        # Create tokens
        access_token = create_access_token(
            data={"user_id": new_user.id, "email": new_user.email}
        )
        refresh_token = create_refresh_token(
            data={"user_id": new_user.id, "email": new_user.email}
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    except Exception as e:
        db.rollback()
        logger.error("registration_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post(
    "/login",
    response_model=Token,
    summary="Login user",
    description="Login with email and password to receive JWT tokens",
)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login user

    Args:
        user_data: User login credentials
        db: Database session

    Returns:
        JWT tokens

    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by email
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user or not verify_password(user_data.password, user.password_hash):
        logger.warning("login_failed", email=user_data.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login time
    user.last_login_at = datetime.utcnow()
    db.commit()

    logger.info("user_logged_in", user_id=user.id, email=user.email)

    # Create tokens
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email}
    )
    refresh_token = create_refresh_token(
        data={"user_id": user.id, "email": user.email}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh access token",
    description="Get a new access token using a refresh token",
)
async def refresh_token(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token

    Args:
        token_data: Refresh token
        db: Database session

    Returns:
        New JWT tokens

    Raises:
        HTTPException: If refresh token is invalid
    """
    # Verify refresh token
    payload = verify_token(token_data.refresh_token, token_type="refresh")

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from token
    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create new tokens
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email}
    )
    new_refresh_token = create_refresh_token(
        data={"user_id": user.id, "email": user.email}
    )

    logger.info("token_refreshed", user_id=user.id)

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get the profile of the currently authenticated user",
)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current user profile

    Args:
        current_user: Current authenticated user

    Returns:
        User profile data
    """
    return current_user


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update current user",
    description="Update the profile of the currently authenticated user",
)
async def update_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user profile

    Args:
        user_update: User update data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated user profile

    Raises:
        HTTPException: If email already exists
    """
    try:
        # Update name if provided
        if user_update.name is not None:
            current_user.name = user_update.name

        # Update email if provided
        if user_update.email is not None and user_update.email != current_user.email:
            # Check if email already exists
            existing_user = db.query(User).filter(
                User.email == user_update.email,
                User.id != current_user.id
            ).first()

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )

            current_user.email = user_update.email

        db.commit()
        db.refresh(current_user)

        logger.info("user_updated", user_id=current_user.id)

        return current_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already in use"
        )
    except Exception as e:
        db.rollback()
        logger.error("user_update_failed", user_id=current_user.id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Update failed"
        )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout user",
    description="Logout the currently authenticated user (client-side token removal)",
)
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout user

    Note: This is a client-side operation. The client should remove the token.

    Args:
        current_user: Current authenticated user

    Returns:
        None
    """
    logger.info("user_logged_out", user_id=current_user.id)
    return None
