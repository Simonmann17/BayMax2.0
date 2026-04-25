from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, field_validator
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

class UserCreate(BaseModel):
	email: EmailStr
	password: str

	@field_validator("password")
	def password_validator(cls, v):
		if len(v.strip()) < 8:
			raise ValueError("Password must be at least 8 characters long with no whitespace")
		if len(v) > 72:
			raise ValueError("Password cannot exceed 72 characters")
		return v

class UserLogin(BaseModel):
	email: EmailStr
	password: str

class Token(BaseModel):
	access_token: str
	token_type: str
	message: str

def hash_password(password: str) -> str:
	return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
	return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict) -> str:
	to_encode = data.copy() #Copy the data to avoid mutating the original data
	expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) #Set the token expiration time
	to_encode.update({"exp": expire}) #Add the expiration time to the token payload
	return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM) #Generating the JWT token

@router.post("/register", response_model=Token) #Register a new user endpoint
def register(user: UserCreate, db: Session = Depends(get_db)): #Register function
	existing_user = db.query(User).filter(User.email == user.email).first() #Check if the email is already registered
	if existing_user: 
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered") 

	#Hash the password and create a new user object
	hashed_password = hash_password(user.password)
	new_user = User(email=user.email, hashed_password=hashed_password)
	#Add the new user to the database and commit the transaction
	db.add(new_user)
	db.commit()
	db.refresh(new_user)

	access_token = create_access_token(data={"sub": new_user.email})
	return {"access_token": access_token, "token_type": "bearer", "message": "User registered successfully"}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
	db_user = db.query(User).filter(User.email == user.email).first()
	if not db_user or not verify_password(user.password, db_user.hashed_password):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

	access_token = create_access_token(data={"sub": db_user.email})

	return {"access_token": access_token, "token_type": "bearer", "message": "Login successful"}