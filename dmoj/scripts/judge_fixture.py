from datetime import datetime
import os
import re
import string
import random
from typing import Optional

from django.contrib.auth.hashers import PBKDF2PasswordHasher

N_JUDGES = 20
JUDGE_NAME = "QQHJudge"
LETTERS = string.ascii_letters
NUMBERS = string.digits
CHARACTERS = r"""!#%&'()*+,-./:;<=>?@[]^_`|~"""

judge_template = string.Template(
    """
    {
        "fields": {
            "name": "${judge_name}",
            "auth_key": "${auth_key}",
            "created": "${current_date}"
        },
        "model": "judge.judge",
        "pk": ${judge_index}
    }
"""
)

env_template = string.Template(
    """
JUDGE_NAME=${judge_name}
JUDGE_KEY="${auth_key}"
SANDBOX_PATH="${sandbox_path}"
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
    printable = f"{LETTERS}{NUMBERS}{CHARACTERS}"

    # convert printable from string to list and shuffle
    printable = list(printable)
    random.shuffle(printable)

    # generate random password and convert to string
    random_password = random.choices(printable, k=length)
    random_password = "".join(random_password)
    return random_password


def is_yes(text: str):
    t = text.lower()
    return t == "y" or t == "yes"


auth_key = random_string(100)
current_date = datetime.now()
first_judge_idx = 1

judges = [
    judge_template.substitute(
        judge_name=f"{JUDGE_NAME}{judge_index}",
        auth_key=auth_key,
        current_date=current_date,
        judge_index=judge_index,
    )
    for judge_index in range(1, N_JUDGES + 1)
]


judges_fixture = ",\n".join(judges)
judges_fixture = f"[\n{judges_fixture}\n]"

with open("repo/judge/fixtures/judges.json", "w+") as f:
    f.write(judges_fixture)


relative_sandbox_path = "../judge-server/sandbox"
sandbox_path = os.path.realpath(relative_sandbox_path)

with open("../judge-server/environment/judge.env", "w+") as f:
    f.write(
        env_template.substitute(
            judge_name=JUDGE_NAME, auth_key=auth_key, sandbox_path=sandbox_path
        )
    )

answer = input(
    """Do you want to execute the fxiture now? [y/N]
The site has to be running or you can run "$ ./scripts/manage.py loaddata \
judges" later to load the fixture when the site is running.
"""
)

if is_yes(answer):
    os.system("./scripts/manage.py loaddata judges")
