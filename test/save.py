from pprint import pprint
from waybacktools import waybacktools

wayback = waybacktools()
pprint(wayback.save("https://www.google.co.jp/"), sort_dicts=False)
