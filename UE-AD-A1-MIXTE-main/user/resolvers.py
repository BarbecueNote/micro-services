import json

def user_with_id(_,info,_id):
    with open('{}/data/users.json'.format("."), "r") as file:
        users = json.load(file)
        for user in users['users']:
            if user['id'] == _id:
                return user