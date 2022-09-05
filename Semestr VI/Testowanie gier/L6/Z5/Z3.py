import inspect

def load_data(path):
    data = []
    now_read = False
    with open(path,encoding='utf-8') as file:
        for line in file:
            if inspect.stack()[1][3] in line:
                now_read = True
            elif len(line.split()) == 1:
                now_read = False
            if now_read:
                data.append((int(line.split()[0]),line.split()[1]))
    return data
