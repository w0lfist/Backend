from motor.motor_asyncio import AsyncIOMotorClient
from models import UserModel
from bson import ObjectId
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)


client = AsyncIOMotorClient("mongodb+srv://Chris:Chris@timetoimprove.c17c0.mongodb.net/?retryWrites=true&w=majority&appName=TimeToImprove")
data_base = client.usersdatabase
collection = data_base.users



async def get_user_id(id):
    user_id = await collection.find_one({"_id": ObjectId(id)})
    return user_id

async def get_user(user_name):
    user_id = await collection.find_one({"user_name": user_name})
    return user_id


async def get_user_email(email):
    user_email = await collection.find_one({"email": email})
    return user_email


async def get_users():
    Users = []
    cursor = collection.find({})
    async for document in cursor:
        Users.append(UserModel(**document))
    return Users


async def create_user(user: UserModel):
    # Hashear la contraseña
    hashed_password = get_password_hash(user.password)
    
    # Crear el diccionario del usuario, reemplazando la contraseña por su hash
    user_dict = user.dict()
    user_dict['hashed_password'] = hashed_password
    del user_dict['password']  # Eliminar el campo de la contraseña en texto plano

    # Insertar el nuevo usuario en la base de datos
    new_user = await collection.insert_one(user_dict)
    created_user = await collection.find_one({"_id": new_user.inserted_id})
    
    return created_user


async def update_user(id: str, data):
    user = {k:v for k, v in data.dict().items() if v is not None}
    print(user)
    await collection.update_one({"_id": ObjectId(id)}, {"$set": user})
    document = await collection.find_one({"_id": ObjectId(id)})
    return document


async def delete_user(id: str):
    await collection.delete_one({"_id": ObjectId(id)})
    return True







