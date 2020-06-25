


# FOR WHAT?

 - For training
 - For learning new
 
# MAIN IDEA 

The idea of this project is to simplify costing for groups of people. 
Suppose you rent an apartment with your friends, every day someone buys something, someone more, someone less, but in the end everyone should spend the same amount.
This application will simplify this task.

# HOW TO USE?

There are thre types of users:

- User
- Moderatoe
- Administrator

User can:

- Make cost
- Make need(wish to purchase)
- Update/Delete own costs and needs
- Join groups

Moderator can:
- User permission
- Create/Update groups
- Delete all costs from groups
- Delete all needs from groups
- Delete costs and needs from groups

Administrator can:
- Moderator permission
- Delete groups
- сhange roles

To use all features, make account, confim your email, and go!
You can view only costs, and needs in groups of which you are a member.
Make groups with friend, write your costs. If your group need some stuff, make need, someone will see that and will buy that.

You want back your money? Do cost canculation, and you can see, who owes whom and how much.

# API 

Only authorized users can access to app. 
Cost app use ```Basic Authorization```, with ```Authorization``` header
Fill in 
```
Authorization : Basic <credentials>
```
Where ```<credentials>``` is (```Username```+ ':'+ ```Password```) encoded by ```Base64``` algorithm 

Also you can use authorization token. All you need, is send ```POST``` requset to  ```https://costapp-2234.herokuapp.com/api/token``` with fiil in ```Authorization``` header 
```
Authorization : Basic <encoded token by base64>
```

All subsequent requests must have a filed header ```Authorization```

#### COSTS
- ```GET /api/costs/<cost_i>``` get cost by ```cost_id```
- ```DELETE /api/costs/<cost_i>``` delete cost by ```cost_id```
- ```PUT /api/costs/<cost_i>``` update cost by ```cost_id```
- ```POST /api/costs/create``` create cost 
- ```GET /api/costs/self``` get current user all costs
- ```GET /api/costs/group/<group_id>``` get all costs by group ```group_id```
- ```GET /api/costs/calculate/<group_id>``` calculate final table

To create costs, you mast send json data like this way:
```
{"cost_title": <Cost Name>,
"spent_money": <Amount>,
"group_id": <Group id>
}
```

#### Needs
- ```GET /api/needs/<need_id>``` get need by ```need_id```
- ```DELETE /api/needs/<need_id>``` delete need by ```need_id```
- ```PUT /api/needs/<nedd_id>``` update need by ```need_id```
- ```POST /api/needs/create``` create need
- ```GET /api/needs/self``` get current user all needs
- ```GET /api/needs/group/<group_id>``` get all needs by ```group_id```

To create need, you mast send json data like this way:
```
{"text": <Text>,
"group_id": <Group id>}
```

#### Groups

- ```GET /api/groups/<group_id>``` get group by ```group_id```
- ```DELETE /api/groups/<group_id>``` delete group by ```group_id```
- ```PUT /api/groups/<group_id>``` update group by ```group_id```
- ```POST /api/groups/create``` create group
- ```GET /api/groups/user/<user_id>``` get user groups by ```user_id```
- ```POST /api/groups/membership``` join a group
- ```DELETE /api/groups/membership``` exit from the group with the removal of all own costs

>To create group, you mast has perrmision ```Moderate```, and send json data like this way:
```
{"name": <Group name>}
```

>To join the group, you mast send json data like this way:

```
{"user_id": <User id>,
"group_id": <Group id>
}
```

*to exit from group, just change method from ```POST``` to ```DELETE```

#### Users

- ```GET /api/users/<user_id>``` get user by ```user_id```
- ```POST /users/register``` register new user
- ```GET /api/users/self``` get self acount info
- ```PUT /api/users/self``` update self acount username

>To register user, you must send json data like this way:
```
{"username": <Username>,
"email": <Email>,
"password": <User password>
}
```
NOTE: ```username``` and ```email``` must be unique

> response ```/api/token```
```
{
  "expiration": 200000,
  "token": "there_you_will_resive_your_access_token"
}
```

> response ```GET /api/costs/<id> ``` 
```
{
  "group": "https://costapp-2234.herokuapp.com/api/groups/<id>",
  "purchase_time": "Mon, 01 May 2020 00:00:00 GMT",
  "spent_money": 2000.0,
  "title": "some",
  "url": "https://costapp-2234.herokuapp.com/api/costs/<id>",
  "who_spent": "https://costapp-2234.herokuapp.com/api/users/<user_id>"
}
```
>  response ```/api/costs/debt_table/<group_id>```
```
{
  "debt_row": [
    {
      "debt_amount": 30,
      "group": "https://costapp-2234.herokuapp.com/api/groups/<group_id>",
      "who": "https://costapp-2234.herokuapp.com/api/users/<user_id>",
      "whom": "https://costapp-2234.herokuapp.com/api/users/<user_id>"
    },
    ...
    ]
    }
```
> response ```GET /api/need/<id> ``` 
```
{
  "author": "https://costapp-2234.herokuapp.com/api/users/<user_id>",
  "done": false,
  "group": "https://costapp-2234.herokuapp.com/api/groups/<group_id>",
  "text": "Need text",
  "url": "https://costapp-2234.herokuapp.com/api/needs/<need_id>"
}
```
> response ```GET /api/users/self ``` 
```

 {
  "groups": "https://costapp-2234.herokuapp.com/api/groups/user/<user_id>",
  "role": "Role",
  "url": "https://costapp-2234.herokuapp.com/api/users/<user_id>",
  "username": "Username"
}
```

# HOW TO RUN?
Clone or download repo  by```git clone```
Set up venv ```python -m venv <venv name>```
Install all package ``` pip install -r requirements.txt```

If wee need to test or deploy our app, we need to set ```FLASK_CONFIG``` env varible. 
There are three values that we can set for this varible, for defult is ```development```, if need to test app that ```testing``` and deployment ```deploy```

Besides this, you need to enter a couple of commands in the terminal:
```sh
$ export SECRET_KEY=<some secret key>
$ export COSTAPP_ADMIN=<Admistrator email>
$ export MAIL_USERNAME=<SMTP email>
$ export MAIL_PASSWORD=<SMTP password>
$ export FLASK_CONFIG=<config>
```
And finally ```python manage.py runserver```

# Disclaimer

App in development procces, and may some things wound`t work

=======
# cost_app
 cost processing application
>>>>>>> edb5ba8e6589b0a9441c107f5b40b7c74c683e52
