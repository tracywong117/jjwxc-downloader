# jjwxc-downloader 晉江文學城小說下載器
<p align="center">
    <br> <a href="README.md">English</a> | 中文
</p>
這是一個用Python編寫的腳本，可以下載晉江文學城的小說免費章節。腳本支持下載txt和epub格式。僅供教育目的使用，請勿將其用於商業目的。

## 前提条件
- Google Chrome
- ChromeDriver（與Google Chrome版本相同）

你可以在設置中檢查Google Chrome的版本。

![google_chrome版本](check-chrome-version.png)

1. 在 https://googlechromelabs.github.io/chrome-for-testing 查看並下載最新版本的ChromeDriver。

2. 下載ChromeDriver的zip文件後，解壓並將chromedriver可執行文件放在jjwxc-downloader腳本的同一文件夾中。
```plaintext
jjwxc-downloader/
├─ jjwxc.py
├─ chromedriver
```
在Windows操作系統中，chromedriver的可執行文件應該命名為chromedriver.exe。

## 更新日誌
### 2024-01-08 新增
- 下載書籍封面
- 將.txt轉換為.epub
- 在.epub中包含書籍封面、目錄和元數據(書名、作者等資料) 

## 如何運行
1. 安裝依賴
```plaintext
pip3 install -r requirements.txt
```
2. 下載書籍的.txt格式和.epub格式以及書籍封面
```plaintext
python3 jjwxc-epub.py
```
或者只下載書籍的.txt格式和書籍封面
```plaintext
python3 jjwxc.py
```
3. 輸入你要下載的小說id

注意每個章節名稱前都加了##。這樣做是為了以後轉換txt到epub時方便添加索引。

## 未來工作
1. 添加從txt到epub的轉換 ✅
2. 添加圖形使用者介面(GUI)

如果你需要任何幫助，請添加issue。