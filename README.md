# my-webpages
# 優惠碼爬蟲與生成 HTML 頁面

此專案包含兩個 Python 腳本，分別用於爬取 UberEats 和 Foodpanda 的優惠碼，並生成對應的 HTML 頁面。

## 目錄結構
├── ubereats_scraper_mobile.py
├── foodpanda_scraper_mobile.py
└── README.md
## 需求

- Python 3.x
- requests
- BeautifulSoup4
- jinja2

可以使用以下命令安裝所需的 Python 套件：

bash
pip install requests beautifulsoup4 jinja2
## 使用說明

### UberEats 優惠碼爬蟲

`ubereats_scraper_mobile.py` 腳本會爬取 UberEats 的優惠碼並生成 HTML 頁面。

#### 執行步驟

1. 執行腳本：

    ```bash
    python ubereats_scraper_mobile.py
    ```

2. 腳本會爬取優惠碼並生成一個 HTML 檔案，保存至指定的路徑。預設路徑為 `//Dog_NAS/docker/UbereatsCode/UbereatsCode.html`。

### Foodpanda 優惠碼爬蟲

`foodpanda_scraper_mobile.py` 腳本會爬取 Foodpanda 的優惠碼並生成 HTML 頁面。

#### 執行步驟

1. 執行腳本：

    ```bash
    python foodpanda_scraper_mobile.py
    ```

2. 腳本會爬取優惠碼並生成一個 HTML 檔案，保存至指定的路徑。預設路徑為 `//Dog_NAS/docker/UbereatsCode/FoodpandaCode.html`。

## 腳本說明

### `ubereats_scraper_mobile.py`

- `scrape_ubereats_codes()`: 爬取 UberEats 優惠碼的函數，返回優惠碼列表。
- `generate_html(codes)`: 根據優惠碼列表生成 HTML 頁面並保存至指定路徑。

### `foodpanda_scraper_mobile.py`

- `scrape_foodpanda_codes()`: 爬取 Foodpanda 優惠碼的函數，返回優惠碼列表。
- `generate_html(codes)`: 根據優惠碼列表生成 HTML 頁面並保存至指定路徑。

## 注意事項

- 請確保網路連線正常，以便腳本能夠成功爬取優惠碼。
- 如果需要更改 HTML 檔案的保存路徑，請修改腳本中的 `filename` 變數。
