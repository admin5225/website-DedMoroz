from pymongo import MongoClient
from tok import MONGO_DB
from tok import MONGODB_LINK

mdb = MongoClient(MONGODB_LINK)[MONGO_DB]       # подключение к онлайн БД монго


def search_or_save_user(mdb, effective_user, total):    # если нет пользователя - то создается, иначе поиск и возвращение
    user = mdb.users.find_one({"name": effective_user.first_name})
    if not user:
        user = {
            "username": effective_user.username,
            "name": effective_user.first_name,
            "total": total
        }
        mdb.users.insert_one(user)
    return user


def save_user_info(mdb, user, effective_user, total): # изменение различных аспектов объекта, в данном случае количества очков
    mdb.users.update_one(
        {'name': effective_user.first_name},
        {'$set': {'total': total}}
    )
    return user
