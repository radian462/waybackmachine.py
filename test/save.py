from waybackmachine import waybackmachine

wayback = waybackmachine(debug=True)
print(wayback.save('https://www.deepl.com/ja/translator'))