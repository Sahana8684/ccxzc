from fastapi import APIRouter, Depends, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional

from school_management_system.database.session import get_db
from school_management_system.models.user import User
from school_management_system.utils.security import verify_password, create_access_token

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Render the home page.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: Optional[str] = None):
    """
    Render the login page.
    """
    return templates.TemplateResponse("auth/login.html", {"request": request, "error": error})


@router.post("/login")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    Process login form submission.
    """
    # Find user by email
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()
    
    # Check if user exists and password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Invalid email or password"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    
    # Check if user is active
    if not user.is_active:
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Account is inactive"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    
    # Create access token
    access_token = create_access_token(subject=user.id)
    
    # Set cookie and redirect to dashboard
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    
    return response


@router.get("/logout")
async def logout():
    """
    Log out the user by clearing the access token cookie.
    """
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Render the dashboard page.
    """
    # This would typically check for authentication and get user data
    # For now, we'll just render a placeholder
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """
    Render the about page.
    """
    return templates.TemplateResponse("about.html", {"request": request})


@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    """
    Render the contact page.
    """
    return templates.TemplateResponse("contact.html", {"request": request})


@router.get("/privacy", response_class=HTMLResponse)
async def privacy(request: Request):
    """
    Render the privacy policy page.
    """
    return templates.TemplateResponse("privacy.html", {"request": request})


@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password(request: Request):
    """
    Render the forgot password page.
    """
    return templates.TemplateResponse("auth/forgot_password.html", {"request": request})


@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    """
    Render the user profile page.
    """
    # This would typically check for authentication and get user data
    # For now, we'll just render a placeholder
    return templates.TemplateResponse("profile.html", {"request": request})


@router.get("/change-password", response_class=HTMLResponse)
async def change_password(request: Request):
    """
    Render the change password page.
    """
    # This would typically check for authentication
    # For now, we'll just render a placeholder
    return templates.TemplateResponse("auth/change_password.html", {"request": request})


# Admin routes
@router.get("/admin/{path:path}", response_class=HTMLResponse)
async def admin_pages(request: Request, path: str):
    """
    Render admin pages.
    """
    # This would typically check for admin permissions
    # For now, we'll just render a placeholder
    return templates.TemplateResponse(f"admin/{path}.html", {"request": request})


# Teacher routes
@router.get("/teacher/{path:path}", response_class=HTMLResponse)
async def teacher_pages(request: Request, path: str):
    """
    Render teacher pages.
    """
    # This would typically check for teacher permissions
    # For now, we'll just render a placeholder
    return templates.TemplateResponse(f"teacher/{path}.html", {"request": request})


# Parent routes
@router.get("/parent/{path:path}", response_class=HTMLResponse)
async def parent_pages(request: Request, path: str):
    """
    Render parent pages.
    """
    # This would typically check for parent permissions
    # For now, we'll just render a placeholder
    return templates.TemplateResponse(f"parent/{path}.html", {"request": request})
