#!/usr/bin/env python3
"""StockGenius — KOPI AI 七维股票分析引擎
数据管线：行情|新闻|财务|机构|社媒|宏观|期权
数据源负责事实，LLM 负责分析
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os, httpx, json, re, asyncio
from datetime import datetime

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_headers=["*"], allow_methods=["*"])

MIMO_API = os.getenv("MIMO_API", "https://token-plan-sgp.xiaomimimo.com/v1")
MIMO_KEY = os.getenv("MIMO_KEY", "")

# ═══════════════════════════════════════════════
# TICKER MAPS
# ═══════════════════════════════════════════════

TICKER_COMPANY = {
    "AAPL": "Apple_Inc.", "MSFT": "Microsoft", "GOOGL": "Alphabet_Inc.", "GOOG": "Alphabet_Inc.",
    "AMZN": "Amazon_(company)", "META": "Meta_Platforms", "TSLA": "Tesla,_Inc.",
    "NVDA": "Nvidia", "INTC": "Intel", "AMD": "Advanced_Micro_Devices",
    "BABA": "Alibaba_Group", "NFLX": "Netflix", "ADBE": "Adobe_Inc.",
    "CRM": "Salesforce", "ORCL": "Oracle_Corporation", "QCOM": "Qualcomm",
    "PYPL": "PayPal", "UBER": "Uber", "SQ": "Block,_Inc.",
    "DIS": "The_Walt_Disney_Company", "BA": "The_Boeing_Company", "JPM": "JPMorgan_Chase",
    "V": "Visa_Inc.", "WMT": "Walmart", "JNJ": "Johnson_%26_Johnson",
    "KO": "The_Coca-Cola_Company", "PEP": "PepsiCo", "WFC": "Wells_Fargo",
    "C": "Citigroup", "GM": "General_Motors", "F": "Ford_Motor_Company",
    "XOM": "ExxonMobil", "CVX": "Chevron_Corporation", "IBM": "IBM",
    "CSCO": "Cisco", "PLTR": "Palantir_Technologies",
    "SNOW": "Snowflake_Inc.", "DDOG": "Datadog", "CRWD": "CrowdStrike",
    "MRNA": "Moderna", "PFE": "Pfizer", "GME": "GameStop",
    "AMC": "AMC_Theatres", "RIVN": "Rivian", "LCID": "Lucid_Group",
    "COIN": "Coinbase", "HOOD": "Robinhood_Markets", "SNAP": "Snap_Inc.",
    "PINS": "Pinterest", "SPOT": "Spotify", "ZM": "Zoom_Video_Communications",
    "DOCU": "DocuSign", "MDB": "MongoDB", "NIO": "NIO_Inc.",
    "LI": "Li_Auto", "XPEV": "XPeng", "TSM": "TSMC",
    "SAP": "SAP_SE", "BIDU": "Baidu", "JD": "JD.com",
    "PDD": "PDD_Holdings", "SE": "Sea_Limited", "SHOP": "Shopify",
}

TICKER_CIK = {
    "AAPL":"0000320193","MSFT":"0000789019","GOOGL":"0001652044","GOOG":"0001652044",
    "AMZN":"0001018724","META":"0001326801","TSLA":"0001318605","NVDA":"0001045810",
    "INTC":"0000050863","AMD":"0000002488","NFLX":"0001065280","ADBE":"0000796343",
    "CRM":"0001108524","ORCL":"0001341439","QCOM":"0000804328","PYPL":"0001633917",
    "UBER":"0001543151","DIS":"0001744489","BA":"0000012927","JPM":"0000019617",
    "V":"0001403161","WMT":"0000104169","JNJ":"0000200406","KO":"0000021344",
    "PEP":"0000077476","WFC":"0000072971","C":"0000831001","GM":"0001467858",
    "F":"0000037996","XOM":"0000034088","CVX":"0000093410","IBM":"0000051143",
    "CSCO":"0000858877","PLTR":"0001321655","SNOW":"0001640147","DDOG":"0001561550",
    "CRWD":"0001535527","MRNA":"0001682852","PFE":"0000078003","GME":"0001326380",
    "AMC":"0001411579","RIVN":"0001874178","LCID":"0001811210","COIN":"0001679788",
    "HOOD":"0001783879","SNAP":"0001564408","PINS":"0001506293","SPOT":"0001639920",
    "ZM":"0001585521","DOCU":"0001261333","MDB":"0001441816","NIO":"0001606798",
    "LI":"0001791708","XPEV":"0001810997","TSM":"0001123412","SAP":"0001003812",
    "BIDU":"0001373327","JD":"0001549105","PDD":"0001737803","SE":"0001324404",
    "SHOP":"0001594805",
}

# ═══════════════════════════════════════════════
# DATA PIPELINES
# ═══════════════════════════════════════════════

async def get_price(symbol):
    """① 行情 — Alpaca 实时"""
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(
                f"https://data.alpaca.markets/v2/stocks/{symbol}/snapshot?feed=iex",
                headers={"APCA-API-KEY-ID": os.getenv("ALPACA_KEY", ""),
                         "APCA-API-SECRET-KEY": os.getenv("ALPACA_SECRET", "")}
            )
            if r.status_code == 200:
                d = r.json()
                t = d.get("latestTrade", {}); b = d.get("dailyBar", {}); p = d.get("prevDailyBar", {})
                price = t.get("p", b.get("c"))
                prev = p.get("c", price or 0)
                return {
                    "price": price, "prev_close": prev,
                    "high": b.get("h", 0), "low": b.get("l", 0),
                    "volume": b.get("v", 0), "change_pct": ((price-prev)/prev*100) if price and prev else 0
                }
    except: pass
    return {"price": None, "prev_close": 0, "high": 0, "low": 0, "volume": 0, "change_pct": 0}

async def get_news(symbol):
    """② 新闻 — Alpaca News"""
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(
                f"https://data.alpaca.markets/v1beta1/news?symbols={symbol}&limit=3&sort=desc",
                headers={"APCA-API-KEY-ID": os.getenv("ALPACA_KEY", ""),
                         "APCA-API-SECRET-KEY": os.getenv("ALPACA_SECRET", "")}
            )
            if r.status_code == 200:
                return [n.get("headline","") for n in r.json().get("news",[]) if n.get("headline")]
    except: pass
    return []

async def get_financials(symbol):
    """③ 财务 — SEC EDGAR companyfacts"""
    cik = TICKER_CIK.get(symbol)
    if not cik: return {}
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(
                f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json",
                headers={"User-Agent": "StockGenius/1.0 (contact@kopi.ai)"}
            )
            if r.status_code == 200:
                facts = r.json().get("facts",{}).get("us-gaap",{})
                result = {}
                def latest_val(key):
                    units = facts.get(key,{}).get("units",{}).get("USD",[])
                    return units[-1] if units else None
                rev = latest_val("RevenueFromContractWithCustomerExcludingAssessedTax") or latest_val("Revenues")
                if rev: result["revenue"] = {"val": rev["val"], "fy": rev["fy"], "fp": rev["fp"]}
                ni = latest_val("NetIncomeLoss")
                if ni: result["net_income"] = {"val": ni["val"], "fy": ni["fy"], "fp": ni["fp"]}
                eps = facts.get("EarningsPerShareBasic",{}).get("units",{}).get("USD/shares",[])
                if eps: result["eps"] = {"val": eps[-1]["val"], "fy": eps[-1]["fy"], "fp": eps[-1]["fp"]}
                assets = latest_val("Assets")
                if assets: result["total_assets"] = assets["val"]
                cash = latest_val("CashAndCashEquivalentsAtCarryingValue") or latest_val("Cash")
                if cash: result["cash"] = cash["val"]
                ocf = latest_val("NetCashProvidedByOperatingActivities")
                if ocf: result["op_cash_flow"] = ocf["val"]
                ebitda = latest_val("EarningsBeforeInterestTaxesDepreciationAndAmortization")
                if ebitda: result["ebitda"] = ebitda["val"]
                return result
    except: pass
    return {}

async def get_social(symbol):
    """④ 社媒 — Stocktwits"""
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")
            if r.status_code == 200:
                d = r.json()
                msgs = d.get("messages",[])
                watchers = d.get("symbol",{}).get("watchlist_count",0)
                bullish = sum(1 for m in msgs if m.get("entities") and m["entities"].get("sentiment") and m["entities"]["sentiment"].get("basic") == "Bullish")
                bearish = sum(1 for m in msgs if m.get("entities") and m["entities"].get("sentiment") and m["entities"]["sentiment"].get("basic") == "Bearish")
                likes = sum(m.get("likes",{}).get("total",0) for m in msgs[:20])
                top_bodies = [m.get("body","")[:120] for m in msgs[:5]]
                return {
                    "watchers": watchers, "messages_30m": len(msgs),
                    "bullish": bullish, "bearish": bearish,
                    "likes_20": likes, "top_messages": top_bodies
                }
    except: pass
    return {}

async def get_macro():
    """⑤ 宏观 — 免费宏观数据聚合"""
    results = {}
    # DXY from free API
    try:
        async with httpx.AsyncClient(timeout=8) as c:
            r = await c.get("https://api.exchangerate-api.com/v4/latest/USD")
            if r.status_code == 200:
                results["dxy_base"] = "USD index base"
    except: pass
    # 10Y yield scrape
    try:
        async with httpx.AsyncClient(timeout=8) as c:
            r = await c.get("https://query1.finance.yahoo.com/v8/finance/chart/%5ETNX?range=1d&interval=1d",
                headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200:
                d = r.json()
                meta = d.get("chart",{}).get("result",[{}])[0].get("meta",{})
                results["10y_yield"] = meta.get("regularMarketPrice")
                prev_close = meta.get("previousClose")
                if prev_close and results["10y_yield"]:
                    results["10y_change"] = round(results["10y_yield"] - prev_close, 3)
    except: pass
    # Oil price
    try:
        async with httpx.AsyncClient(timeout=8) as c:
            r = await c.get("https://query1.finance.yahoo.com/v8/finance/chart/CL=F?range=1d&interval=1d",
                headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200:
                d = r.json()
                meta = d.get("chart",{}).get("result",[{}])[0].get("meta",{})
                results["crude_oil"] = meta.get("regularMarketPrice")
    except: pass
    # VIX
    try:
        async with httpx.AsyncClient(timeout=8) as c:
            r = await c.get("https://query1.finance.yahoo.com/v8/finance/chart/%5EVIX?range=1d&interval=1d",
                headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200:
                d = r.json()
                meta = d.get("chart",{}).get("result",[{}])[0].get("meta",{})
                results["vix"] = meta.get("regularMarketPrice")
    except: pass
    # CPI latest (scrape from FRED quick)
    try:
        async with httpx.AsyncClient(timeout=8) as c:
            r = await c.get("https://query1.finance.yahoo.com/v8/finance/chart/CPIAUCNS?range=1mo&interval=1d",
                headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200:
                d = r.json()
                result = d.get("chart",{}).get("result",[{}])[0]
                quotes = result.get("indicators",{}).get("quote",[{}])[0].get("close",[])
                timestamps = result.get("timestamp",[])
                if quotes and timestamps:
                    # Find latest non-null value
                    for i in range(len(quotes)-1, -1, -1):
                        if quotes[i]:
                            results["cpi"] = quotes[i]
                            results["cpi_date"] = timestamps[i]
                            break
    except: pass
    return results

async def get_institutional(symbol):
    """⑥ 机构持仓 — 基于 Stocktwits 数据 + 信息"""
    # Stocktwits watcher count is a proxy for retail interest
    # For real 13F data, we'd use SEC filings or Nasdaq Data Link
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")
            if r.status_code == 200:
                d = r.json()
                watchers = d.get("symbol",{}).get("watchlist_count",0)
                return {"watchlist_count": watchers}
    except: pass
    return {}

async def get_options(symbol):
    """⑦ 期权 — Yahoo Finance (need cookie sometimes)"""
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(
                f"https://query1.finance.yahoo.com/v7/finance/options/{symbol}",
                headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
            )
            if r.status_code == 200:
                d = r.json()
                opt = d.get("optionChain",{}).get("result",[{}])[0]
                options = opt.get("options",[{}])[0]
                calls = options.get("calls",[])
                puts = options.get("puts",[])
                if calls and puts:
                    call_oi = sum(c.get("openInterest",0) for c in calls)
                    put_oi = sum(p.get("openInterest",0) for p in puts)
                    max_oi_call = max(calls, key=lambda x: x.get("openInterest",0))
                    max_oi_put = max(puts, key=lambda x: x.get("openInterest",0))
                    return {
                        "call_oi": call_oi, "put_oi": put_oi,
                        "pc_ratio": round(put_oi/call_oi, 2) if call_oi > 0 else 0,
                        "max_call_strike": max_oi_call.get("strike"),
                        "max_call_oi": max_oi_call.get("openInterest"),
                        "max_put_strike": max_oi_put.get("strike"),
                        "max_put_oi": max_oi_put.get("openInterest"),
                        "near_price_call_iv": calls[0].get("impliedVolatility"),
                        "near_price_put_iv": puts[0].get("impliedVolatility"),
                    }
    except: pass
    return {}

async def get_wikipedia_ceo(symbol):
    """CEO 事实 — Wikipedia infobox"""
    name = TICKER_COMPANY.get(symbol, symbol)
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            resp = await c.get(f"https://en.wikipedia.org/wiki/{name}",
                headers={"User-Agent": "StockGenius/1.0", "Accept": "text/html"})
            if resp.status_code == 200:
                html = resp.text
                li_start = html.find('<li>')
                while li_start >= 0:
                    li_end = html.find('</li>', li_start)
                    if li_end < 0: break
                    li_content = html[li_start:li_end]
                    li_start = html.find('<li>', li_start + 1)
                    if 'CEO' in li_content or 'chief executive' in li_content.lower():
                        paren = li_content.find('(')
                        if paren > 0:
                            name_text = li_content[4:paren]
                            name_text = re.sub(r'<[^>]+>', '', name_text).strip()
                            if name_text: return f"Current CEO: {name_text}"
    except: pass
    return ""

# ═══════════════════════════════════════════════
# PROMPT BUILDER
# ═══════════════════════════════════════════════

def fmt(val, unit="", div=1):
    if val is None: return "N/A"
    if unit == "$" and isinstance(val, (int,float)):
        if abs(val) >= 1e9: return f"${val/1e9:.2f}B"
        if abs(val) >= 1e6: return f"${val/1e6:.2f}M"
        return f"${val:,.2f}"
    if isinstance(val, (int,float)):
        return f"{val:,}"
    return str(val)

@app.post("/api/stock/analyze")
async def analyze(request: Request):
    body = await request.json()
    symbol = body.get("symbol", "AAPL").strip().upper()
    lang = body.get("lang", "zh")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    today = datetime.now().strftime("%Y-%m-%d")

    # ═══ 并行抓取所有数据管线 ═══
    price_d, news_h, fin, social, macro, inst, opts = await asyncio.gather(
        get_price(symbol),
        get_news(symbol),
        get_financials(symbol),
        get_social(symbol),
        get_macro(),
        get_institutional(symbol),
        get_options(symbol),
    )
    ceo_fact = await get_wikipedia_ceo(symbol)

    # ═══ 构建事实上下文 ═══
    ctx = f"Today: {today}\nTicker: {symbol} ({TICKER_COMPANY.get(symbol, symbol)})\n"

    # ① 行情
    p = price_d.get("price")
    if p:
        chg = price_d.get("change_pct",0)
        ctx += f"Price: ${p:.2f} ({chg:+.2f}%)\n"
        ctx += f"Daily: H${price_d['high']:.2f} L${price_d['low']:.2f} Vol{price_d['volume']:,}\n"

    # ② 新闻
    if news_h:
        ctx += "News:\n" + "\n".join(f"- {h}" for h in news_h) + "\n"

    # ③ 财务
    if fin:
        ctx += "\nFinancials (SEC EDGAR):\n"
        if "revenue" in fin:
            r = fin["revenue"]
            ctx += f"- Revenue: ${r['val']/1e9:.2f}B ({r['fy']} {r['fp']})\n"
        if "net_income" in fin:
            ni = fin["net_income"]
            ctx += f"- Net Income: ${ni['val']/1e9:.2f}B ({ni['fy']} {ni['fp']})\n"
        if "eps" in fin:
            ctx += f"- EPS: ${fin['eps']['val']:.2f} ({fin['eps']['fy']} {fin['eps']['fp']})\n"
        if "total_assets" in fin:
            ctx += f"- Total Assets: ${fin['total_assets']/1e9:.2f}B\n"
        if "cash" in fin:
            ctx += f"- Cash: ${fin['cash']/1e9:.2f}B\n"
        if "op_cash_flow" in fin:
            ctx += f"- Operating Cash Flow: ${fin['op_cash_flow']/1e9:.2f}B\n"
        if "ebitda" in fin:
            ctx += f"- EBITDA: ${fin['ebitda']/1e9:.2f}B\n"
    else:
        ctx += "\nFinancials: SEC EDGAR data unavailable for this ticker\n"

    # ④ 社媒
    if social:
        ctx += f"\nSocial (Stocktwits):\n"
        ctx += f"- Watchers: {social.get('watchers',0):,}\n"
        ctx += f"- Messages (30min): {social.get('messages_30m',0)}\n"
        ctx += f"- Sentiment: {social.get('bullish',0)} bullish / {social.get('bearish',0)} bearish\n"
        ctx += f"- Recent chatter: " + " | ".join(social.get('top_messages',[])) + "\n"

    # ⑤ 宏观
    if macro:
        ctx += f"\nMacro:\n"
        if "10y_yield" in macro:
            ctx += f"- 10Y Yield: {macro.get('10y_yield')}%"
            if "10y_change" in macro:
                ctx += f" ({macro['10y_change']:+.3f}bp)"
            ctx += "\n"
        if "crude_oil" in macro:
            ctx += f"- Crude Oil: ${macro['crude_oil']:.2f}\n"
        if "vix" in macro:
            ctx += f"- VIX: {macro['vix']:.2f}\n"
        if "cpi" in macro:
            ctx += f"- CPI: {macro['cpi']:.1f}\n"
    else:
        ctx += "\nMacro: data unavailable\n"

    # ⑥ 机构
    if inst:
        ctx += f"\nInstitutional:\n- Stocktwits Watchlist: {inst.get('watchlist_count',0):,}\n"
    else:
        ctx += "\nInstitutional: data unavailable\n"

    # ⑦ 期权
    if opts:
        ctx += f"\nOptions:\n"
        ctx += f"- Put/Call OI Ratio: {opts.get('pc_ratio',0):.2f}\n"
        ctx += f"- Max Pain Call: ${opts.get('max_call_strike','N/A')} (OI: {opts.get('max_call_oi','N/A')})\n"
        ctx += f"- Max Pain Put: ${opts.get('max_put_strike','N/A')} (OI: {opts.get('max_put_oi','N/A')})\n"
        ctx += f"- Near ATM Call IV: {opts.get('near_price_call_iv','N/A')}\n"
        ctx += f"- Near ATM Put IV: {opts.get('near_price_put_iv','N/A')}\n"
    else:
        ctx += "\nOptions: data unavailable\n"

    # CEO
    if ceo_fact:
        ctx += f"\n{ceo_fact}\n"

    # ═══ LLM Prompt ═══
    lang_instr = "Chinese main + English key terms. No markdown." if lang == "zh" else "English only. No Chinese characters. No markdown."
    user_prompt = f"""Analyze {symbol} using ONLY the data below. Your training data is OUTDATED.

=== REAL-TIME DATA ({today}) ===
{ctx}

=== INSTRUCTIONS ===
Return ONLY valid JSON with these fields (4-6 detailed sentences each, with specific numbers):

- signal: 看涨/看跌/震荡
- risk: 低/中/高
- technical: Support/resistance levels from price data, volume analysis, intraday pattern. Use actual H/L prices.
- news: How EACH news headline affects this company's specific business lines. If no news, say so.
- social: Stocktwits sentiment, message volume, bullish/bearish ratio. If no data, say unavailable.
- financial: SEC-sourced revenue, net income, EPS, cash position. Calculate PE if price+EPS available. If no data, say unavailable.
- founder: CEO name from Wikipedia. If no data, say unavailable.
- funds: Institutional interest from watchlist data. If no data, say unavailable.
- macro: How 10Y yield, oil, VIX, CPI affect this stock. If no data, say unavailable.
- options: Put/Call ratio, max pain, IV analysis. If no data, say unavailable.
- strategy: Entry/stop-loss/target prices with reasoning based on ALL dimensions above. 5-7 sentences.

{lang_instr}"""

    try:
        async with httpx.AsyncClient(timeout=120) as c:
            resp = await c.post(
                f"{MIMO_API}/chat/completions",
                json={"model":"mimo-v2.5","messages":[{"role":"system","content":"JSON only. Today is "+today+". Use ONLY the data provided. Output JSON directly, no reasoning."},{"role":"user","content":user_prompt}],"max_tokens":8192,"temperature":0.3},
                headers={"Authorization": f"Bearer {MIMO_KEY}"}
            )
            text = resp.json()["choices"][0]["message"]["content"]
            text = re.sub(r'^```(?:json)?[\s]*', '', text.strip())
            text = re.sub(r'[\s]*```$', '', text)
            m = re.search(r'\{[\s\S]*\}', text)
            data = json.loads(m.group()) if m else {}
    except:
        data = {}

    return {
        "symbol": symbol, "timestamp": now_str,
        "price": p,
        "change": f"${p:.2f} ({price_d.get('change_pct',0):+.2f}%)" if p else "N/A",
        "high": price_d.get("high",0), "low": price_d.get("low",0), "volume": price_d.get("volume",0),
        "news_headlines": news_h,
        "signal": data.get("signal", "震荡"),
        "risk": data.get("risk", "中"),
        "strategy": data.get("strategy", "-"),
        "technical": data.get("technical", "-"),
        "news": data.get("news", "-"),
        "social": data.get("social", "-"),
        "financial": data.get("financial", "-"),
        "founder": data.get("founder", "-"),
        "funds": data.get("funds", "-"),
        "macro": data.get("macro", "-"),
        "options": data.get("options", "-"),
    }

if __name__ == "__main__":
    import uvicorn, asyncio
    uvicorn.run(app, host="0.0.0.0", port=8773)
