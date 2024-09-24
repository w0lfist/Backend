from fastapi import APIRouter, Depends, HTTPException, status
from database import get_users, get_user_id, create_user, get_user, get_user_email, delete_user, update_user
from models import UserModel, UpdateUserModel
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

user_route = APIRouter()

@user_route.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["user_name"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@user_route.get("/api/users")
async def get_all_users():
    all_users = await get_users()
    return all_users


@user_route.get("/api/users/{id}", response_model=UserModel)
async def get_one_user(id: str):
    one_user = await get_user_id(id)
    if one_user:
        return one_user
    raise HTTPException(404, f"User with id {id} not found")


@user_route.post("/api/users", response_model=UserModel)
async def create_one_user(User: UserModel):

    user_found = await get_user(User.user_name)
    user_found_email= await get_user_email(User.email)
    if user_found:
        raise HTTPException(409, "User alredy exist")
    if user_found_email:
        raise HTTPException(409, "this email alredy login")
    response = await create_user(User)
    if response:
        return response
    raise HTTPException(400, "something went wrong")
    


@user_route.put("/api/users/{id}", response_model=UserModel)
async def edit_user(id: str, user: UpdateUserModel):
    response = await update_user(id, user)
    if response:
        return response
    raise HTTPException(404, f"User with id {id} not found")