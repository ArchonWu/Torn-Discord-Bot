from random import randint, choice


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return "nothing was said."
    elif 'hello' or 'hi' in lowered:
        return 'Hello there!'
    elif 'roll dice' in lowered:
        return f'You rolled: {randint(1, 20)}'
    else:
        return choice(['what?',
                       'nani?'])
