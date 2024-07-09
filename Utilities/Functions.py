import os

import aiohttp


full_stats_notified = []
FULL_STATS = 1.0


async def request_all_player_stats():
    torn_api_key_limited = os.getenv('TORN_API_KEY_LIMITED')
    url = f"https://api.torn.com/user/?selections=bars&key={torn_api_key_limited}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()


# calculate whether user's energy or nerve level reaches target_level, and notify the user
# e.g. 80/100 is >= 0.8
# e.g. stats_type can be one of energy, nerve, happy, health
async def check_stats_type(stats_type, target_level, target_user):
    global full_stats_notified

    torn_user_bars = await request_all_player_stats()    # calls API

    user_stats_current = torn_user_bars[stats_type]["current"]
    user_stats_maximum = torn_user_bars[stats_type]["maximum"]
    user_stats_level = user_stats_current / user_stats_maximum
    user_stats_level_rounded = round(user_stats_level * 100, 3)

    if stats_type not in full_stats_notified:   # if last notify was not at FULL (100%)
        if target_level <= user_stats_level < FULL_STATS:   # user_stats_level not full and is > target_level
            await notify_user(target_user,
                              f"Your {stats_type} is now {user_stats_level_rounded}% full!"
                              f"({user_stats_current} / {user_stats_maximum})")

        # if current stats level == FULL (100%), add to full_stats_notified
        if user_stats_level >= FULL_STATS:
            full_stats_notified.append(stats_type)

    elif stats_type in full_stats_notified:
        # if last notification was at 100% (in full_stats_notified),
        # but currently not FULL (<100%), notify user and remove from full_stats_notified
        if user_stats_level < FULL_STATS:
            await notify_user(target_user,
                              f"Your {stats_type} is now {user_stats_level_rounded}% full!"
                              f"({user_stats_current} / {user_stats_maximum})")
            full_stats_notified.remove(stats_type)

    print(stats_type, user_stats_level_rounded, full_stats_notified, FULL_STATS)


async def notify_user(target_user, private_message):
    await target_user.send(private_message)

