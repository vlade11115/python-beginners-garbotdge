#/usr/bin/env python3
# -*- coding: utf-8 -*-
import shelve

import config
from utils import bot, logger, get_user


def ban_bots(message):
    """Scans new members for bots,
    if there are user bots among new users -- kicks the bots
    and adds the rest of the users to the database
    """

    with shelve.open(config.data_name, 'c', writeback=True) as data:
        data['members'] = {} if not data.get('members') else data['members']
        # Checks every new member
        for member in message.new_chat_members:
            # If new member is bot, kicks it out and moves on
            if member.is_bot:
                bot.kick_chat_member(chat_id=config.chat_id, user_id=member.id)
                logger.info("Bot {} has been kicked out".format(get_user(member)))
                continue

            # If new member has joined for the first time
            # adds him/her to the database
            if not member.id in data['members']:
                data['members'][member.id] = 0
                logger.info("User {} has joined the chat for the first time and "\
                            "has been successfully added to the database".format(get_user(member)))