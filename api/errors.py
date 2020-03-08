def error(code, info=None):
    return {
        'error_code': code,
        'error_info': info,
    }


BadLogin = error(1, 'Bad login.')
BadToken = error(19, 'Bad token.')
