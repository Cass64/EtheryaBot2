def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def get_loans_data():
    return read_json_file('data/prets.json')

def save_loans_data(data):
    write_json_file('data/prets.json', data)

def get_livret_a_data():
    return read_json_file('data/livret_a.json')

def save_livret_a_data(data):
    write_json_file('data/livret_a.json', data)

def get_entreprises_data():
    return read_json_file('data/entreprises.json')

def save_entreprises_data(data):
    write_json_file('data/entreprises.json', data)

def get_config_data():
    return read_json_file('data/config.json')

def save_config_data(data):
    write_json_file('data/config.json', data)