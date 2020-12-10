import sys
import queue
import time
import crawler
import random
import csv
from itertools import islice
import concurrent.futures
import requests

q = queue.Queue()
completed = []

if len(sys.argv) > 3 and sys.argv[1] != None:
    uid_file = './raw_uid/' + sys.argv[1]
    PHPSESSID = sys.argv[3]
    result_filename = sys.argv[2] is not None and sys.argv[2] or 'data.csv'
    full_result_file_name = './data/' + result_filename

    with open(full_result_file_name, mode='w+',newline='',encoding='utf-8') as csv_file:
        fieldnames = ['uid', 'phone']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # read uid file
        with open(uid_file, 'r') as f:
            while True:
                next_5_lines = list(islice(f, 5))
                #process 5 lines
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    futures = []
                    for uid in next_5_lines:
                        futures.append(
                            executor.submit(
                                crawler.get_phone_by_uid, uid=uid, PHPSESSID=PHPSESSID, writer=writer
                            )
                        )
                    for future in concurrent.futures.as_completed(futures):
                        try:
                            print(future.result())
                        except requests.ConnectTimeout:
                            print("ConnectTimeout.")
                if not next_5_lines:
                    break


    # insert URL to the queue
    '''
    filename = sys.argv[2] is not None and sys.argv[2] or 'data.csv'
    full_file_name = './data/' + filename
    q.put(URL)
    total = 0
    with open(full_file_name, mode='w+',newline='',encoding='utf-8') as csv_file:
        fieldnames = ['#', 'name', 'address', 'landlines', 'mobile', 'email', 'website', 'social']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        while not q.empty():
            processcing_url = q.get()
            if processcing_url not in completed:
                data = crawler.crawl(processcing_url, q, completed)
                # total = total + len(data)
                for company in data:
                    total = total + 1
                    company['#'] = total
                    writer.writerow(company)

                print('...harvested %s item(s)' % len(data))
                if not q.empty():
                    t = random.randint(30, 65)
                    print('...delay for %s seconds...' % t)
                    time.sleep(t)

    print('Finished')
    print('Total items: %s' % total)
    '''
    exit()
else:
    print("Error! Command need arguments, eg: python main.py uid.txt result.csv PHPSESSION")
