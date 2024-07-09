import os

import aiohttp


last_reported_stats_values = {}  # dictionary to store last reported values


async def request_all_player_stats():
    torn_api_key_limited = os.getenv('TORN_API_KEY_LIMITED')
    url = f"https://api.torn.com/user/?selections=bars&key={torn_api_key_limited}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()


# calculate whether user's energy or nerve level reaches target_level, and notify the user
# e.g. 80/100 is >= 0.8
# e.g. stats_type can be one of energy, nerve, happy, health, chain
async def check_stats_type(stats_type, target_level, target_user):
    global last_reported_stats_values

    torn_user_bars = await request_all_player_stats()    # calls API

    user_stats_current = torn_user_bars[stats_type]["current"]
    user_stats_maximum = torn_user_bars[stats_type]["maximum"]
    user_stats_level = user_stats_current / user_stats_maximum
    user_stats_level_rounded = round(user_stats_level * 100, 1)

    if stats_type not in last_reported_stats_values:
        # last_reported_values is empty since this is the first time calling the API
        await notify_user(target_user,
                          f"Your {stats_type} is now {user_stats_level_rounded}% full!"
                          f"({user_stats_current} / {user_stats_maximum})")
        last_reported_stats_values[stats_type] = user_stats_current

    else:   # stats_type in last_reported_values
        last_reported_current = last_reported_stats_values[stats_type]
        # notify only if there is a change in stats, and meets or exceeds target_level
        if last_reported_current != user_stats_current and user_stats_level >= target_level:
            await notify_user(target_user,
                              f"Your {stats_type} is now {user_stats_level_rounded}% full!"
                              f"({user_stats_current} / {user_stats_maximum})")
            last_reported_stats_values[stats_type] = user_stats_current

        print(stats_type, user_stats_level, last_reported_stats_values, last_reported_current)


async def notify_user(target_user, private_message):
    await target_user.send(private_message)

