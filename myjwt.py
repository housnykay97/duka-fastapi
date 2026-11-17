#import libraries
from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel


#
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#fake user for testing
fake_users_db = {
    "johndoe@example.com": {
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
    }
}

#Pydantic Models
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class User(BaseModel):
    email: str 
    full_name: str


class UserInDB(User):
    hashed_password: str


#Password hashing
password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")


#Change to JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



#JWT and Password hash functions
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def get_user(db, email: str):
    if email in db:
        user_dict = db[email]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, email: str, password: str):
    #We shall replace it with data from db
    user = get_user(fake_db, email)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception

    #We shall replace it with user from db
    user = get_user(fake_users_db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Test Functions to authenticate the above

#Password Functions
# hashed_pass = get_password_hash("dummypassword")
# print("Password Verifiation is------------",verify_password("dummypassword", hashed_pass))

# #Token Functions
# access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
# token = create_access_token(
#         data={"sub": "johndoe@example.com"}, 
#         expires_delta=access_token_expires
#     )
# print("Token is------------",token)
# #User Functions
# user = get_current_user(token)
# print("User email is------------",user)
