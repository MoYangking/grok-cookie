import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random  # 添加random模块导入


def get_grok_cookie(count=50):  # 默认设置为50
    """
    启动Chrome浏览器，通过无痕窗口访问grok.com，获取Cookie

    Args:
        count (int): 获取Cookie的次数，默认为50

    Returns:
        list: 获取的Cookie列表
    """
    all_cookies = []

    # 创建存储文件夹
    if not os.path.exists("cookies"):
        os.makedirs("cookies")

    for i in range(1, count + 1):
        print(f"正在获取第 {i}/{count} 个Cookie...")

        # 设置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument("--incognito")  # 无痕模式
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 禁用标识
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")  # 添加无头模式，适合CI环境
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # 添加更真实的用户代理
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

        # 启动Chrome浏览器
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)

            # 修改WebDriver属性，避免被检测
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en']})")

            # 打开grok.com
            driver.get("https://grok.com")

            # 等待页面加载完成（等待任意一个元素出现）
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                # 给网页额外的加载时间
                time.sleep(5)
                
                
                # 尝试与页面进行一些交互
                try:
                    # 查找并点击指定的<div>元素
                    interaction_div = driver.find_element(By.CSS_SELECTOR, "div.relative.z-10")
                    interaction_div.click()
                    print("已点击交互区域")
                    time.sleep(2)  # 等待交互效果
                except Exception as e:
                    print(f"无法找到或点击交互区域: {e}")
                
                # 继续其他交互
                driver.execute_script("window.scrollTo(0, 300)")
                time.sleep(1)
                driver.execute_script("window.scrollTo(300, 600)")
                time.sleep(1)
                
            except Exception as e:
                print(f"等待页面加载超时: {e}")

            # 获取所有cookie
            cookies = driver.get_cookies()

            # 格式化cookie字符串
            cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

            # 将cookie添加到列表
            if cookie_str:
                all_cookies.append(cookie_str)
                print(f"成功获取Cookie（长度: {len(cookie_str)}）")
                print(f"获取的Cookie: {cookie_str[:50]}...{cookie_str[-50:] if len(cookie_str) > 100 else cookie_str[50:]}")

                # 将Cookie保存到单独的文件
                with open(f"cookies/cookie_{i}.txt", "w") as f:
                    f.write(cookie_str)
            else:
                print("未能获取有效的Cookie")

        except Exception as e:
            print(f"获取Cookie过程中出错: {e}")

        finally:
            # 关闭浏览器
            try:
                driver.quit()
                print("已关闭浏览器")
            except Exception as e:
                print(f"关闭浏览器时出错: {e}")

            # 在两次获取之间稍作暂停
            if i < count:
                delay = random.randint(5, 10)  # 随机延迟5-10秒
                print(f"等待 {delay} 秒后继续...")
                time.sleep(delay)

    # 将所有Cookie保存到一个总文件
    cookies_dict = {
        "cookies": all_cookies,
        "last_cookie_index": {
            "grok-2": 0,
            "grok-3": 0,
            "grok-3-thinking": 0
        },
        "temporary_mode": True
    }

    with open("cookies/all_cookies.json", "w") as f:
        json.dump(cookies_dict, f, indent=2)

    print(f"\n总计获取了 {len(all_cookies)} 个Cookie")
    print(f"所有Cookie已保存到 cookies/all_cookies.json")

    return all_cookies


if __name__ == "__main__":
    # 硬编码获取50个Cookie
    cookies = get_grok_cookie(50)

    # 显示结果
    if cookies:
        print("\n获取到的Cookie列表:")
        for i, cookie in enumerate(cookies, 1):
            # 显示截断的cookie以便于查看
            truncated = cookie[:50] + "..." + cookie[-50:] if len(cookie) > 100 else cookie
            print(f"{i}. {truncated}")