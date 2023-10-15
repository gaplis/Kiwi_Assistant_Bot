from random import choice


def get_random_word():
    with open('data/words_for_wordle.txt', 'r', encoding='utf-8') as file:
        words = file.read().split('\n')

    random_word = choice(words)
    return random_word


def get_text_with_emoji(secret_word, user_word):
    emoji_dict = {
        1: '✅',
        2: '⚠️',
        3: '❌',
    }

    text_with_emoji = []

    for i in range(6):
        if user_word[i] not in secret_word:
            text_with_emoji.append(f'{emoji_dict[3]}-{user_word[i].upper()}')
        elif user_word[i] == secret_word[i]:
            text_with_emoji.append(f'{emoji_dict[1]}-{user_word[i].upper()}')
        else:
            text_with_emoji.append(f'{emoji_dict[2]}-{user_word[i].upper()}')

    return " ".join(text_with_emoji)


def checking_for_word_existence(check_word):
    with open('data/words_for_wordle.txt', 'r', encoding='utf-8') as file:
        words = file.read().split('\n')

        return check_word in words
