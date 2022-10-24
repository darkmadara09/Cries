from pprint import pprint
from typing import Any
from pymongo import MongoClient
from telegram import user
from config import MONGO_HOST
import itertools

my_client = MongoClient(host=MONGO_HOST)
my_db = my_client["aki-db"]


def addUser(user_id: int, first_name: str, last_name: str, user_name: str) -> None:
    dbam = my_db["users"]
    user = dbam.find_one({"user_id": user_id})
    if user is None:
    my_dict = {
    "user_id": user_id,
    "first_name": first_name,
    "last_name": last_name,
    "user_name": user_name,
    "aki_lang": "en",
    "child_mode": 1,
    "total_guess": 0,
    "correct_guess": 0,
    "wrong_guess": 0,
    "unfinished_guess": 0,
    "total_questions": 0,
  }
        dbam.insert_one(my_dict)
    elif user["user_id"] == user_id:
        updateUser(user_id, first_name, last_name, user_name)

    
def totalUsers():
    dbam = my_db["users"]
    #Returns the total no.of users who has started the bot.
    return len(list(dbam.find({})))


def updateUser(user_id: int, first_name: str, last_name: str, user_name: str) -> None:
    dbam = my_db["users"]
    to_update = {
        "user_name": user_name,
        "first_name": first_name,
        "last_name": last_name,
    }
    dbam.update_one({"user_id": user_id}, {"$set":to_update})


def getUser(user_id: int) -> Any or None:
    dbam = my_db["users"]
    return dbam.find_one({"user_id": user_id})


def getLanguage(user_id: int) -> str:
    dbam = my_db["users"]
    return dbam.find_one({"user_id": user_id})["aki_lang"]


def getTotalGuess(user_id: int) -> int:
    return my_db["users"].find_one({"user_id": user_id})["total_guess"]


def getCorrectGuess(user_id: int) -> int:
    return my_db["users"].find_one({"user_id": user_id})["correct_guess"]



def getWrongGuess(user_id: int) -> int:
    return my_db["users"].find_one({"user_id": user_id})["wrong_guess"]


def getUnfinishedGuess(user_id: int) -> int:
    crct_wrong_guess = getCorrectGuess(user_id)+getWrongGuess(user_id)
    unfinished_guess = getTotalGuess(user_id)-crct_wrong_guess
    my_db["users"].update_one({"user_id": user_id}, {"$set": {"unfinished_guess": unfinished_guess}})
    return my_db["users"].find_one({"user_id": user_id})["unfinished_guess"]



def getTotalQuestions(user_id: int) -> int:
    return my_db["users"].find_one({"user_id": user_id})["total_questions"]



def updateLanguage(user_id: int, lang_code: str) -> None:
    dbam = my_db["users"]
    dbam.update_one({"user_id": user_id}, {"$set": {"Fu_lang": lang_code}})


def updateTotalGuess(user_id: int, total_guess: int) -> None:
    total_guess = getTotalGuess(user_id)+total_guess
    my_db["users"].update_one({"user_id": user_id}, {"$set": {"total_guess": total_guess}})


def updateCorrectGuess(user_id: int, correct_guess: int) -> None:
    correct_guess = getCorrectGuess(user_id)+correct_guess
    my_db["users"].update_one({"user_id": user_id}, {"$set": {"correct_guess": correct_guess}})


def updateWrongGuess(user_id: int, wrong_guess: int) -> None:
    wrong_guess = getWrongGuess(user_id)+wrong_guess
    my_db["users"].update_one({"user_id": user_id}, {"$set": {"wrong_guess": wrong_guess}})
    

def updateTotalQuestions(user_id: int, total_questions: int) -> None:
    total_questions = total_questions+ getTotalQuestions(user_id)
    my_db["users"].update_one({"user_id": user_id}, {"$set": {"total_questions": total_questions}})


################# LEADERBOARD FUNCTIONS ####################

def getLead(what:str) -> list:
    lead_dict = {}
    for user in my_db['users'].find({}):
        lead_dict.update({user['first_name']: user[what]})
    lead_dict = sorted(lead_dict.items(), key=lambda x: x[1], reverse=True)
    return lead_dict[:10]
