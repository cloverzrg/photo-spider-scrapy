import re


def format_key(key):
    key = key.lower().strip()
    key = re.sub(r'[ ]{2,}', " ", key)
    verify = re.findall(r'^[a-zA-Z][a-zA-Z \',0-9\-.]+[a-zA-Z]$', key)
    if len(verify) == 0:
        key2 = re.findall(r'[a-zA-Z][a-zA-Z \',0-9\-.]+[a-zA-Z]', key)
        if len(key2) == 0:
            return False
        else:
            return key2[0]
    else:
        return key


if __name__ == "__main__":
    key = format_key("  one    people   ")
    print(key)