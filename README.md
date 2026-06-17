# 📈 StockGenius — KOPI AI 股票分析引擎 ☕

> ✨ **数据源负责事实，LLM 负责分析** ✨
>
> 一只会帮你分析股票的 AI 咖啡师 🤖☕

---

## 🎀 什么是 StockGenius？

StockGenius 是一只住在 KOPI 咖啡馆里的 AI 精灵 🧚‍♀️

你只要告诉它一个股票代码，它就会：
- 🔍 扫描 **8 大维度** 数据
- 📊 从 **SEC EDGAR** 抓真实财报
- 🤖 用 **MiMo 推理模型** 深度分析
- 📝 生成一份完整的投资分析报告

**不是 ChatGPT 幻觉，是真数据驱动！** 💪

---

## 🌟 Live Demo

| 版本 | 链接 |
|------|------|
| 🇨🇳 中文版 | [stockgenius.html](https://sub.readinghero.xyz/stockgenius.html) |
| 🇬🇧 English | [stockgenius-en.html](https://sub.readinghero.xyz/stockgenius-en.html) |
| 🐂🐻 Stock Swarm | [stock-swarm](https://sub.readinghero.xyz/stock-swarm/) |
| 📡 数据终端 | [tradecat](https://sub.readinghero.xyz/tradecat/) |

---

## 🎯 八维分析魔法

```
         📊 技术面
            │
   📰 消息面 ──┼── 🔥 社媒热度
            │
   💰 财务 ──┼── 👤 创始人
            │
   🏛️ 机构持仓 ──┼── 🌍 宏观经济
            │
         🎯 期权
            │
            ▼
     🤖 MiMo 推理模型
            │
            ▼
     📝 投资分析报告
```

| 维度 | 数据源 | 分析内容 |
|------|--------|----------|
| 📊 技术面 | Yahoo Finance | 股价、涨跌、成交量、52周高低 |
| 📰 消息面 | Wikipedia | 近期重大新闻、公司动态 |
| 🔥 社媒热度 | StockTwits | 散户情绪、消息量、热度趋势 |
| 💰 财务 | SEC EDGAR | 营收、净利、PE、EPS、现金流 |
| 👤 创始人 | Wikipedia | 管理层背景、领导力分析 |
| 🏛️ 机构持仓 | SEC 13F | Top 5 机构持仓变动 |
| 🌍 宏观经济 | FRED | 10Y国债、VIX、GDP、失业率 |
| 🎯 期权 | Yahoo Finance | Put/Call 比率、最大痛点 |

---

## 🛍️ 支持的股票 (100+)

### 🏗️ 科技巨头
`AAPL` 苹果 · `MSFT` 微软 · `GOOGL` 谷歌 · `AMZN` 亚马逊 · `NVDA` 英伟达 · `META` · `TSLA` 特斯拉

### 💰 金融大佬
`JPM` 摩根大通 · `V` Visa · `GS` 高盛 · `MS` 摩根士丹利 · `BAC` 美国银行 · `BLK` 贝莱德

### 🎮 科技新贵
`PLTR` Palantir · `COIN` Coinbase · `HOOD` Robinhood · `SHOP` Shopify · `SNOW` Snowflake

### 🚀 太空探索
`SPCX` SpaceX · `SPCU` 2X做多SpaceX · `RKLB` 火箭实验室 · `LUNR` 直觉机器 · `ASTS` AST太空移动

### 🍔 消费品牌
`KO` 可口可乐 · `PEP` 百事 · `MCD` 麦当劳 · `SBUX` 星巴克 · `NKE` 耐克 · `DIS` 迪士尼

### 📈 ETF指数
`VOO` 标普500 · `SPY` · `QQQ` 纳指100 · `IWM` 罗素2000 · `BITO` 比特币期货 · `IBIT` iShares比特币

> 💡 还有更多！支持搜索中文名：输入"苹果"就能找到 AAPL~

---

## 🐂🐻 Stock Swarm 多 Agent 辩论

```
                    ┌─────────────┐
                    │  📊 Data    │
                    │   Agent     │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ 🐂 Bull  │ │ 🐻 Bear  │ │ 🔮 Seer  │
        │  Agent   │ │  Agent   │ │  Agent   │
        └────┬─────┘ └────┬─────┘ └────┬─────┘
             │            │            │
             └────────────┼────────────┘
                          ▼
                   ┌─────────────┐
                   │ ⚖️ Judge    │
                   │   Agent     │
                   └─────────────┘
```

五个 AI 特工一起辩论一只股票：

| Agent | 角色 | 性格 |
|-------|------|------|
| 🐂 **Bull** | 看多 | 乐观派，找上涨理由 |
| 🐻 **Bear** | 看空 | 悲观派，找风险点 |
| 📊 **Data** | 数据 | 理性派，提供事实 |
| 🔮 **Seer** | 预言 | 未来派，预测趋势 |
| ⚖️ **Judge** | 裁决 | 公正派，综合判断 |

---

## 🎨 界面预览

```
┌────────────────────────────────────────────────────────┐
│  ✦ StockGenius          KOPI AI  [中] [EN]            │
├────────────────────────────────────────────────────────┤
│                                                        │
│  📈 StockGenius                                        │
│  📊 Kopi Stock 六维分析  📡 KOPI 数据终端  🚀 SpaceX   │
│                                                        │
│  ┌─────────────────────────────────────────────────┐  │
│  │ 美股 98  [🔍 搜索代码...                        ]│  │
│  ├─────────────────────────────────────────────────┤  │
│  │ AAPL 苹果    │  ┌─────────────────────────────┐│  │
│  │ MSFT 微软    │  │                             ││  │
│  │ GOOGL 谷歌   │  │    📊 TradingView 图表      ││  │
│  │ AMZN 亚马逊   │  │                             ││  │
│  │ NVDA 英伟达   │  │    K线 · 成交量 · 指标      ││  │
│  │ TSLA 特斯拉   │  │                             ││  │
│  │ ...          │  └─────────────────────────────┘│  │
│  └─────────────────────────────────────────────────┘  │
│                                                        │
│              [ 🚀 开始分析 ]                           │
│                                                        │
│  ┌─────────────────────────────────────────────────┐  │
│  │ 💰 SEC EDGAR 财务数据                            │  │
│  │ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐            │  │
│  │ │ 营收  │ │ 净利  │ │ PE   │ │ EPS  │            │  │
│  │ │$394B │ │$101B │ │33.2  │ │$6.58 │            │  │
│  │ └──────┘ └──────┘ └──────┘ └──────┘            │  │
│  │                                                 │  │
│  │ 📊 技术面  │ 📰 消息面  │ 🔥 社媒热度            │  │
│  │ 💰 财务    │ 👤 创始人  │ 🏛️ 机构持仓           │  │
│  │ 🌍 宏观    │ 🎯 期权                           │  │
│  │                                                 │  │
│  │ [AI 实时分析流式输出...]                          │  │
│  └─────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

---

## ✨ 功能特性

### 🖥️ 前端魔法
- 🌙 **暗色主题** — 咖啡 + 金色，KOPI 品牌色调
- 📱 **移动优先** — 手机上也能流畅使用
- 📊 **TradingView** — 专业 K 线图嵌入
- 🔄 **流式输出** — SSE 实时显示分析过程
- 🇨🇳🇬🇧 **双语支持** — 中英文一键切换
- 📋 **一键复制** — 分析结果秒复制
- 🔍 **智能搜索** — 支持代码和中文名搜索
- 📦 **100+ 股票** — 科技、金融、太空、消费全覆盖

### ⚙️ 后端引擎
- 🐍 **FastAPI** — 高性能 Python 异步框架
- 📡 **SEC EDGAR** — 真实 XBRL 财务数据
- 🤖 **MiMo V2.5** — 小米推理模型，深度分析
- 🔌 **SSE 流式** — Server-Sent Events 实时推送
- 🛡️ **数据管线** — 8 维数据自动采集 + 清洗
- ⏱️ **超时保护** — 120 秒超时，优雅降级

---

## 🚀 快速部署

### 1️⃣ 环境变量
```bash
# 创建 .env 文件
cat > .env << 'EOF'
MIMO_API=https://your-mimo-endpoint/v1
MIMO_KEY=your-api-key-here
ALPACA_KEY=your-alpaca-key      # 可选，期权数据
ALPACA_SECRET=your-alpaca-secret # 可选
EOF
```

### 2️⃣ 安装依赖
```bash
pip install fastapi uvicorn httpx
```

### 3️⃣ 启动后端
```bash
cd backend
python server.py  # 🎉 Port 8773
```

### 4️⃣ Nginx 配置
```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8773;
    proxy_read_timeout 300s;
    proxy_buffering off;  # SSE 流式必须！
}
```

### 5️⃣ Systemd 服务
```ini
[Unit]
Description=StockGenius Backend ☕
After=network.target

[Service]
WorkingDirectory=/root/stockgenius
ExecStart=python3 server.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## 📡 API 接口

### 分析股票
```bash
# 流式分析
curl -X POST http://localhost:8773/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'

# 返回 SSE 流
data: {"dim": "tech", "content": "📊 技术面分析..."}
data: {"dim": "news", "content": "📰 新闻摘要..."}
...
data: [DONE]
```

### 健康检查
```bash
curl http://localhost:8773/health
# {"status": "ok"}
```

---

## 🗂️ 项目结构

```
stockgenius/
├── README.md                 ← 你正在看的这个 📖
├── .gitignore
├── frontend/
│   ├── stockgenius.html      🇨🇳 中文版 (22KB)
│   └── stockgenius-en.html   🇬🇧 English (21KB)
├── backend/
│   └── server.py             ⚙️ FastAPI 后端 (468行)
├── stock-swarm/
│   └── index.html            🐂🐻 多Agent辩论 (14KB)
└── tradecat/
    ├── index.html            📡 数据终端
    ├── fred-proxy.py         🌍 FRED 经济数据代理
    └── fetch-fred.sh         📥 FRED 数据抓取
```

---

## 🏷️ Tech Stack

| 层级 | 技术 |
|------|------|
| 🎨 Frontend | Vanilla HTML/CSS/JS, TradingView Widget |
| ⚙️ Backend | Python 3.11, FastAPI, httpx |
| 🤖 LLM | MiMo V2.5 Pro (小米推理模型) |
| 📊 Data | Yahoo Finance, SEC EDGAR, StockTwits, FRED, Wikipedia |
| 🚀 Deploy | Nginx, Systemd, Ubuntu |

---

## 💡 设计哲学

```
┌─────────────────────────────────────────────┐
│                                             │
│   "数据源负责事实，LLM 负责分析"             │
│                                             │
│   ❌ 不要 LLM 幻觉                          │
│   ✅ 要真实数据管线                          │
│                                             │
│   ❌ 不要静态报告                            │
│   ✅ 要实时流式分析                          │
│                                             │
│   ❌ 不要单一维度                            │
│   ✅ 要八维全方位                            │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🤝 相关项目

- 🏠 [KOPI AI Agent](https://kopiaiagent.com) — 新加坡 Agentic AI 平台
- 📊 [Stock Swarm](https://sub.readinghero.xyz/stock-swarm/) — 多 Agent 辩论系统
- 📡 [KOPI 数据终端](https://sub.readinghero.xyz/tradecat/) — 实时经济数据

---

## 📄 License

MIT © [KOPI AI Agent PTE LTD](https://kopiaiagent.com)

---

<div align="center">

**☕ Made with ❤️ by KOPI AI in Singapore 🇸🇬**

*StockGenius — 让 AI 帮你看股票，喝咖啡的时间省下来~* ☕📈

</div>
