import requests
from bs4 import BeautifulSoup
import re
import os
import urllib.parse
from jinja2 import Template

def scrape_ubereats_codes():
    url = "https://www.callingtaiwan.com.tw/ubereats優惠-最新餐廳外送首購優惠序號-折扣碼-推薦碼/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        codes = []
        
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')[1:]
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    expiry = cols[0].text.strip()
                    content = cols[1].text.strip()
                    code = cols[2].text.strip()
                    
                    code = re.sub(r'\s*\(.*?\)\s*', '', code)
                    
                    # 使用新的 URL Scheme
                    deep_link = f"ubereats://promo/apply?client_id=eats&promoCode={urllib.parse.quote(code)}"
                    
                    codes.append({
                        "expiry": expiry,
                        "content": content,
                        "code": code,
                        "deep_link": deep_link
                    })
        
        print(f"找到 {len(codes)} 個 UberEats 優惠碼")
        return codes
    except Exception as e:
        print(f"爬取 UberEats 優惠碼過程中出現錯誤: {e}")
        return []

def scrape_foodpanda_codes():
    url = "https://www.callingtaiwan.com.tw/foodpanda-coupon-code/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        codes = []
        
        coupon_table = soup.find('table', id='coupon_table')
        if coupon_table:
            rows = coupon_table.find_all('tr')[1:]  # 跳過表頭
            for row in rows:
                cells = row.find_all('td')
                if len(cells) == 3:
                    expiry_date = cells[0].text.strip()
                    content = cells[1].text.strip()
                    code_element = cells[2].find('a', class_='rdc_box_button')
                    
                    if code_element and 'data-code' in code_element.attrs:
                        code = code_element.text.strip()
                        
                        # 創建深層連結
                        deep_link = f"foodpanda://coupon?code={urllib.parse.quote(code)}"
                        
                        codes.append({
                            "expiry_date": expiry_date,
                            "content": content,
                            "code": code,
                            "deep_link": deep_link
                        })
        
        print(f"找到 {len(codes)} 個 Foodpanda 優惠碼")
        return codes
    except Exception as e:
        print(f"爬取 Foodpanda 優惠碼過程中出現錯誤: {e}")
        return []

def generate_html(ubereats_codes, foodpanda_codes):
    categories = {"UberEats": {}, "Foodpanda": {}}
    
    for code in ubereats_codes:
        category = re.search(r'【(.*?)】', code['content'])
        if category:
            category = category.group(1)
        else:
            category = '其他'
        
        if category not in categories["UberEats"]:
            categories["UberEats"][category] = []
        categories["UberEats"][category].append(code)
    
    for code in foodpanda_codes:
        category = re.search(r'【(.*?)】', code['content'])
        if category:
            category = category.group(1)
        else:
            category = '其他'
        
        if category not in categories["Foodpanda"]:
            categories["Foodpanda"][category] = []
        categories["Foodpanda"][category].append(code)
    
    html_template = """
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>外送平台優惠碼</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                line-height: 1.6; 
                padding: 10px; 
                margin: 0;
                background-color: #f0f0f0;
                color: #333;
                transition: background-color 0.3s, color 0.3s;
            }
            h1 { 
                text-align: center; 
                color: inherit;
            }
            .sidebar {
                width: 250px;
                background-color: #333;
                padding: 15px;
                color: white;
                height: 100vh;
                position: fixed;
                top: 0;
                left: 0;
                transform: translateX(-100%);
                transition: transform 0.3s ease;
                overflow-y: auto;
                z-index: 1000;
            }
            .sidebar a {
                color: white;
                text-decoration: none;
                display: block;
                padding: 10px 0;
            }
            .sidebar a:hover {
                background-color: #575757;
            }
            .content {
                margin-left: 0;
                padding: 20px;
                transition: margin-left 0.3s ease;
            }
            .content.shifted {
                margin-left: 250px;
            }
            .code-card {
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 15px;
                padding: 15px;
            }
            .code-card h2 {
                margin-top: 0;
                font-size: 1.2em;
                color: #444;
            }
            .code-card p {
                margin: 5px 0;
                font-size: 0.9em;
                color: #666;
            }
            .code {
                font-weight: bold;
                color: #e44d26;
            }
            .button {
                display: block;
                width: calc(100% - 30px); 
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 1em;
                cursor: pointer;
                text-align: center;
                text-decoration: none;
                background-color: #4CAF50;
                color: white;
                margin-top: 10px;
                margin: 0 auto;
            }
            .copied {
                background-color: #45a049;
            }
            .toggle-button {
                display: block;
                background-color: transparent;
                color: white;
                padding: 10px;
                text-align: center;
                cursor: pointer;
                margin-bottom: 10px;
                position: fixed;
                top: 10px;
                left: 10px;
                z-index: 1001;
            }
            .toggle-button div {
                width: 25px;
                height: 3px;
                background-color: #333;
                margin: 4px 0;
            }
            .divider {
                height: 1px;
                background-color: #575757;
                margin: 15px 0;
            }

            /* 深色模式 */
            @media (prefers-color-scheme: dark) {
                body {
                    background-color: #121212;
                    color: #ffffff; // 將字體顏色改為白色
                }
                h1, h2, h3, p {
                    color: #ffffff; // 將標題和段落文字顏色改為白色
                }
                .code-card {
                    background-color: #1e1e1e;
                }
                .code-card h2 {
                    color: #ffffff; // 將優惠碼標題顏色改為白色
                }
                .code-card p {
                    color: #dddddd; // 將段落文字顏色調亮
                }
                .code {
                    color: #ff7b7b; // 保持優惠碼顏色
                }
                .button {
                    color: #ffffff; // 按鈕文字顏色改為白色
                    background-color: #4CAF50; // 按鈕背景保持不變或根據需要調整
                }
                .sidebar {
                    background-color: #1e1e1e;
                    color: #ffffff; // 側邊欄文字顏色改為白色
                }
                .sidebar a {
                    color: #ffffff; // 側邊欄連結文字顏色改為白色
                }
            }


        </style>
    </head>
    <body>
        <div class="toggle-button" onclick="toggleSidebar()">
            <div></div>
            <div></div>
            <div></div>
        </div>
        <div class="sidebar" id="sidebar">
            <h2>外送平台優惠碼</h2>
            <h3>UberEats</h3>
            {% for category in categories["UberEats"] %}
                <a href="#UberEats-{{ category }}" onclick="toggleSidebar()">{{ category }}</a>
            {% endfor %}
            <div class="divider"></div>
            <h3>Foodpanda</h3>
            {% for category in categories["Foodpanda"] %}
                <a href="#Foodpanda-{{ category }}" onclick="toggleSidebar()">{{ category }}</a>
            {% endfor %}
        </div>
        <div class="content" id="content">
            <h1>外送平台優惠碼</h1>
            <h2 id="UberEats">UberEats</h2>
            {% for category, codes in categories["UberEats"].items() %}
                <h3 id="UberEats-{{ category }}">{{ category }}</h3>
                {% for code in codes %}
                    <div class="code-card">
                        <h2>{{ code.content }}</h2>
                        <p>優惠碼: <span class="code">{{ code.code }}</span></p>
                        <p>有效期限: {{ code.expiry }}</p>
                        <a href="{{ code.deep_link }}" class="button" onclick="copyCode('{{ code.code }}', this); return false;">複製優惠碼並開啟APP</a>
                    </div>
                {% endfor %}
            {% endfor %}
            <h2 id="Foodpanda">Foodpanda</h2>
            {% for category, codes in categories["Foodpanda"].items() %}
                <h3 id="Foodpanda-{{ category }}">{{ category }}</h3>
                {% for code in codes %}
                    <div class="code-card">
                        <h2>{{ code.content }}</h2>
                        <p>優惠碼: <span class="code">{{ code.code }}</span></p>
                        <p>有效期限: {{ code.expiry_date }}</p>
                        <a href="{{ code.deep_link }}" class="button" onclick="copyCode('{{ code.code }}', this); return false;">複製優惠碼並開啟APP</a>
                    </div>
                {% endfor %}
            {% endfor %}
        </div>
        <script>
            function toggleSidebar() {
                var sidebar = document.getElementById('sidebar');
                var content = document.getElementById('content');
                if (sidebar.style.transform === 'translateX(0%)') {
                    sidebar.style.transform = 'translateX(-100%)';
                    content.classList.remove('shifted');
                } else {
                    sidebar.style.transform = 'translateX(0%)';
                    content.classList.add('shifted');
                }
            }



            function copyCode(code, button) {
                navigator.clipboard.writeText(code).then(function() {
                    button.textContent = '已複製';
                    button.classList.add('copied');
                    setTimeout(function() {
                        button.textContent = '複製優惠碼並開啟APP';
                        button.classList.remove('copied');
                        window.location.href = button.href;
                    }, 500);
                }, function(err) {
                    console.error('無法複製文字: ', err);
                    window.location.href = button.href;
                });
                return false;
            }
        </script>
    </body>
    </html>
    """
    
    template = Template(html_template)
    html_content = template.render(categories=categories)
    
    filename = 'DeliveryCodes.html'
    
    current_dir = os.getcwd()
    print(f"當前工作目錄: {current_dir}")
    
    print("目錄內容:")
    for item in os.listdir(current_dir):
        print(item)
    
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"HTML 檔案已保存至: {os.path.join(current_dir, filename)}")
    except PermissionError:
        print(f"沒有權限寫入檔案: {filename}")
    except Exception as e:
        print(f"寫入檔案時發生錯誤: {e}")

if __name__ == "__main__":
    ubereats_codes = scrape_ubereats_codes()
    foodpanda_codes = scrape_foodpanda_codes()
    if ubereats_codes or foodpanda_codes:
        generate_html(ubereats_codes, foodpanda_codes)
    else:
        print("沒有找到優惠碼，不創建 HTML 檔案")
