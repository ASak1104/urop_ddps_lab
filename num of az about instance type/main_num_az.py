import time
import boto3
import os
import pickle
from datetime import datetime
from ec2_package import *
from collections import Counter
from dotenv import load_dotenv
load_dotenv()

# Need .env file
access_key = os.environ.get('ACCESS_KEY')
secret_key = os.environ.get('SECRET_KEY')

start = time.time()

session = boto3.session.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key)

regions = get_regions(session)
print(f'total {len(regions)} regions')

counter = Counter()
for idx, region in enumerate(regions):
    print(f'{idx + 1}/{len(regions)} {region}')

    for it in get_it_az(session, region):
        counter += {(region, it): 1}

result = dict()
for key, cnt in counter.items():
    region, it = key
    if it in result:
        result[it].append((region, cnt))
    else:
        result[it] = [(region, cnt)]

with open(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.bin", 'wb') as file:
    pickle.dump(result, file)

print('end process, the running time is', f'{int(time.time() - start)}s')

