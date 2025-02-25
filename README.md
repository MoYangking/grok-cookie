# Grok Cookie 获取器

这个项目通过自动化工具获取 Grok.com 的 Cookie，并定期发布到 GitHub Releases。

## 功能特点

- 使用 Selenium 和 Chrome WebDriver 自动访问 Grok.com
- 获取站点 Cookie 并保存为 JSON 格式
- 通过 GitHub Actions 自动运行并发布结果
- 默认每次获取 50 个 Cookie
- 每周自动更新

## 使用方法

### 手动运行

1. 克隆仓库
2. 安装依赖：`pip install -r requirements.txt`
3. 运行脚本：`python getCookie.py`

### 通过 GitHub Actions 使用

1. Fork 此仓库
2. 启用 GitHub Actions
3. 可以手动触发 workflow 或等待自动运行（每周日）
4. 在仓库的 Releases 页面下载最新的 Cookie 文件

## 文件说明

- `getCookie.py` - 主要脚本，用于获取 Cookie
- `.github/workflows/grok_cookie.yml` - GitHub Actions workflow 配置
- `requirements.txt` - 项目依赖

## 注意事项

- 使用 Cookie 时请遵守 Grok.com 的服务条款
- 此工具仅用于学习和研究目的
- 获取的 Cookie 有效期可能有限 