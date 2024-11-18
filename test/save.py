from waybacktools import waybackmachine

wayback = waybackmachine()
print(wayback.save('https://www.google.co.jp/',show_resources=False))