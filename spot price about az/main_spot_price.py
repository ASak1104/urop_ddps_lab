import os
import time
import boto3
import pickle
from multiprocessing import Manager
from pathos import multiprocessing as mp
from datetime import datetime, timedelta
from ec2_package import get_regions, store_spot_price
from update_base import update_base
from dotenv import load_dotenv
load_dotenv()


if __name__ == '__main__':
    start_time = time.time()
    # Need .env file
    access_key = os.environ.get('ACCESS_KEY')
    secret_key = os.environ.get('SECRET_KEY')

    session = boto3.session.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key)

    regions = get_regions(session)

    end_date = datetime.utcnow().replace(microsecond=0)
    start_date = end_date - timedelta(minutes=10)
    result = dict()

    manager = Manager()
    buffers = manager.list()
    args = [(buffers, session, region, start_date, end_date) for region in regions]

    pool = mp.Pool(processes=min(len(regions), mp.cpu_count() * 2, 6))
    for region in pool.imap(store_spot_price, args):
        print(f'{region} end at {int(time.time() - start_time)}s')
    pool.close()
    pool.join()

    for buffer in buffers:
        for it in buffer.keys():
            if it in result:
                for az, value in buffer[it].items():
                    result[it][az] = value
            else:
                result[it] = buffer[it]

    path = './spot history'
    try:
        os.chdir(path)
    except FileNotFoundError:
        os.mkdir(path)
        os.chdir(path)

    with open(f'{end_date}.bin', 'wb') as file:
        pickle.dump(result, file)

    base = update_base('base.bin')
    # print(len(base))

    print('end process, the running time is', f'{int(time.time() - start_time)}s')
