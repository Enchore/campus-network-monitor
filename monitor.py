#!/usr/bin/env python3
"""
校园网自动检测与登录工具
使用系统 Edge 浏览器，无需下载
"""

import json
import time
import sys
import os
import subprocess
import urllib.request
from datetime import datetime
from pathlib import Path

# 检查并安装依赖
def install_deps():
    try:
        import requests
    except ImportError:
        print("Installing requests...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests', '-q'])
    
    try:
        from selenium import webdriver
    except ImportError:
        print("Installing selenium...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'selenium', '-q'])
    
    try:
        from win32com.client import Dispatch
    except ImportError:
        print("Installing pywin32...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pywin32', '-q'])

install_deps()

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from win32com.client import Dispatch

# 配置文件路径
CONFIG_PATH = Path(__file__).parent / "config.json"
LOG_PATH = Path(__file__).parent / "monitor.log"
LOCK_PATH = Path(__file__).parent / ".monitor.lock"

class CampusNetworkMonitor:
    def __init__(self):
        self.config = self.load_config()
        self.running = False
        
    def load_config(self):
        """加载配置"""
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')
    
    def check_internet(self):
        """检测是否能访问外网"""
        try:
            # 尝试访问多个网站，避免误判
            urls = [
                'https://www.baidu.com',
                'https://www.qq.com',
                'https://www.bilibili.com',
            ]
            for url in urls:
                try:
                    response = requests.get(url, timeout=3, headers={'User-Agent': 'Mozilla/5.0'})
                    if response.status_code == 200:
                        return True
                except:
                    continue
            return False
        except:
            return False
    
    def login(self):
        """自动登录校园网"""
        self.log("开始自动登录...")
        driver = None
        
        try:
            # 使用 Edge 浏览器
            edge_options = Options()
            edge_options.add_argument('--start-maximized')
            
            driver = webdriver.Edge(options=edge_options)
            
            # 访问认证页面
            driver.get(self.config['campus']['authUrl'])
            self.log("已打开认证页面")
            time.sleep(3)
            
            # 填写用户名
            username_selectors = [
                '#username',
                'input[name="username"]',
                'input[name="user"]',
                'input[name="account"]',
                'input[type="text"]',
            ]
            
            # 截图保存页面结构
            screenshot_path = Path(__file__).parent / "page_debug.png"
            driver.save_screenshot(str(screenshot_path))
            self.log(f"已保存页面截图: {screenshot_path}")
            
            # 获取页面源码
            page_source = driver.page_source
            with open(Path(__file__).parent / "page_source.html", 'w', encoding='utf-8') as f:
                f.write(page_source)
            self.log("已保存页面源码")
            
            username_filled = False
            for selector in username_selectors:
                try:
                    elem = driver.find_element(By.CSS_SELECTOR, selector)
                    elem.clear()
                    elem.send_keys(self.config['campus']['username'])
                    username_filled = True
                    self.log(f"已填写用户名 (选择器: {selector})")
                    break
                except Exception as e:
                    self.log(f"用户名选择器 {selector} 失败: {e}")
                    continue
            
            # 填写密码 - 需要先点击密码区域显示输入框
            password_filled = False
            
            # 先尝试点击密码提示区域来显示密码输入框
            try:
                pwd_tip = driver.find_element(By.ID, 'pwd_tip')
                pwd_tip.click()
                self.log("已点击密码提示区域")
                time.sleep(0.5)
            except Exception as e:
                self.log(f"点击密码提示区域失败: {e}")
            
            # 再尝试点击密码容器
            try:
                pwd_div = driver.find_element(By.ID, 'pwdDiv')
                pwd_div.click()
                self.log("已点击密码输入区域")
                time.sleep(0.5)
            except Exception as e:
                self.log(f"点击密码容器失败: {e}")
            
            password_selectors = [
                '#pwd',
                'input[name="pwd"]',
                '#pwdDiv input',
                'input[type="password"]',
                'input[name="password"]',
                '#password',
            ]
            
            for selector in password_selectors:
                try:
                    elem = driver.find_element(By.CSS_SELECTOR, selector)
                    # 确保元素可见
                    driver.execute_script("arguments[0].style.display='block';", elem)
                    elem.clear()
                    elem.send_keys(self.config['campus']['password'])
                    password_filled = True
                    self.log(f"已填写密码 (选择器: {selector})")
                    break
                except Exception as e:
                    self.log(f"密码选择器 {selector} 失败: {e}")
                    continue
            
            # 选择运营商（中国电信）
            if username_filled and password_filled:
                try:
                    # 先点击服务选择下拉框
                    service_dropdown = driver.find_element(By.ID, 'xiala')
                    service_dropdown.click()
                    self.log("已点击运营商下拉框")
                    time.sleep(1)
                    
                    # 选择中国电信
                    telecom_option = driver.find_element(By.XPATH, "//div[contains(text(), '中国电信')]")
                    telecom_option.click()
                    self.log("已选择中国电信")
                    time.sleep(1)
                except Exception as e:
                    self.log(f"选择运营商失败: {e}")
                
                # 点击登录 - 根据页面源码使用正确的登录链接
                login_selectors = [
                    '#loginLink',
                    '#loginLink_div',
                    '#SLoginBtn_1 a',
                    '#login_btn_1 a',
                    'a[onclick*="doauthen"]',
                    'input[type="submit"]',
                    'button[type="submit"]',
                ]
                
                login_clicked = False
                for selector in login_selectors:
                    try:
                        elem = driver.find_element(By.CSS_SELECTOR, selector)
                        elem.click()
                        self.log(f"已点击登录 (选择器: {selector})")
                        login_clicked = True
                        break
                    except Exception as e:
                        self.log(f"登录按钮选择器 {selector} 失败: {e}")
                        continue
                
                if not login_clicked:
                    # 尝试使用 JavaScript 点击
                    try:
                        driver.execute_script("doauthen();")
                        self.log("已使用 JavaScript 调用 doauthen() 登录")
                    except Exception as e:
                        self.log(f"JavaScript 登录失败: {e}")
                
                # 等待登录完成
                time.sleep(5)
                
                # 检查是否成功
                if self.check_internet():
                    self.log("登录成功！关闭浏览器")
                    driver.quit()
                    return True
                else:
                    self.log("登录可能失败，保持浏览器打开")
                    time.sleep(30)
                    driver.quit()
                    return False
            else:
                self.log("未能找到输入框")
                time.sleep(30)
                driver.quit()
                return False
                
        except Exception as e:
            self.log(f"登录出错: {e}")
            import traceback
            self.log(f"错误详情: {traceback.format_exc()}")
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            return False
    
    def run(self):
        """主循环"""
        self.running = True
        self.log("=" * 50)
        self.log("校园网监控启动")
        self.log("=" * 50)
        
        # 首次检测
        self.log("首次检测网络状态...")
        if not self.check_internet():
            self.log("启动时检测到网络断开，开始登录...")
            self.login()
        else:
            self.log("网络正常")
        
        while self.running:
            try:
                # 检测网络
                if not self.check_internet():
                    self.log("网络断开，开始自动登录...")
                    self.login()
                    self.log("等待 2 分钟后再次检测...")
                    time.sleep(120)
                else:
                    self.log("网络正常")
                
                # 等待下次检测
                self.log("等待 30 秒后再次检测...")
                time.sleep(self.config['campus']['checkInterval'])
                
            except KeyboardInterrupt:
                self.log("收到停止信号")
                self.running = False
                break
            except Exception as e:
                self.log(f"运行出错: {e}")
                time.sleep(60)
        
        self.log("监控已停止")


def add_to_startup():
    """添加到开机启动"""
    try:
        startup_path = Path(os.environ['APPDATA']) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        target = Path(__file__).parent / "start.vbs"
        shortcut_path = startup_path / "校园网监控.lnk"
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.Targetpath = str(target)
        shortcut.WorkingDirectory = str(target.parent)
        shortcut.save()
        return True
    except Exception as e:
        print(f"添加开机启动失败: {e}")
        return False


def remove_from_startup():
    """从开机启动移除"""
    try:
        startup_path = Path(os.environ['APPDATA']) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        shortcut_path = startup_path / "校园网监控.lnk"
        if shortcut_path.exists():
            shortcut_path.unlink()
        return True
    except:
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--install', action='store_true', help='添加到开机启动')
    parser.add_argument('--uninstall', action='store_true', help='从开机启动移除')
    args = parser.parse_args()
    
    if args.install:
        if add_to_startup():
            print("已添加到开机启动")
        return
    
    if args.uninstall:
        if remove_from_startup():
            print("已从开机启动移除")
        return
    
    # 检查是否已运行
    if LOCK_PATH.exists():
        return
    
    LOCK_PATH.touch()
    
    try:
        monitor = CampusNetworkMonitor()
        monitor.run()
    finally:
        if LOCK_PATH.exists():
            LOCK_PATH.unlink()


if __name__ == "__main__":
    main()
