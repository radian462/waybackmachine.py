[English](./README-EN.md)

# waybacktools
waybackmachineのpythonの非公式APIラッパー  
現在開発中

# 特徴
## **API Keyが不要**
このライブラリにはAPI Keyが必要ありません。

## **リソースの取得**
保存時にアーカイブのリソースを取得できます。

## **ダウンロード機能**
内部でPlaywrightを利用し、MHTML形式またはPDF形式でアーカイブをダウンロードできます。

# 導入
```bash
pip install waybacktools
playwright install
```

# 使い方
## 保存
```python
from waybacktools import waybackmachine

wayback = waybackmachine()
print(wayback.save('https://github.com'))
```
<details>
    <summary>ログ</summary>
    
```bash
    
```   
</details>
  
このようにサイトによっては膨大な量のログが流れるので、リソースログを隠したい場合はこのように書いてください。

```python
from waybacktools import waybackmachine
    
wayback = waybackmachine()
print(wayback.save('https://github.com',show_resources=False))
```


<details>
    <summary>ログ</summary>
```python
```
</details>

## 取得
```python
from waybacktools import waybackmachine

wayback = waybackmachine()
print(wayback.get('https://github.com/radian462/waybacktools'))
```

## ダウンロード
```python
from waybacktools import waybackmachine

wayback = waybackmachine()
print(wayback.download('https://github.com/radian462/waybacktools'))
```

# 実装予定
- [ ] asyncに対応
- [ ] 脱playwright
- [ ] 動作の安定化

# 開発者
- [radian462](https://github.com/radian462)