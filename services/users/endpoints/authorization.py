from fastapi import APIRouter, Request, Form, Depends
from starlette.responses import JSONResponse
from pydantic import EmailStr
from typing import Annotated, Any
from starlette.templating import Jinja2Templates
from models.users import UserCreate
from repository.database.users import UsersRepository
from services.users import UserService
from core.db import session_manager
from core.http import create_response


router = APIRouter()
templates = Jinja2Templates(directory='frontend/templates')


async def get_users_service() -> UserService:
    async with session_manager.manage_session() as session:
        user_repository = UsersRepository(session)
        return UserService(user_repository)


@router.get('/register-form')
async def show_create_form(request: Request):
    return templates.TemplateResponse('users/register.html', context={'request': request})

@router.post('/create')
async def create_user(
    username: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    confirm_password: Annotated[str, Form()],
    user_service: UserService = Depends(get_users_service),
):

    if password != confirm_password:
        return JSONResponse(
            {"error": "Passwords don't match"},
            status_code=400
        )

    user_data = UserCreate(username=username, email=email, password=password)

    try:
        if await user_service.get_user_by_email(str(email)):
            return JSONResponse(
                {"error": "Email already registered"},
                status_code=400
            )

        if await user_service.get_user_by_username(username):
            return JSONResponse(
                {"error": "Username already taken"},
                status_code=400
            )

        await user_service.create_user(user_data)
        print('before redirect')
        return JSONResponse(
            {"success": True, "redirect": "/users/success"},
            status_code=200
        )

    except Exception as e:
        print(f"Error creating user: {e}")
        return JSONResponse(
            {"error": "Registration failed"},
            status_code=500
        )


@router.get('/success')
async def show_success_page(request: Request):
    return templates.TemplateResponse('users/success.html', context={'request': request})


@router.get('/email')
async def get_user_by_email(
        request: Request,
        user_service: UserService = Depends(get_users_service),
        email: EmailStr = Form(...)
) -> Any[JSONResponse, Jinja2Templates]:
    if not email:
        return templates.TemplateResponse('users/error.html', context={'request': request})

    user = user_service.get_user_by_email(email=str(email))
    if not user:
        return templates.TemplateResponse('users/error.html', context={'request': request}, status_code=404, headers={'error': 'User not found'})

    return user


@router.get('/username')
async def get_user_by_username(
        request: Request,
        user_service: UserService = Depends(get_users_service),
        username: str = Form(...)
) -> Any[JSONResponse, Jinja2Templates]:

    if not username:
        return templates.TemplateResponse('users/error.html', context={'request': request}, status_code=400, headers={'error': 'Username is null'})

    user = user_service.get_user_by_username(username=str(username))

    if not user:
        return templates.TemplateResponse('users/error.html', context={'request': request}, status_code=404, headers={'error': 'User not found'})