# 校园网自动监控与登录工具

[![CI](https://github.com/Enchore/campus-network-monitor/actions/workflows/ci.yml/badge.svg)](https://github.com/Enchore/campus-network-monitor/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

一个基于 Python + Selenium 的校园网自动监控工具，支持断网自动检测和自动登录。

## 功能特点

- 🔍 **自动检测网络状态** - 定时检测网络连接
- 🔄 **断网自动重连** - 检测到断网后自动打开浏览器登录
- 🖥️ **后台静默运行** - 使用 VBS 脚本实现无窗口后台运行
- 🚀 **开机自动启动** - 可配置开机自动启动
- 🌐 **多运营商支持** - 支持选择不同运营商（中国电信/移动/联通等）

## 环境要求

- Windows 10/11
- Python 3.8+
- Microsoft Edge 浏览器
- 以下 Python 包：
  ```
  pip install requests selenium pywin32
  ```

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/Enchore/campus-network-monitor.git
cd campus-network-monitor
```

### 2. 安装依赖

```bash
pip install requests selenium pywin32
```

### 3. 配置账号信息

复制配置文件模板：

```bash
copy config.example.json config.json
```

编辑 `config.json`，填入你的校园网账号信息：

```json
{
  "campus": {
    "authUrl": "http://10.192.5.3",
    "username": "你的学号",
    "password": "你的密码",
    "operator": "中国电信",
    "checkInterval": 30
  }
}
```

**配置说明：**
- `authUrl` - 校园网认证页面地址
- `username` - 学号/工号
- `password` - 登录密码
- `operator` - 运营商（中国电信/中国移动/中国联通/校园网）
- `checkInterval` - 网络检测间隔（秒）

### 4. 运行监控

#### 方式一：后台运行（推荐）

双击 `start_hidden.vbs`，程序将在后台静默运行。

#### 方式二：前台运行（调试用）

```bash
python monitor.py
```

### 5. 停止监控

双击 `stop_monitor.bat` 停止后台运行的监控程序。

## 开机自动启动

### 方法一：启动文件夹（推荐）

1. 按 `Win + R`，输入 `shell:startup`，回车
2. 将 `start_hidden.vbs` 复制到打开的文件夹中
3. 重启电脑，监控程序将自动后台运行

### 方法二：任务计划程序

1. 打开"任务计划程序"
2. 创建基本任务
3. 触发器选择"当用户登录时"
4. 操作选择"启动程序"，浏览选择 `start_hidden.vbs`

## 文件说明

| 文件 | 说明 |
|------|------|
| `monitor.py` | 主程序，包含网络检测和自动登录逻辑 |
| `start_hidden.vbs` | 后台启动脚本（无窗口） |
| `stop_monitor.bat` | 停止监控脚本 |
| `config.json` | 配置文件（需要自行创建） |
| `config.example.json` | 配置文件模板 |
| `monitor.log` | 运行日志（自动生成） |

## 日志查看

运行日志保存在 `monitor.log` 文件中，可以查看网络检测和登录记录：

```
[2026-04-03 21:34:09] 校园网监控启动
[2026-04-03 21:34:09] 网络正常
[2026-04-03 21:34:39] 网络正常
[2026-04-03 21:35:09] 网络断开，开始自动登录...
[2026-04-03 21:35:15] 登录成功！关闭浏览器
```

## 适配说明

本工具目前适配 **西华大学** 校园网认证系统（认证地址：http://10.192.5.3）。

如果您的学校使用不同的认证系统，可能需要修改 `monitor.py` 中的以下部分：

1. **认证页面 URL** - 修改 `config.json` 中的 `authUrl`
2. **输入框选择器** - 根据页面源码修改 CSS 选择器：
   - 用户名输入框：`#username`, `input[name="username"]`
   - 密码输入框：`#pwd`, `input[name="pwd"]`
   - 登录按钮：`#loginLink`, `a[onclick*="doauthen"]`
3. **运营商选择** - 修改 XPath 或添加点击逻辑

## 注意事项

1. **安全性**：配置文件包含明文密码，请妥善保管，不要上传到公共仓库
2. **Edge 浏览器**：确保系统已安装 Microsoft Edge 浏览器
3. **网络权限**：首次运行可能需要允许防火墙访问
4. **多实例**：不要同时运行多个实例，避免冲突

## 常见问题

### Q: 程序无法启动？
A: 检查是否已安装依赖包，以及 Python 是否在环境变量中。

### Q: 无法找到输入框？
A: 可能是认证页面结构不同，需要根据实际情况修改 CSS 选择器。

### Q: 登录失败？
A: 检查账号密码是否正确，以及运营商选择是否匹配。

### Q: 如何彻底卸载？
A: 删除程序文件夹，并从启动文件夹中删除 `start_hidden.vbs`。

## 技术栈

- Python 3.8+
- Selenium WebDriver
- Microsoft Edge WebDriver
- VBScript

## 许可证

MIT License

Copyright (c) 2026 Enchore

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 贡献指南

非常感谢您对本项目的关注！如果您有任何建议或想法，欢迎通过以下方式参与：

### 提交 Issue
如果您在使用过程中遇到问题，或有新的功能建议，欢迎提交 Issue。请在提交时尽可能详细地描述问题或建议，这将帮助我们更好地理解和处理。

### 提交 Pull Request
如果您想为项目贡献代码，我们非常欢迎：

1. **Fork 仓库** - 点击右上角的 "Fork" 按钮，将仓库复制到您的账号下
2. **创建分支** - 在您的 Fork 中创建一个新的分支进行修改
3. **提交更改** - 完成修改后，提交到您的分支
4. **发起 PR** - 向我们发起 Pull Request，我们会尽快进行审核

### 联系方式
如有任何问题，欢迎通过邮件联系：lwp1246@gmail.com

再次感谢您的支持与贡献！

## 更新日志

### v1.0.0 (2026-04-03)
- 初始版本发布
- 支持自动检测和登录
- 支持后台运行和开机启动
