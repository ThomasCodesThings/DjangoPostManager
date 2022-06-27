import requests

USERS_URL = 'https://jsonplaceholder.typicode.com/users'
POSTS_URL = 'https://jsonplaceholder.typicode.com/posts'
USER_API_KEY = 'id'


def getUsersFromAPI():
    return requests.get(USERS_URL).json()

def getPostsFromAPI():
    return requests.get(POSTS_URL).json()

def validateUserId(userId):
    users = getUsersFromAPI()
    for user in users:
        if(user[USER_API_KEY] == userId):
            return True
    return False
