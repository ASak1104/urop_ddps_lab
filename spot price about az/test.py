import pickle


def is_same_dict(d0: dict, d1: dict, show=False) -> bool:
    def print_ex(*args):
        if show:
            print(args[0])
            for arg in args[1:]:
                print('\t', arg)
        return

    result = True
    if type(d0) != type(d1):
        print_ex('type differ', type(d0), type(d1))
        result = False
    elif len(d0) != len(d1):
        print_ex('length differ', len(d0), len(d1))
        result = False
    for k0, v0 in d0.items():
        if k0 not in d1:
            print_ex(f'key [{k0}] is not in second dict')
            result = False
        elif type(v0) != type(d1[k0]):
            print_ex(f'in key [{k0}], type of value differ', type(v0), type(d1[k0]))
            result = False
        elif type(v0) == dict:
            if not is_same_dict(v0, d1[k0], show=show):
                result = False
        elif v0 != d1[k0]:
            print_ex(f'in key [{k0}], value differ', v0, d1[k0])
            result = False
    return result


file00 = 'base.bin'
file01 = 'spot history/2022-04-12 02:48:06.bin'

with open(file00, 'rb') as file:
    data01 = pickle.load(file)

with open(file01, 'rb') as file:
    data02 = pickle.load(file)

print(f'diff {file00} {file01}')
print(data01 == data02)
print(is_same_dict(data01, data02, show=True))
