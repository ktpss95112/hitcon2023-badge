# TODO: this code is so dirty ...

from script.create_db_prod import CardReaderType, gen_readers

l = [
    (reader.id, dt, emoji)
    for reader in gen_readers()
    if reader.type == CardReaderType.SPONSOR
    for dt, emoji in reader.time_emoji
]

data = {}

for reader, time, emoji in l:
    if reader not in data:
        data[reader] = {}
    data[reader][time] = emoji

table = [list(data.keys())]
for time in data[table[0][0]].keys():
    ll = [time] + [data[reader][time] for reader in table[0]]
    table.append(ll)

table[0] = [""] + table[0]

for line in table:
    print(*map(str, line), sep=",")
