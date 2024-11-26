from waybacktools import waybacktools

wayback = waybacktools()
print(wayback.download("https://www.google.co.jp/",path="./test/file/%(title)s - %(timestamp)s.%(ext)s",))
