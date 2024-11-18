from pprint import pprint
from waybacktools import waybackmachine

wayback = waybackmachine()
pprint(wayback.save("https://www.google.co.jp/"), sort_dicts=False)
