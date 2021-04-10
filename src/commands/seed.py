from telegram.ext import CommandHandler
from auth import auth

def seed(update, context):
    if auth.auth(update, context):
        pass
    else:
        pass

handler = CommandHandler('seed', seed)
