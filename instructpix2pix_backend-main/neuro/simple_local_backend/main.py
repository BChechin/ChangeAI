#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

from telegram import __version__ as TG_VER

from bot import Bot
from sd_utils import setup_sd, SD_Env, setup_pix2pix

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )


def build_bot(token, sd_env: SD_Env = SD_Env.MacBookM1, base_dir='app_data', use_sd=True, use_pix2pix=True) -> Bot:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    if use_sd:
        pipe_sd = setup_sd(sd_env=sd_env)
    else:
        pipe_sd = None
    if use_pix2pix:
        pipe_img2img = setup_pix2pix(sd_env=sd_env)
    else:
        pipe_img2img = None
    bot = Bot(token, pipe_sd, pipe_img2img, base_dir=base_dir)

    return bot


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--token', type=str, required=False, default=None)
    parser.add_argument('--secrets-path', type=str, default='secrets.json')
    parser.add_argument('--sd-env', type=str, default='m1', help='"m1" for macbook m1 or "t4" for nvidia t4')
    parser.add_argument('--base-dir', type=str, default='app_data', help='base directory for storing images and logs')
    parser.add_argument('--debug', action='store_true', help='debug mode')
    args = parser.parse_args()
    import json

    if args.token is None:
        with open(args.secrets_path) as f:
            secrets = json.load(f)
        token = secrets["TELEGRAM_BOT_TOKEN"]
    else:
        token = args.token

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)
    logging.info("Logging level: %s", logging.getLogger().getEffectiveLevel())

    bot = build_bot(token,
                    sd_env=SD_Env(args.sd_env),
                    base_dir=args.base_dir,
                    use_sd=False,
                    use_pix2pix=True
                    # use_pix2pix=False
                    )
    # noinspection PyTypeChecker
    bot.run()
    # asyncio.run(bot.run())
