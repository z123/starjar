from functools import wraps

from flask import flash, redirect
from flask_login import current_user


def anonymous_required(url='/settings'):
    """
    Redirect a user to a specified location if they are already signed in.
    :param url: URL to be redirected to if invalid
    :type url: str
    :return: Function
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated():
            return redirect(url)

        return f(*args, **kwargs)

    return decorated_function
