# BrillianceLab — 完整 Setup 手冊

從零到「全自動跑」的 step-by-step。預估時間:**約 90 分鐘**(含等待第三方 email 認證)。

---

## 0. 一次性 — 本機環境(5 min)

```bash
cd BrillianceLab

# 安裝 pre-commit hook(每次 commit 自動跑 JSON-LD/canonical/JS check)
sh build/git-hooks/install.sh         # macOS / Linux / Git Bash
build\git-hooks\install.bat           # Windows cmd

# 確認驗證可跑
python build/scripts/check_js.py
python build/scripts/audit_canonicals.py
```

---

## 1. Google Analytics 4(15 min,優先做)

**為什麼最優先**:沒有 GA4,Web Vitals / scroll / outbound / bookmark / A/B test 全部資料丟掉。

1. https://analytics.google.com → **建立帳戶 / 資源**
2. 屬性類型:**Web** · 屬性名稱:**BrillianceLab**
3. 時區:**台灣** · 幣別:**TWD**
4. 選「業務目標」:Generate leads + Examine user behavior
5. 「資料串流」→ **新增串流** → Web → URL:`https://brilliancelab.vercel.app`
6. 複製 **「測量 ID」**(格式 `G-XXXXXXXXXX`)
7. 在 BrillianceLab/ 跑:
   ```bash
   python build/scripts/set_ga4.py G-你的真ID
   ```
   這會自動把 index.html 裡的 `G-XXXXXXXXXX` 換成你的 ID 並 uncomment 整段 gtag block。
8. `deploy.bat` 推上去 → 開 https://brilliancelab.vercel.app/ → DevTools Network 應該看到 `google-analytics.com/collect` 在發送

**驗證資料進來**:GA4 → 報表 → 即時 → 應該看到自己的 session(可能要等 30 秒)

---

## 2. Google Search Console(10 min)

1. https://search.google.com/search-console → **新增資源**
2. 選 **「網址前置字元」**(不是「網域」,domain 需要 DNS,比較麻煩)
3. 輸入 `https://brilliancelab.vercel.app/` → **繼續**
4. 驗證方法選 **「HTML 標記」** → 應該秒驗(因為 token `ptLFsBUrBRXmB3HiFIGEK0GO4wOijz03YSWPrDtwfDg` 已經寫在 index.html)
5. 進去後 → 左側 **「Sitemap」** → 輸入 `sitemap.xml` → **提交**
   - GSC 會自動展開 sitemap-index 抓到 4 個子 sitemap
   - 24-48h 後「涵蓋範圍」報表會出現第一筆數據
6. **(關鍵)手動 Request Indexing** — GSC 有限制,每天約 10 次:
   - 「網址檢查」→ 貼 URL → 「要求建立索引」
   - 5 天分批,參考下面這份順序:

### Day 1(核心 5 篇)
```
https://brilliancelab.vercel.app/
https://brilliancelab.vercel.app/blog/master-guide
https://brilliancelab.vercel.app/blog/gia-guide
https://brilliancelab.vercel.app/blog/diamond-faq
https://brilliancelab.vercel.app/blog/budget-formula
```

### Day 2(5 個 silo hub)
```
https://brilliancelab.vercel.app/blog/hub-fundamentals
https://brilliancelab.vercel.app/blog/hub-4cs
https://brilliancelab.vercel.app/blog/hub-purchase
https://brilliancelab.vercel.app/blog/hub-proposal
https://brilliancelab.vercel.app/blog/hub-care
```

### Day 3(基礎深度 10 篇)
```
hearts-arrows-truth · lab-vs-natural · cert-comparison
diamond-color · diamond-clarity · diamond-shapes · diamond-carat-size
round-cut-deep-dive · fancy-cuts-guide · fluorescence-deep-dive
```

### Day 4(購買實戰 10 篇)
```
engagement-guide · diamond-scams · diamond-financing · secondhand-rings
moissanite-vs-cz-vs-lab · proposal-speech · ring-sizing
wedding-bands · wedding-metals · engagement-timeline
```

### Day 5(剩下的長尾)
```
diamond-care · ring-insurance · diamond-resale · diamond-news-2026
inclusions-types-guide · prong-settings-guide · engraving-personalization
mens-engagement-rings · heirloom-redesign · diamond-fun-facts
```

剩下的(famous-diamonds, sustainable-diamonds 等)就交給 sitemap 自動 crawl。

---

## 3. Bing Webmaster Tools(5 min)

1. https://www.bing.com/webmasters → 用 Microsoft 帳號登入
2. **加入網站** → `https://brilliancelab.vercel.app/`
3. **驗證** → HTML Meta Tag 方式,應該秒驗(token `E0C80549746F44CC7041C29DBBE89452` 已寫好)
4. **Sitemaps** → Submit `https://brilliancelab.vercel.app/sitemap.xml`

**Bing 的好消息**:你已經有 IndexNow,不用手動 request indexing。當天跑這個指令一次:
```bash
python build/scripts/ping_indexnow.py --all
```
Bing/Yandex/Seznam/Naver **2-24 小時內**會 indexing。

---

## 4. GitHub Actions 自動化(10 min)

3 個 workflow 已經寫好,只需要在 GitHub 上「啟用」:

1. 把 BrillianceLab/ push 到 GitHub(`deploy.bat` 已經做這件事)
2. 開 https://github.com/expertise88864/brilliancelab/actions
3. 第一次進去會看到「Workflows are disabled」→ 按 **「I understand my workflows, go ahead and enable them」**
4. 立刻會看到 4 個 workflow:
   - **Validate** — 每次 push/PR 跑(JSON-LD + canonical + JS check)
   - **Monthly Report** — 每月 1 號 02:00 UTC 自動跑
   - **IndexNow weekly** — 每週一 01:00 UTC 自動跑
   - **IndexNow on push** — 每次 push 自動偵測變動 URL 推送

**手動測一次 Monthly Report**:
- Actions → Monthly Report → **Run workflow**(右上)→ Run
- 約 60 秒完成,然後在 repo 看到一個 `Auto: monthly report for YYYY-MM` 新 commit
- 同時在 Issues 會自動開一張 TODO 提醒你補「編輯觀點」

**權限注意**:Actions 需要 `contents: write` 才能 commit。在 `Settings → Actions → General → Workflow permissions` 選 **「Read and write permissions」**。

---

## 5. Buttondown 電子報(15 min,可選但推薦)

電子報是「不靠 Google」的流量來源。免費版每月 1,000 封信(約 100 訂閱 × 10 封)。

1. https://buttondown.com → Sign up(用 Google login 最快)
2. Settings → 取你的 username(例:`brilliancelab`)
3. Settings → Subscribe form → 試一下 embed code 確認 endpoint
4. 在 BrillianceLab/blog/blog-shared.js 第 ~795 行附近找:
   ```js
   BL.NEWSLETTER = '';   // ← 改成你的 buttondown username
   ```
   改成:
   ```js
   BL.NEWSLETTER = 'brilliancelab';
   ```
5. `deploy.bat` 推上去
6. 開任何文章頁,文末會看到「鑽石市場月報」訂閱卡片

每月寫信:Buttondown 後台 → New email → markdown 格式直接貼。

---

## 6. Microsoft Clarity 已經設好了

不用動。資料看 https://clarity.microsoft.com/projects/view/wk7c4j2r47

3 天有 2 個 session 的話 = 你自己進來 2 次,正常。等 GSC indexing 起來後 traffic 會慢慢上來。

---

## 7. AdSense slot ID(可選,優化收益用)

目前所有 ad slot 都是 `auto`,Google 自己決定哪邊放廣告。要用「分版位收益分析」才需要設真 slot ID:

1. https://adsense.google.com → 廣告 → 廣告單元
2. 為文章頂部 + 文章底部各建一個 **「展示廣告」**單元
3. 取 `data-ad-slot` 數字(例:`1234567890`、`0987654321`)
4. 編輯 `BrillianceLab/build/adsense-slots.json`:
   ```json
   {
     "_default_top":    "1234567890",
     "_default_bottom": "0987654321",
     ...
   }
   ```
5. ```bash
   python build/scripts/apply_adsense_slots.py
   ```
6. `deploy.bat`

---

## 8. 月報全自動工作流(已啟用後不用做事)

**自動發生:**
- 每月 1 號 02:00 UTC,GitHub Action 跑 `build_monthly_report.py`
- 抓 Google News RSS 4 silos × 6 篇新聞
- 生成 `/blog/diamond-news-2026-XX.html`(含 Article schema、OG image、breadcrumb)
- 自動 commit、push → Vercel auto-deploy
- 自動 ping IndexNow → Bing 24h 內收錄
- 自動開 GitHub Issue 提醒你補「編輯觀點」

**你要做的:**
- 收到 GitHub Issue 通知(email),花 15 分鐘把 4 個 TODO 寫成 2-3 句編輯觀點
- 用 GitHub Web UI 直接 edit → commit
- 推上去後 IndexNow on push 又會自動 ping 一次

---

## 9. A/B test 開測(可選,要先有流量才有意義)

每天 100+ session 後再開測。範例 — 在某文章測 CTA 文字:

```html
<script defer>
document.addEventListener('DOMContentLoaded', () => BL.initBlog({
  slug: 'gia-guide',
  abTests: {
    cta_text: {
      selector: 'a[data-bl-cta="zh"]',
      variants: {
        A: '用 BrillianceLab 計算器先算分',     // control
        B: '30 秒算出你的鑽石分數',
        C: '免費評估,不用註冊',
      },
    },
  },
}));
</script>
```

GA4 → 探索 → 自由形式 → 維度加 `experiment_id` + `variant_id` → 看哪個 CTA 點擊率最高(`experiment_conversion` event)。跑 1-2 週,選贏家,把 A/B test 拿掉,直接寫死贏家文字。

---

## 10. 月維護 checklist

每月做一次(15 min):

```bash
# 1. 同步 dateModified(讓 Google 看到內容是「活」的)
python build/scripts/sync_datemodified.py

# 2. SEO 健檢
python build/scripts/audit_seo.py
# → 看 audit_seo.csv,有 issues 就跑下面這幾個 auto-fix:
python build/scripts/tighten_titles.py        # title 太長
python build/scripts/tighten_meta_desc.py     # description 太長/太短
python build/scripts/punct_fullwidth.py blog  # 半形標點

# 3. 補漏的全形標點
python build/scripts/inject_seo_essentials.py
python build/scripts/inject_faqpage_multi.py

# 4. 通知 Bing 一次
python build/scripts/ping_indexnow.py --all

# 5. deploy
./deploy.bat
```

---

## 故障排除

| 症狀 | 原因 | 解 |
|---|---|---|
| GSC 「驗證失敗」 | DNS 還沒生效 / 你還沒 deploy | 等 5 min,確認 https://brilliancelab.vercel.app/ 能看到 `<meta name="google-site-verification" content="...">` |
| `/blog/` ERR_FAILED | Service worker 快取了舊的 308 redirect | 清瀏覽器 DevTools → Application → Storage → Clear site data |
| GitHub Action 紅燈 | Workflow permissions 不對 | Settings → Actions → General → Workflow permissions 改成 Read and write |
| 月報 OG image 是空白 | CI 找不到 CJK font | 已經處理 — workflow 用 fc-match 找 Noto Sans CJK TC |
| IndexNow 回 403 | key 檔不在 root | 確認 `https://brilliancelab.vercel.app/0fe6807e04fbf0a30fffa590eb9c1b11.txt` 能載入 |
| Buttondown 表單沒反應 | 還沒設 username | `BL.NEWSLETTER` 還是空字串,檢查 blog-shared.js |
