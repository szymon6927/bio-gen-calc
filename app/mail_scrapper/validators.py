from email.utils import parseaddr


def is_email_valid(email: str) -> bool:
    return '@' in parseaddr(email)[1]
