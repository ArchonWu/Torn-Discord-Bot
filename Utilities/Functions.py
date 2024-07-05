import os

import aiohttp


full_energy_notified = 0
full_nerve_notified = 0


async def request_all_player_bars():
    torn_api_key_limited = os.getenv('TORN_API_KEY_LIMITED')
    url = f"https://api.torn.com/user/?selections=bars&key={torn_api_key_limited}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()


# calculate whether user's energy or nerve level reaches target_level, and notify the user
# e.g. 80/100 is >= 0.8
async def check_energy_or_nerve_reach_levels(target_user, target_level):
    torn_user_bars = await request_all_player_bars()
    print(torn_user_bars)

    # calculate user_energy_level
    user_energy_current = torn_user_bars["energy"]["current"]
    user_energy_maximum = torn_user_bars["energy"]["maximum"]
    user_energy_level = user_energy_current / user_energy_maximum
    user_energy_level_rounded = round(user_energy_level * 100, 3)
    print(user_energy_level, user_energy_current, user_energy_maximum)

    # calculate user_nerve_level
    user_nerve_current = torn_user_bars["nerve"]["current"]
    user_nerve_maximum = torn_user_bars["nerve"]["maximum"]
    user_nerve_level = user_nerve_current / user_nerve_maximum
    user_nerve_level_rounded = round(user_nerve_level * 100, 3)
    print(user_nerve_level, user_nerve_current, user_nerve_maximum)

    # notify user if necessary
    if 1.0 > user_energy_level >= target_level:
        await notify_user(target_user,
                          f"Your energy is now {user_energy_level_rounded}% full! "
                          f"({user_energy_current} / {user_energy_maximum})")

    if 1.0 > user_nerve_level >= target_level:
        await notify_user(target_user,
                          f"Your nerve is now {user_nerve_level_rounded}% full! "
                          f"({user_nerve_current} / {user_nerve_maximum})")


async def notify_user(target_user, private_message):
    await target_user.send(private_message)

