import logging

from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# compile translations
import subprocess
subprocess.call(['pybabel', 'compile', '-d', 'locales', '-D', 'messages'])

import api
import bot as botsource
import middlewares
import config as cnf
import setup

dp = Dispatcher()
dp.include_router(botsource.router)

logger = logging.getLogger(__name__)

middlewares.db.setup(dp)
middlewares.referer.setup(dp)
middlewares.session.setup(dp)
middlewares.i18n.setup(dp)

# This function is called when bots are started (setup.start_bot)
# Bots won't start until this function's execution is over
dp.startup.register(setup.main_startup)

dp.shutdown.register(setup.main_shutdown)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router)

# Initialize Bot instance with an default parse mode which will be passed to all API calls
bot = Bot(cnf.TOKEN, parse_mode="HTML")
setup.register_main_bot(dp, app, bot)
