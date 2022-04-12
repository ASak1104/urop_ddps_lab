import os
import pickle
from glob import glob
# from pprint import pprint


def update_base(base_file_name: str) -> dict:
    recent_file_name = ''
    for file_name in glob('2*.bin'):
        recent_file_name = max(recent_file_name, file_name)
    # print(recent_file_name)

    recent = None
    try:
        with open(recent_file_name, 'rb') as file:
            recent = pickle.load(file)
    except FileNotFoundError as e:
        print(e)
        recent = dict()

    os.chdir('../')
    with open(base_file_name, 'wb') as file:
        pickle.dump(recent, file)

    return recent

    # for it, az_dic in recent.items():
    #     if it not in base:
    #         base[it] = az_dic
    #         continue
    #     for az, os_dic in az_dic.items():
    #         if az not in base[it]:
    #             base[it][az] = os_dic
    #             continue
    #         for os, p_t_dict in os_dic.items():
    #             if os not in base[it][az]:
    #                 base[it][az][os] = p_t_dict
    #                 continue
    #             if base[it][az][os]['timestamp'] < p_t_dict['timestamp']:
    #                 base[it][az][os] = p_t_dict

    # pprint(base)
    # print(len(base))
