_MESSAGES = {
    'NO_NC_GRANT': 'The access is not yet granted in Nextcloud!',
    'NC_AUTHZ_FLOW_RESET_DONE': 'Ok, try again now!',
    'NC_CREDENTIALS_DESERIALIZATION_ERROR': 'Nextcloud credentials cannot be found. If the problem persists, please contact administrator.',
}

def getmsg(msg_code, fail_silently=True):
    if not fail_silently and msg_code not in _MESSAGES:
        raise ValueError('Invalid message code "%s"' % msg_code)
    return _MESSAGES.get(msg_code, msg_code)
