import yfinance as yf
import datetime

# 가져올 티커 설정
tickers = {
    'VIX (공포지수)': '^VIX',
    'WTI 원유 선물': 'CL=F',
    '필라델피아 반도체': '^SOX',
    '원/달러 환율': 'KRW=X'
}

results = []

for name, symbol in tickers.items():
    try:
        data = yf.Ticker(symbol).history(period='5d')
        if len(data) >= 2:
            curr_price = data['Close'].iloc[-1]
            prev_price = data['Close'].iloc[-2]
            
            diff = curr_price - prev_price
            rate = (diff / prev_price) * 100
            
            results.append({
                'name': name,
                'price': round(curr_price, 2),
                'diff': round(diff, 2),
                'rate': round(rate, 2)
            })
    except Exception as e:
        print(f"Error fetching {name}: {e}")

# HTML 템플릿 작성
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

rows_html = ""
for r in results:
    color = "#d63031" if r['rate'] > 0 else ("#0984e3" if r['rate'] < 0 else "#636e72")
    sign = "+" if r['rate'] > 0 else ""
    
    rows_html += f"""
    <tr>
        <td style="padding: 12px; font-weight: bold;">{r['name']}</td>
        <td style="padding: 12px; text-align: right;">{r['price']:,}</td>
        <td style="padding: 12px; text-align: right; color: {color}; font-weight: bold;">
            {sign}{r['diff']} ({sign}{r['rate']}%)
        </td>
    </tr>
    """

html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>주요 시장 지표 동향</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8f9fa; display: flex; justify-content: center; padding: 40px 20px; }}
        .card {{ background: white; padding: 24px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); width: 100%; max-width: 500px; }}
        h2 {{ margin-top: 0; font-size: 20px; color: #2d3436; border-bottom: 2px solid #edf2f7; padding-bottom: 12px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        tr {{ border-bottom: 1px solid #edf2f7; }}
        .update-time {{ font-size: 12px; color: #b2bec3; text-align: right; margin-top: 16px; }}
    </style>
</head>
<body>
    <div class="card">
        <h2>📊 주요 해외 지수 & 선물 동향</h2>
        <table>
            <thead>
                <tr style="color: #718096; font-size: 13px; text-align: left;">
                    <th style="padding: 8px 12px;">종목</th>
                    <th style="padding: 8px 12px; text-align: right;">현재가</th>
                    <th style="padding: 8px 12px; text-align: right;">전일대비</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        <div class="update-time">최종 업데이트: {now}</div>
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("index.html 생성 완료!")
