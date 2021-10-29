import os
from collections import Counter


def save_attempt(attempt, user_id, challenge_id):
    path = 'attempt_logs/challenge_%s' % challenge_id
    if not os.path.exists(path):
        os.makedirs(path)
    with open('attempt_logs/challenge_%s/%s.txt' % (challenge_id, user_id), mode='a') as file:
        file.write(attempt + '\n')


def convert_file_to_dict(file):
    attempts = file.read()[:-1].split('\n')
    result = {}
    for attempt in attempts:
        aux = result.get(attempt, 0) + 1
        result[attempt] = aux
    return result


def get_attempts(challenge_id, user_id=None):
    path = 'attempt_logs/challenge_%s' % challenge_id
    result = {}
    try:
        if user_id is None:
            result = Counter(result)
            for file_name in os.listdir(path):
                with open('%s/%s' % (path, file_name), mode='r') as file:
                    result += Counter(convert_file_to_dict(file))
            result = dict(result)
        else:
            with open('%s/%s.txt' % (path, user_id), mode='r') as file:
                result.update(convert_file_to_dict(file))
    except IOError:
        pass
    return sorted(result.items(), key=lambda item: item[1])
