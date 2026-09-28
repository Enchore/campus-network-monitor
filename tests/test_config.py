"""配置文件校验。

注意：这里刻意不 import monitor.py —— 它在模块顶层就调用 install_deps()，
会尝试 pip 安装 pywin32（Windows 专用），在 Linux CI 上必然失败。
它的语法正确性由 CI 里的 compileall 步骤负责。
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(ROOT, "config.example.json")


def test_example_config_is_valid_json():
    with open(CONFIG, encoding="utf-8") as f:
        config = json.load(f)

    campus = config["campus"]

    assert isinstance(campus["checkInterval"], int)
    assert campus["checkInterval"] > 0
    assert campus["authUrl"].startswith("http")


def test_example_config_contains_no_real_credentials():
    with open(CONFIG, encoding="utf-8") as f:
        campus = json.load(f)["campus"]

    # 示例配置里只能是占位符，真实学号/密码写在本地 config.json（已被 .gitignore 忽略）
    assert campus["username"] == "你的学号"
    assert campus["password"] == "你的密码"


def test_real_config_is_gitignored():
    gitignore = os.path.join(ROOT, ".gitignore")

    with open(gitignore, encoding="utf-8") as f:
        ignored = f.read()

    assert "config.json" in ignored
