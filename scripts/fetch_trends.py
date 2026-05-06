"""
SeasonalRank — Weekly Trend Fetcher
====================================
Sources:
  1. Google Trends   (Pytrends, free, no key)     weight: 40%
  2. TikTok Creative Center (scrape, free)         weight: 30%
  3. YouTube Data API v3 (free, 10k units/day)     weight: 20%
  4. Pinterest Trends (scrape, free)               weight: 10%

Also:
  - Fetches one Unsplash photo per style (free API)
  - Saves weekly JSON to rankings/YYYY-MM-DD.json
  - Updates data.json (current week, read by homepage)

Run: python fetch_trends.py
Requires env vars: GEMINI_API_KEY, YOUTUBE_API_KEY, UNSPLASH_ACCESS_KEY
"""

import json, os, time, random, re, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timezone

# ── STYLE LIST ────────────────────────────────────────────────────────────────
STYLES = [
    {"name": "Barrel leg jeans",     "cat": "Bottoms",   "keyword": "barrel leg jeans",         "tiktok_tag": "barreljeans",       "youtube_q": "barrel leg jeans outfit"},
    {"name": "Linen wide trousers",  "cat": "Bottoms",   "keyword": "linen wide leg pants",      "tiktok_tag": "linentrousers",     "youtube_q": "linen trousers outfit spring"},
    {"name": "Sheer overlay dress",  "cat": "Dresses",   "keyword": "sheer overlay dress",       "tiktok_tag": "sheerdress",        "youtube_q": "sheer dress outfit ideas"},
    {"name": "Coquette aesthetic",   "cat": "Aesthetic", "keyword": "coquette aesthetic outfit",  "tiktok_tag": "coquetteaesthetic", "youtube_q": "coquette aesthetic outfit"},
    {"name": "Ballet flat",          "cat": "Footwear",  "keyword": "ballet flat shoes",         "tiktok_tag": "balletflats",       "youtube_q": "ballet flats outfit 2026"},
    {"name": "Broderie top",         "cat": "Tops",      "keyword": "broderie anglaise top",     "tiktok_tag": "broderietop",       "youtube_q": "broderie top outfit"},
    {"name": "Maxi slip dress",      "cat": "Dresses",   "keyword": "maxi slip dress",           "tiktok_tag": "slipdress",         "youtube_q": "maxi slip dress styling"},
    {"name": "Cargo wide leg",       "cat": "Bottoms",   "keyword": "cargo wide leg pants",      "tiktok_tag": "cargopants",        "youtube_q": "cargo wide leg pants outfit"},
    {"name": "Varsity jacket",       "cat": "Outerwear", "keyword": "varsity jacket women",      "tiktok_tag": "varsityjacket",     "youtube_q": "varsity jacket outfit women"},
    {"name": "Butter yellow set",    "cat": "Aesthetic", "keyword": "butter yellow matching set", "tiktok_tag": "butteryellow",      "youtube_q": "butter yellow set outfit"},
    {"name": "Platform mule",        "cat": "Footwear",  "keyword": "platform mule shoes",       "tiktok_tag": "platformmules",     "youtube_q": "platform mules outfit"},
    {"name": "Lace trim cami",       "cat": "Tops",      "keyword": "lace trim camisole",        "tiktok_tag": "lacecami",          "youtube_q": "lace cami outfit ideas"},
    {"name": "Denim midi skirt",     "cat": "Bottoms",   "keyword": "denim midi skirt",          "tiktok_tag": "denimmidiskirt",    "youtube_q": "denim midi skirt outfit"},
    {"name": "Bubble hem skirt",     "cat": "Dresses",   "keyword": "bubble hem skirt",          "tiktok_tag": "bubbleskirt",       "youtube_q": "bubble skirt outfit 2026"},
    {"name": "Trench coat",          "cat": "Outerwear", "keyword": "trench coat women spring",  "tiktok_tag": "trenchcoat",        "youtube_q": "trench coat outfit spring"},
    {"name": "Ruched sundress",      "cat": "Dresses",   "keyword": "ruched sundress",           "tiktok_tag": "rucheddress",       "youtube_q": "ruched dress outfit"},
    {"name": "Mary jane heel",       "cat": "Footwear",  "keyword": "mary jane heels",           "tiktok_tag": "maryjaneshoes",     "youtube_q": "mary jane heels outfit"},
    {"name": "Oversized blazer",     "cat": "Outerwear", "keyword": "oversized blazer women",    "tiktok_tag": "oversizedblazer",   "youtube_q": "oversized blazer outfit women"},
    {"name": "Tie-front top",        "cat": "Tops",      "keyword": "tie front top women",       "tiktok_tag": "tiefronttop",       "youtube_q": "tie front top outfit"},
    {"name": "Ribbed tank set",      "cat": "Tops",      "keyword": "ribbed tank matching set",  "tiktok_tag": "ribbedset",         "youtube_q": "ribbed tank set outfit"},
]

WEIGHTS = {"google": 0.40, "tiktok": 0.30, "youtube": 0.20, "pinterest": 0.10}

# ── HELPERS ───────────────────────────────────────────────────────────────────
def http_get_text(url, headers=None, timeout=20):
    """HTTP GET returning text."""
    try:
        req = urllib.request.Request(url, headers=headers or {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"    HTTP error {url[:60]}: {e}")
        return None

def http_get_bytes(url, headers=None, timeout=30):
    """HTTP GET returning raw bytes — for image downloads."""
    try:
        req = urllib.request.Request(url, headers=headers or {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except Exception as e:
        print(f"    HTTP bytes error {url[:60]}: {e}")
        return None

def normalize(values):
    """Normalize a dict of values to 0-100 scale."""
    if not values:
        return {}
    mn, mx = min(values.values()), max(values.values())
    rng = mx - mn or 1
    return {k: round((v - mn) / rng * 100) for k, v in values.items()}

def load_prev_data():
    """Load previous week's data.json for rank comparison."""
    # Script runs from scripts/ folder — data.json is one level up
    try:
        with open("../data.json", "r") as f:
            return json.load(f)
    except Exception:
        return {}

def get_prev_rank(name, prev_data):
    for s in prev_data.get("styles", []):
        if s["name"] == name:
            return s.get("rank")
    return None

def get_prev_weeks(name, prev_data):
    for s in prev_data.get("styles", []):
        if s["name"] == name:
            return s.get("weeks", [])
    return []

def get_season(month):
    return {12:"Winter",1:"Winter",2:"Winter",
            3:"Spring",4:"Spring",5:"Spring",
            6:"Summer",7:"Summer",8:"Summer",
            9:"Fall",10:"Fall",11:"Fall"}[month]

# ── 1. GOOGLE TRENDS ──────────────────────────────────────────────────────────
def fetch_google_trends():
    print("\n[1/5] Google Trends (Pytrends)...")
    try:
        from pytrends.request import TrendReq
    except ImportError:
        print("  pytrends not installed — pip install pytrends")
        return {}

    pytrends = TrendReq(hl="en-US", tz=360, timeout=(10, 25))
    results = {}

    for i in range(0, len(STYLES), 5):
        batch = STYLES[i:i+5]
        keywords = [s["keyword"] for s in batch]
        try:
            pytrends.build_payload(keywords, cat=185, timeframe="now 4-W", geo="US")
            df = pytrends.interest_over_time()
            if not df.empty:
                for style, kw in zip(batch, keywords):
                    if kw in df.columns:
                        weeks = [int(v) for v in df[kw].tolist()]
                        last4 = weeks[-4:] if len(weeks) >= 4 else weeks
                        while len(last4) < 4:
                            last4.insert(0, last4[0] if last4 else 30)
                        results[style["name"]] = {
                            "score": last4[-1],
                            "weeks": last4
                        }
                        print(f"  ✓ {style['name']}: {last4[-1]}")
            time.sleep(random.uniform(4, 7))
        except Exception as e:
            print(f"  ✗ Batch error: {e}")
            time.sleep(12)

    return results

# ── 2. TIKTOK CREATIVE CENTER ─────────────────────────────────────────────────
def fetch_tiktok():
    print("\n[2/5] TikTok Creative Center...")
    results = {}

    for style in STYLES:
        tag = style["tiktok_tag"]
        try:
            url = f"https://ads.tiktok.com/business/creativecenter/api/v1/keywords/search?keyword={urllib.parse.quote(style['keyword'])}&period=7&country_code=US"
            html = http_get_text(url, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "Referer": "https://ads.tiktok.com/business/creativecenter/trend-keywords/pc/en",
                "Accept": "application/json"
            })

            score = 30
            if html:
                try:
                    data = json.loads(html)
                    items = data.get("data", {}).get("list", [])
                    if items:
                        score = min(100, int(items[0].get("popularity", 30)))
                except Exception:
                    pass

            tag_url = f"https://www.tiktok.com/tag/{tag}"
            tag_html = http_get_text(tag_url)
            if tag_html:
                match = re.search(r'"videoCount"[:\s]+(\d+)', tag_html)
                if match:
                    video_count = int(match.group(1))
                    score = min(100, int(video_count / 100000))

            results[style["name"]] = score
            print(f"  ✓ {style['name']}: {score}")
            time.sleep(random.uniform(1.5, 3))

        except Exception as e:
            print(f"  ✗ {style['name']}: {e}")
            results[style["name"]] = 30

    return normalize(results)

# ── 3. YOUTUBE DATA API ───────────────────────────────────────────────────────
def fetch_youtube():
    print("\n[3/5] YouTube Data API...")
    api_key = os.environ.get("YOUTUBE_API_KEY", "")
    if not api_key:
        print("  No YOUTUBE_API_KEY — skipping")
        return {}

    results = {}
    for style in STYLES:
        try:
            query = urllib.parse.quote(style["youtube_q"])
            url = (
                f"https://www.googleapis.com/youtube/v3/search"
                f"?part=snippet&q={query}&type=video&order=viewCount"
                f"&publishedAfter={(datetime.now(timezone.utc).strftime('%Y-%m-%dT00:00:00Z'))[:10]}T00:00:00Z"
                f"&maxResults=10&regionCode=US&relevanceLanguage=en"
                f"&key={api_key}"
            )
            resp = http_get_text(url)
            if not resp:
                results[style["name"]] = 30
                continue

            data = json.loads(resp)
            items = data.get("items", [])
            video_count = len(items)

            if items:
                video_ids = ",".join(i["id"]["videoId"] for i in items if "videoId" in i.get("id", {}))
                if video_ids:
                    stats_url = (
                        f"https://www.googleapis.com/youtube/v3/videos"
                        f"?part=statistics&id={video_ids}&key={api_key}"
                    )
                    stats_resp = http_get_text(stats_url)
                    if stats_resp:
                        stats_data = json.loads(stats_resp)
                        total_views = sum(
                            int(v.get("statistics", {}).get("viewCount", 0))
                            for v in stats_data.get("items", [])
                        )
                        view_score = min(50, int(total_views / 50000))
                        count_score = min(50, video_count * 5)
                        results[style["name"]] = view_score + count_score
                    else:
                        results[style["name"]] = video_count * 5
                else:
                    results[style["name"]] = 20
            else:
                results[style["name"]] = 10

            print(f"  ✓ {style['name']}: {results[style['name']]} ({video_count} videos)")
            time.sleep(0.5)

        except Exception as e:
            print(f"  ✗ {style['name']}: {e}")
            results[style["name"]] = 20

    return normalize(results)

# ── 4. PINTEREST TRENDS ───────────────────────────────────────────────────────
def fetch_pinterest():
    print("\n[4/5] Pinterest Trends...")
    results = {}

    for style in STYLES:
        try:
            query = urllib.parse.quote(style["keyword"])
            url = f"https://trends.pinterest.com/trending?term={query}&country=US"
            html = http_get_text(url, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "Accept": "application/json, text/javascript",
                "X-Requested-With": "XMLHttpRequest"
            })

            score = 30
            if html:
                try:
                    data = json.loads(html)
                    trend_data = data.get("trend", {})
                    if trend_data:
                        weekly = trend_data.get("weekly_volume", [])
                        if weekly:
                            score = min(100, int(weekly[-1] / 1000))
                except Exception:
                    match = re.search(r'"volume"[:\s]+(\d+)', html or "")
                    if match:
                        score = min(100, int(int(match.group(1)) / 1000))

            results[style["name"]] = score
            print(f"  ✓ {style['name']}: {score}")
            time.sleep(random.uniform(1, 2))

        except Exception as e:
            print(f"  ✗ {style['name']}: {e}")
            results[style["name"]] = 30

    return normalize(results)

# ── 5. UNSPLASH PHOTOS ────────────────────────────────────────────────────────
def fetch_photos():
    """
    Fetch one editorial fashion photo per style from Unsplash.
    KEY FIXES:
    - Uses http_get_bytes() for image download (raw bytes, not text)
    - Saves to images/ relative to REPO ROOT (not scripts/)
    - Returns path as "images/filename.jpg" (no ../ prefix)
    - Photo already exists → still returns correct path
    """
    print("\n[5/5] Unsplash photos...")
    access_key = os.environ.get("UNSPLASH_ACCESS_KEY", "")
    if not access_key:
        print("  No UNSPLASH_ACCESS_KEY — skipping photos")
        return {}

    photos = {}

    # Script runs from scripts/ — images/ folder is one level up
    images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")
    os.makedirs(images_dir, exist_ok=True)
    print(f"  Saving photos to: {os.path.abspath(images_dir)}")

    for style in STYLES:
        filename = style["name"].lower().replace(" ", "-").replace("'", "").replace("/", "-") + ".jpg"
        filepath = os.path.join(images_dir, filename)
        photo_path = f"images/{filename}"  # ← clean path, no ../

        # Already exists — just record path, skip download
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
            photos[style["name"]] = photo_path
            print(f"  ✓ {style['name']}: already exists → {photo_path}")
            continue

        try:
            # 1. Ask Unsplash for photo URL
            query = urllib.parse.quote(style["keyword"] + " fashion editorial")
            api_url = (
                f"https://api.unsplash.com/search/photos"
                f"?query={query}&per_page=1&orientation=portrait"
                f"&content_filter=high&order_by=relevant"
            )
            resp = http_get_text(api_url, headers={
                "Authorization": f"Client-ID {access_key}",
                "Accept-Version": "v1"
            })

            if not resp:
                print(f"  ✗ {style['name']}: Unsplash API no response")
                photos[style["name"]] = ""
                continue

            data = json.loads(resp)
            results_list = data.get("results", [])

            if not results_list:
                print(f"  - {style['name']}: no Unsplash results")
                photos[style["name"]] = ""
                continue

            # 2. Get the image URL and download as raw bytes
            img_url = results_list[0]["urls"]["small"]  # smaller = faster download
            photo_credit = results_list[0]["user"]["name"]

            img_bytes = http_get_bytes(img_url)
            if img_bytes and len(img_bytes) > 1000:
                # 3. Save raw bytes directly to file
                with open(filepath, "wb") as f:
                    f.write(img_bytes)
                photos[style["name"]] = photo_path
                print(f"  ✓ {style['name']}: saved {len(img_bytes)//1024}KB → {photo_path} (by {photo_credit})")
            else:
                print(f"  ✗ {style['name']}: image download failed or too small")
                photos[style["name"]] = ""

            time.sleep(1.5)  # Stay within Unsplash rate limits

        except Exception as e:
            print(f"  ✗ {style['name']}: {e}")
            photos[style["name"]] = ""

    # Summary
    found = sum(1 for v in photos.values() if v)
    print(f"  → {found}/{len(STYLES)} photos ready")
    return photos

# ── GEMINI AI INSIGHTS ────────────────────────────────────────────────────────
def fetch_gemini_insights(scored_styles):
    print("\n[6/6] Gemini Flash insights...")
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("  No GEMINI_API_KEY — skipping insights")
        return {}

    top10 = scored_styles[:10]
    style_list = "\n".join([
        f"{i+1}. {s['name']} (score:{s['final_score']}, momentum:{s['momentum_pct']:+.0f}%)"
        for i, s in enumerate(top10)
    ])

    prompt = f"""You are a fashion trend analyst for the US market.
Here are the top 10 trending clothing styles this week ranked by combined signal score:

{style_list}

Write ONE punchy sentence (max 10 words) for each explaining why it is trending.
Respond ONLY with a valid JSON object. No markdown, no backticks, no explanation.
Example format:
{{"Barrel leg jeans":"Relaxed silhouette dominating street style everywhere."}}"""

    try:
        payload = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": 600, "temperature": 0.4}
        }).encode("utf-8")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        req = urllib.request.Request(url, data=payload,
            headers={"Content-Type": "application/json"}, method="POST")

        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            text = text.strip().strip("```json").strip("```").strip()
            insights = json.loads(text)
            print(f"  ✓ {len(insights)} insights generated")
            return insights

    except Exception as e:
        print(f"  ✗ Gemini error: {e}")
        return {}

# ── COMBINE SCORES ────────────────────────────────────────────────────────────
def combine_scores(google, tiktok, youtube, pinterest, photos, prev_data):
    styled = []

    for style in STYLES:
        name = style["name"]
        g = google.get(name, {}).get("score", 30) if isinstance(google.get(name), dict) else google.get(name, 30)
        t = tiktok.get(name, 30)
        y = youtube.get(name, 30)
        p = pinterest.get(name, 30)

        final = round(
            g * WEIGHTS["google"] +
            t * WEIGHTS["tiktok"] +
            y * WEIGHTS["youtube"] +
            p * WEIGHTS["pinterest"]
        )

        prev_weeks = get_prev_weeks(name, prev_data)
        if isinstance(google.get(name), dict):
            current_weeks = google[name].get("weeks", [g, g, g, g])
        else:
            current_weeks = prev_weeks[-3:] + [final] if len(prev_weeks) >= 3 else [final] * 4

        styled.append({
            "name":       name,
            "cat":        style["cat"],
            "final_score": final,
            "weeks":      current_weeks[-4:],
            "signals": {
                "google":    {"score": g, "weight": WEIGHTS["google"],    "keyword": style["keyword"]},
                "tiktok":    {"score": t, "weight": WEIGHTS["tiktok"],    "hashtag": "#" + style["tiktok_tag"]},
                "youtube":   {"score": y, "weight": WEIGHTS["youtube"],   "query":   style["youtube_q"]},
                "pinterest": {"score": p, "weight": WEIGHTS["pinterest"], "keyword": style["keyword"]},
            },
            "photo":      photos.get(name, ""),
            "insight":    "",
            "prev_rank":  get_prev_rank(name, prev_data),
        })

    styled.sort(key=lambda x: x["final_score"], reverse=True)
    for i, s in enumerate(styled):
        s["rank"] = i + 1
        prev = s["prev_rank"]
        s["momentum_pct"] = round(
            (s["final_score"] - prev) / prev * 100, 1
        ) if prev else 0.0

    return styled

# ── SAVE DATA ─────────────────────────────────────────────────────────────────
def save_data(styled, insights):
    now    = datetime.now(timezone.utc)
    season = get_season(now.month)

    for s in styled:
        s["insight"] = insights.get(s["name"], "")

    output = {
        "updated_at":    now.strftime("%B %d, %Y"),
        "updated_iso":   now.isoformat(),
        "week_of":       now.strftime("%Y-%m-%d"),
        "season":        season,
        "year":          now.year,
        "geo":           "US",
        "total_tracked": len(STYLES),
        "rising_count":  sum(1 for s in styled if s["momentum_pct"] > 0),
        "new_entries":   sum(1 for s in styled if s["prev_rank"] is None),
        "avg_momentum":  round(sum(s["momentum_pct"] for s in styled) / len(styled), 1),
        "weights":       WEIGHTS,
        "styles":        styled,
    }

    # All paths relative to repo root (script runs from scripts/)
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

    # 1. data.json — homepage reads this
    with open(os.path.join(root, "data.json"), "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n  ✓ data.json saved")

    # 2. rankings/YYYY-MM-DD.json — history archive
    rankings_dir = os.path.join(root, "rankings")
    os.makedirs(rankings_dir, exist_ok=True)
    week_file = os.path.join(rankings_dir, f"{now.strftime('%Y-%m-%d')}.json")
    with open(week_file, "w") as f:
        json.dump(output, f, indent=2)
    print(f"  ✓ rankings/{now.strftime('%Y-%m-%d')}.json saved")

    # 3. rankings/index.json — list of all weeks
    index_file = os.path.join(rankings_dir, "index.json")
    try:
        with open(index_file, "r") as f:
            index = json.load(f)
    except Exception:
        index = {"weeks": []}

    week_entry = {
        "date":         now.strftime("%Y-%m-%d"),
        "label":        now.strftime("%B %d, %Y"),
        "season":       season,
        "year":         now.year,
        "top_style":    styled[0]["name"],
        "rising_count": output["rising_count"],
    }
    if not any(w["date"] == week_entry["date"] for w in index["weeks"]):
        index["weeks"].insert(0, week_entry)

    with open(index_file, "w") as f:
        json.dump(index, f, indent=2)
    print(f"  ✓ rankings/index.json updated ({len(index['weeks'])} weeks)")

    return output

# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 55)
    print("SeasonalRank — Weekly Trend Fetch")
    print(f"Running: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 55)

    prev_data = load_prev_data()

    google    = fetch_google_trends()
    tiktok    = fetch_tiktok()
    youtube   = fetch_youtube()
    pinterest = fetch_pinterest()
    photos    = fetch_photos()

    print("\n[Combining scores...]")
    styled = combine_scores(google, tiktok, youtube, pinterest, photos, prev_data)

    insights = fetch_gemini_insights(styled)

    print("\n[Saving data...]")
    output = save_data(styled, insights)

    print(f"\n{'='*55}")
    print(f"✅ Done — {len(styled)} styles ranked")
    print(f"   #1: {styled[0]['name']} (score: {styled[0]['final_score']})")
    print(f"   #2: {styled[1]['name']} (score: {styled[1]['final_score']})")
    print(f"   #3: {styled[2]['name']} (score: {styled[2]['final_score']})")
    print(f"   Updated: {output['updated_at']}")
    print(f"{'='*55}")

if __name__ == "__main__":
    main()
