# reyes-bot
Bot for helping moderate the help queue in my multivariable calculus course's discord server.

# setup and install
```
> Cloning
git clone https://github.com/fuzzyhappy/reyes-bot.git
cd reyes-bot

> Setting up the virtual env
python3 -m venv botenv
>> On Windows
py -m venv botenv

> Activating the env
source botenv/bin/activate
>> Windows
botenv\Scripts\activate.bat

> Installing the requirements
pip install -r requirements.txt

> Installing discord.py
pip install -U discord.py

> Setting the secret token
touch secret
[put token in secret]

> Running bot
python bot.py
>> Windows
py bot.py
```
