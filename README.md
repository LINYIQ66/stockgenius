# 📈 StockGenius — KOPI AI 股票分析引擎

七维 AI 股票分析平台，数据驱动而非 LLM 幻觉。

> **数据源负责事实，LLM 负责分析**

## 🔗 Live Demo

- 🇨🇳 [中文版](https://sub.readinghero.xyz/stockgenius.html)
- 🇬🇧 [English](https://sub.readinghero.xyz/stockgenius-en.html)
- 📊 [Stock Swarm 多 Agent 辩论](https://sub.readinghero.xyz/stock-swarm/)

## 📐 架构

```
┌─────────────────────────────────────────────────┐
│  Frontend (static HTML)                         │
│  stockgenius.html / stockgenius-en.html         │
│  TradingView Charts · Dark Theme · Mobile       │
└───────────────┬─────────────────────────────────┘
                │ POST /api/analyze
                ▼
┌─────────────────────────────────────────────────┐
│  Backend (FastAPI) — server.py :8773            │
│                                                 │
│  七维数据管线 (7-Dimension Pipeline):            │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐           │
│  │ 行情 │ │ 新闻 │ │ 财务 │ │ 机构 │           │
│  └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘           │
│  ┌──────┐ ┌──────┐ ┌──────┐                    │
│  │ 社媒 │ │ 宏观 │ │ 期权 │                    │
│  └──┬───┘ └──┬───┘ └──┬───┘                    │
│     └────────┴────────┘                         │
│              │                                  │
│              ▼                                  │
│     MiMo V2.5 Pro (推理模型)                    │
│     七维 prompt → 投资分析报告                   │
└─────────────────────────────────────────────────┘
```

## 🗂 项目结构

```
stockgenius/
├── README.md
├── frontend/
│   ├── stockgenius.html      # 中文版主页
│   └── stockgenius-en.html   # English 版主页
├── backend/
│   └── server.py             # FastAPI 后端 (七维数据管线 + LLM 分析)
├── stock-swarm/
│   └── index.html            # Stock Swarm 多 Agent 辩论系统
└── tradecat/
    ├── index.html            # KOPI 数据终端
    ├── fred-proxy.py         # FRED 经济数据代理
    └── fetch-fred.sh         # FRED 数据抓取脚本
```

## 🚀 功能特性

### 七维分析
| 维度 | 数据源 | 内容 |
|------|--------|------|
| 📈 行情 | Yahoo Finance | 股价、涨跌、成交量、52周高低 |
| 📰 新闻 | Wikipedia + StockTwits | 近期新闻、社媒情绪 |
| 💰 财务 | SEC EDGAR | 营收、净利、PE、EPS 等关键指标 |
| 🏛 机构 | SEC 13F | 机构持仓变动 (Top 5) |
| 💬 社媒 | StockTwits | 散户情绪、消息量 |
| 🌍 宏观 | FRED | 10Y国债、VIX、GDP、失业率 |
| 📊 期权 | Yahoo Finance | Put/Call 比率、最大痛点 |

### 前端特性
- 🌙 暗色主题 + 咖啡金色调 (KOPI 品牌)
- 📱 移动端优先响应式设计
- 📊 TradingView 高级图表嵌入
- 🔄 实时流式输出 (SSE)
- 🇨🇳🇬🇧 中英双语支持
- 📋 一键复制分析结果

### Stock Swarm
多 Agent 辩论系统：
- 🐂 Bull Agent — 看多论证
- 🐻 Bear Agent — 看空论证
- 📊 Data Agent — 数据研究
- 🔮 Seer Agent — 预测未来
- ⚖️ Judge Agent — 综合裁决

## 🛠 部署

### 环境变量
```bash
# MiMo API (LLM 推理)
MIMO_API=https://your-mimo-endpoint/v1
MIMO_KEY=your-api-key
```

### 启动后端
```bash
pip install fastapi uvicorn httpx
cd backend
python server.py  # Port 8773
```

### Nginx 配置
```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8773;
    proxy_read_timeout 300s;
    proxy_buffering off;
}
```

### Systemd 服务
```ini
[Unit]
Description=StockGenius Backend
After=network.target

[Service]
WorkingDirectory=/root/stockgenius
ExecStart=python3 server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## 📡 API Endpoints

```
POST /api/analyze
  Body: { "ticker": "AAPL" }
  Returns: SSE stream of 七维分析报告

GET  /health
  Returns: { "status": "ok" }
```

## 🏷 Tech Stack

- **Frontend**: Vanilla HTML/CSS/JS, TradingView Widget
- **Backend**: Python 3.11, FastAPI, httpx
- **LLM**: MiMo V2.5 Pro (小米 MiMo 推理模型)
- **Data**: Yahoo Finance, SEC EDGAR, StockTwits, FRED, Wikipedia
- **Deploy**: Nginx, Systemd, Ubuntu

## 📄 License

MIT © KOPI AI Agent PTE LTD
