BURROW_VERSION = "v0.8.0"

# UNDERLINE_LENGTH = 100
START_TRUNCATION_LENGTH = 4
END_TRUNCATION_LENGTH = 4

##### The below are regular expressions used to find specific types of disclosure on a line-by-line basis

KEY_WITH_QUOTES_REGEX = r"k[e3]y['\"]?\s*[=:]+\s*['\"]{1}(?P<burrow>.+)['\"]{1}"
KEY_WITH_QUOTES = {
    "name": "Line contains \"key\" (within quotes)",
    "regex": KEY_WITH_QUOTES_REGEX,
    "type": "filecontent",
    "multiline": False,
    "entropic": True
}

KEY_WITHOUT_QUOTES_REGEX = r"k[e3]y\s*=+\s*(?!'\")(?P<burrow>[a-zA-Z0-9_\-+\/]+)"
KEY_WITHOUT_QUOTES = {
    "name": "\"key\" phrase",
    "regex": KEY_WITHOUT_QUOTES_REGEX,
    "type": "filecontent",
    "multiline": False,
    "entropic": True
}

SECRET_WITH_QUOTES_REGEX = r"s[e3]c[r4][e3]t['\"]?\s*[=:]+\s*['\"]{1}(?P<burrow>.+)['\"]{1}"
SECRET_WITH_QUOTES = {
    "name": "Line contains \"secret\" (within quotes)",
    "regex": SECRET_WITH_QUOTES_REGEX,
    "type": "filecontent",
    "multiline": False,
    "entropic": True
}

SECRET_WITHOUT_QUOTES_REGEX = r"s[e3]c[r4][e3]t\s*=+\s*(?P<burrow>[a-zA-Z0-9_\-+\/]+)"
SECRET_WITHOUT_QUOTES = {
    "name": "\"secret\" phrase",
    "regex": SECRET_WITHOUT_QUOTES_REGEX,
    "type": "filecontent",
    "multiline": False,
    "entropic": True
}

AWS_ACCESS_KEY_ID_REGEX = r"(?P<burrow>(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9]))"
AWS_ACCESS_KEY_ID = {
    "name": "AWS access key ID format",
    "regex": AWS_ACCESS_KEY_ID_REGEX,
    "type": "filecontent",
    "multiline": False,
    "entropic": True
}

AWS_SECRET_ACCESS_KEY_REGEX = r"(?P<burrow>(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=]))"
AWS_SECRET_ACCESS_KEY = {
    "name": "AWS secret key format",
    "regex": AWS_SECRET_ACCESS_KEY_REGEX,
    "type": "filecontent",
    "multiline": False,
    "entropic": True
}

BASIC_AUTH_REGEX = r"(?P<burrow>http[s]?:\/\/[a-zA-Z0-9]+:.+@[a-zA-Z0-9]+[a-zA-Z0-9./-]+)"
BASIC_AUTH = {
    "name": "Basic Authentication URL format",
    "regex": BASIC_AUTH_REGEX,
    # "variable_length": True,
    # "min_length": 4,
    "type": "filecontent",
    "multiline": False,
    "entropic": False
}

DJANGO_SECRET_KEY_REGEX = r"SECRET_KEY\s{0,1}=\s{0,1}['|\"](?P<burrow>.+)['|\"]"
DJANGO_SECRET_KEY = {
    "name": "Django secret key format",
    "regex": DJANGO_SECRET_KEY_REGEX,
    "type": "filecontent",
    "multiline": False,
    "entropic": True
}

PRIVATE_KEY_REGEX = r"-----BEGIN (?:RSA|OPENSSH) PRIVATE KEY-----.*----END (?:RSA|OPENSSH) PRIVATE KEY-----"
PRIVATE_KEY = {
    "name": "Private key format",
    "regex": PRIVATE_KEY_REGEX,
    "type": "filecontent",
    "multiline": True,
    "entropic": False
}

##### The below regular expresions are all for checking the name of a file.

BACKUP_FILE_REGEX = r".*backup.*"
BACKUP_FILE = {
    "name": "Filename contains \"backup\"",
    "regex": BACKUP_FILE_REGEX,
    "type": "filename"
}

DOTFILE_REGEX = r"[.](?:zsh|bash|mysql|psql|irb|profile)(?:_history|_profile|rc){0,1}"
DOTFILE = {
    "name": "Dotfile filename",
    "regex": DOTFILE_REGEX,
    "type": "filename"
}

DUMP_REGEX = r".*dump.*"
DUMP = {
    "name": "Filename contains \"dump\"",
    "regex": DUMP_REGEX,
    "type": "filename"
}

PRIVATE_KEY_FILE_REGEX = r".+[.](?:pem|key|p12)"
PRIVATE_KEY_FILE = {
    "name": "Private key file extension",
    "regex": PRIVATE_KEY_FILE_REGEX,
    "type": "filename"
}

SQL_FILE_REGEX = r".+[.]sql"
SQL_FILE = {
    "name": "SQL file extension",
    "regex": SQL_FILE_REGEX,
    "type": "filename"
}

##### The below is a list of the above checks.
ALL_REGEX_CHECKS = [
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    BASIC_AUTH,
    DJANGO_SECRET_KEY, 
    KEY_WITH_QUOTES,
    KEY_WITHOUT_QUOTES,  
    PRIVATE_KEY,
    SECRET_WITH_QUOTES,
    SECRET_WITHOUT_QUOTES,
    BACKUP_FILE,
    DOTFILE,
    DUMP,
    PRIVATE_KEY_FILE,
    SQL_FILE
]