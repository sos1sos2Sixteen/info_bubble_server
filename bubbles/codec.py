from .authentication import validate_auth
from .models import Account

USER_LOGGED_IN  =   0
NO_SUCH_USER    =   1
FORMAT_ERROR    =   2


def reply(data,succ):
    datum = {
        "success" : succ,
        "data" : data
    }
    return (datum)

def success(data):
    return reply(data,0)

def failure(data):
    return reply(data,1)

def userAuthentication(request):
    try:
        user = request['user']
        auth = request['auth']
        # insert authentication

        acct = Account.objects.get(account_num = user)

        if validate_auth(acct,auth):
            return USER_LOGGED_IN    # 0 -> logged-in user
        else:
            return NO_SUCH_USER    # 1 -> not logged-in or no-such-user
    except KeyError:
        return FORMAT_ERROR        # 2 -> request format-error
    except Account.DoesNotExist:
        return NO_SUCH_USER



    