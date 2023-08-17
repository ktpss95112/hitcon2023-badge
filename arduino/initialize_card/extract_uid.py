import re


def main():
    with open('recv.log', 'r') as fp:
        content = fp.read()

    all_uid = set()
    for match in re.finditer(r"uid=b'[a-f0-9]{8}'\n", content):
        uid_hex = match.group()[6:-2]
        all_uid.add(uid_hex)

    print(*all_uid, sep='\n')


if __name__ == '__main__':
    main()
