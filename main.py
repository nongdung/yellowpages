import sys
import queue
import time
import crawler
import random
import csv

q = queue.Queue()
completed = []

if len(sys.argv) > 1 and sys.argv[1] != None:
    URL = sys.argv[1]
    # insert URL to the queue
    filename = sys.argv[2] is not None and sys.argv[2] or 'data.csv'
    full_file_name = './data/' + filename
    q.put(URL)
    total = 0
    with open(full_file_name, mode='w+',newline='',encoding='utf-8') as csv_file:
        fieldnames = ['#', 'name', 'address', 'city', 'phone', 'email', 'website', 'category']
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
                    t = random.randint(10, 15)
                    print('...delay for %s seconds...' % t)
                    time.sleep(t)

    print('Finished')
    print('Total items: %s' % total)
    exit()
else:
    print("Error! Command need a url, eg: python2 crawler.py https://yourdomain.com")
