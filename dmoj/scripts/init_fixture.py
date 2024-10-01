from datetime import datetime
import os
import re
import string
import random
from typing import Optional

from django.contrib.auth.hashers import PBKDF2PasswordHasher

LETTERS = string.ascii_letters
NUMBERS = string.digits

template = string.Template(
    """
[
    {
        "fields": {
            "about": "",
            "ace_theme": "github",
            "current_contest": null,
            "display_rank": "admin",
            "ip": "10.0.2.2",
            "language": 1,
            "last_access": "${date_joined}",
            "math_engine": "auto",
            "mute": false,
            "organizations": [
                1
            ],
            "performance_points": 0.0,
            "points": 0.0,
            "problem_count": 0,
            "rating": null,
            "timezone": "Europe/Prague",
            "user": 1,
            "user_script": ""
        },
        "model": "judge.profile",
        "pk": 1
    },
    {
        "fields": {
            "date_joined": "${date_joined}",
            "email": "",
            "first_name": "",
            "groups": [

            ],
            "is_active": true,
            "is_staff": true,
            "is_superuser": true,
            "last_login": "${date_joined}",
            "last_name": "",
            "password": "${password_hash}",
            "user_permissions": [

            ],
            "username": "admin"
        },
        "model": "auth.user",
        "pk": 1
    },
    {
        "fields": {
            "about": "",
            "access_code": null,
            "admins": [
                1
            ],
            "creation_date": "${date_joined}",
            "is_open": true,
            "slug": "qqh",
            "name": "QQH: Qminers Quant Hackathon",
            "short_name": "QQH",
            "slots": null
        },
        "model": "judge.organization",
        "pk": 1
    },
    {
        "fields": {
            "full_name": "Sports Bettings",
            "name": "Sports Bettings"
        },
        "model": "judge.problemtype",
        "pk": 1
    },
    {
        "fields": {
            "full_name": "Machine Learning",
            "name": "Machine Learning"
        },
        "model": "judge.problemgroup",
        "pk": 1
    },
    {
        "fields": {
            "domain": "localhost:8080",
            "name": "QQH: Qminers Quant Hackathon"
        },
        "model": "sites.site",
        "pk": 1
    }
]
"""
)


def random_string(length: int = 20):
    """
    Generates a random password having the specified length
    :length -> length of password to be generated. Defaults to 8
        if nothing is specified.
    :returns string <class 'str'>
    """
    # create alphanumerical from string constants
    printable = f"{LETTERS}{NUMBERS}"

    # convert printable from string to list and shuffle
    printable = list(printable)
    random.shuffle(printable)

    # generate random password and convert to string
    random_password = random.choices(printable, k=length)
    random_password = "".join(random_password)
    return random_password


def get_password_hash(
    password: str, salt: Optional[str] = None, iterations: int = 36000
):
    hasher = PBKDF2PasswordHasher()
    if salt is None:
        salt = random_string(12)
    return hasher.encode(password, salt, iterations)

def is_yes(text: str):
    t = text.lower()
    return t == "y" or t == "yes"

answer = input(
    """Create your own admin password? [y/N]
If [N] is selected password will be automatically generated.
"""
)

if is_yes(answer):
    password = input("Enter your password (alphanumeric characters):\n")
    password = re.sub(r"[^a-zA-Z0-9]", "", password)

else:
    password = random_string(12)

print(f"Your password is: {password}")

pw_hash = get_password_hash(password)

init_fixture = template.substitute(password_hash=pw_hash, date_joined=datetime.now())

with open("repo/judge/fixtures/init.json", "w+") as f:
    f.write(init_fixture)
    

answer = input(
    """Do you want to execute the fxiture now? [y/N]
The site has to be running or you can run "$ ./scripts/manage.py loaddata init" later to load the fixture when the site is running.
""")

if is_yes(answer):
    os.system("./scripts/manage.py loaddata init")
