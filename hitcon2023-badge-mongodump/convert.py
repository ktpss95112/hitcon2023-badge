import os

for (dirpath, dirnames, filenames) in os.walk('.'):
    for file in filenames:
        path = os.path.join(dirpath, file)
        if not path.endswith('.bson'): continue

        os.system(f'docker run -v $(realpath .):/data -w /data --rm mongo:6.0 bsondump --outFile={file}.json {path}')
