import pickle


def is_same_dict(d0: dict, d1: dict) -> bool:
    if type(d0) != type(d1):
        print('type differ')
        print(type(d0), type(d1))
        return False
    if len(d0) != len(d1):
        print('length differ')
        print(len(d0), len(d1))
        return False
    for k0, v0 in d0.items():
        if k0 not in d1:
            print(f'key [{k0}] is not in second dict')
            return False
        if type(v0) != type(d1[k0]):
            print(f'in key [{k0}], type of value differ')
            print(type(v0), type(d1[k0]))
            return False
        if type(v0) == dict:
            if not is_same_dict(v0, d1[k0]):
                return False
        elif v0 != d1[k0]:
            print(f'in key [{k0}], value differ')
            print(v0, d1[k0])
            return False
    return True


with open("2022-04-09 17:02:00.bin", 'rb') as file:
    data01 = pickle.load(file)

with open("2022-04-09 17:14:00.bin", 'rb') as file:
    data02 = pickle.load(file)

print(is_same_dict(data01, data02))
print(data01 == data02)
