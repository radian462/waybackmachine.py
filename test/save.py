from waybacktools import waybackmachine

wayback = waybackmachine()
print(wayback.save('https://dmwiki.net'))