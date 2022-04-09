import os
import time
import boto3
import pickle
from ec2_package import *
from datetime import datetime, timedelta
from pathos import multiprocessing as mp
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

    end_date = datetime.now().replace(second=0, microsecond=0)
    start_date = end_date - timedelta(minutes=10)
    result = dict()

    buffers = [dict() for _ in range(len(regions))]
    args = [(buffer, session, region, start_date, end_date) for region, buffer in zip(regions, buffers)]

    pool = mp.Pool(processes=min(len(buffers), mp.cpu_count() * 3))
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

    print(f'end {int(time.time() - start_time)} s')

    with open(f"{end_date}.bin", 'wb') as file:
        pickle.dump(result, file)

    print('end process, the running time is', f'{int(time.time() - start_time)}s')
