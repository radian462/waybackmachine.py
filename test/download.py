from waybacktools import waybackmachine

wayback = waybackmachine()
print(
    wayback.download(
        "https://www.google.co.jp/",
        path="./test/file/%(title)s - %(timestamp)s.%(ext)s",
    )
)
