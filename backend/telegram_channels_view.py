# -*- coding: utf-8 -*-
"""
HTML View Renderer for Telegram Channels & Groups Auto-Broadcaster (/telegram_channels_hub).
"""

from telegram_bot import load_channels, load_config, load_subscribers
from datetime import datetime

def render_telegram_channels_html():
    channels = load_channels()
    config = load_config()
    subscribers = load_subscribers()
    bot_token = config.get("bot_token", "")
    masked_token = bot_token[:8] + "..." + bot_token[-5:] if len(bot_token) > 15 else "Not Configured"
    total_subscribers = len(subscribers)

    channel_rows = ""
    if channels:
        for ch in channels:
            cid = ch.get("channel_id", "")
            title = ch.get("title", cid)
            channel_rows += f"""
            <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
              <div>
                <div class="flex items-center gap-2">
                  <span class="w-8 h-8 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-sm">📢</span>
                  <div>
                    <h4 class="text-sm font-black text-slate-900">{title}</h4>
                    <p class="text-xs font-mono text-slate-500 font-semibold">{cid}</p>
                  </div>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <button onclick="testChannel('{cid}')" class="px-3 py-1.5 bg-blue-50 hover:bg-blue-100 text-blue-700 font-bold text-xs rounded-xl transition border border-blue-200 flex items-center gap-1 cursor-pointer">
                  <span>🔔 టెస్ట్ మెసేజ్</span>
                </button>
                <button onclick="removeChannel('{cid}')" class="px-3 py-1.5 bg-rose-50 hover:bg-rose-100 text-rose-600 font-bold text-xs rounded-xl transition border border-rose-200 flex items-center gap-1 cursor-pointer">
                  <span>🗑️ తీసివేయి</span>
                </button>
              </div>
            </div>
            """
    else:
        channel_rows = """
        <div class="bg-white p-8 rounded-2xl border border-dashed border-slate-300 text-center text-slate-500">
          <div class="text-3xl mb-2">📢</div>
          <h4 class="text-sm font-bold text-slate-800">ఇంకా ఎలాంటి ఛానల్స్ లింక్ కాలేదు</h4>
          <p class="text-xs text-slate-500 mt-1">క్రింది ఫారమ్ ద్వారా మీ టెలిగ్రామ్ ఛానల్ లేదా గ్రూప్‌ను లింక్ చేయండి.</p>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>📢 టెలిగ్రామ్ ఛానల్స్ & గ్రూప్స్ ఆటో-బ్రోడ్‌కాస్టర్ | లక్ష్య కరెంట్ అఫైర్స్</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=Mandali&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Plus Jakarta Sans', 'Mandali', sans-serif; background-color: #f8fafc; color: #0f172a; }}
  </style>
</head>
<body class="min-h-screen pb-16">

  <!-- Top Header -->
  <header class="bg-slate-900 text-white sticky top-0 z-30 shadow-md border-b border-slate-800">
    <div class="max-w-5xl mx-auto px-4 py-3 flex justify-between items-center">
      <div class="flex items-center space-x-3">
        <a href="/" class="w-9 h-9 rounded-xl bg-slate-800 hover:bg-slate-700 flex items-center justify-center text-white font-black transition border border-slate-700" title="హోమ్‌కు వెళ్లు">
          ←
        </a>
        <div>
          <h1 class="text-base sm:text-lg font-black flex items-center gap-2">
            <span>📢</span> <span>టెలిగ్రామ్ స్టడీ గ్రూప్స్ & ఛానల్స్ ఆటో-బ్రోడ్‌కాస్టర్</span>
          </h1>
          <p class="text-[11px] text-slate-400">డైలీ 7:00 AM ఈ-పేపర్ PDF & క్విజ్ పోల్స్ మల్టీ-ఛానల్ డిస్పాచ్</p>
        </div>
      </div>
      <a href="/" class="text-xs font-bold text-blue-400 bg-blue-950/60 hover:bg-blue-900/60 px-3 py-1.5 rounded-lg border border-blue-800 transition">
        🌐 హోమ్‌పేజీ
      </a>
    </div>
  </header>

  <main class="max-w-5xl mx-auto px-4 mt-6 space-y-6">

    <!-- Status & Stats Card -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
        <p class="text-xs font-bold text-slate-500">కనెక్ట్ అయిన ఛానల్స్ & గ్రూప్స్</p>
        <p class="text-2xl font-black text-blue-600 mt-1">{len(channels)}</p>
        <p class="text-[11px] text-slate-400 mt-1">ఆటోమేటిక్ బ్రాడ్‌కాస్ట్ జాబితా</p>
      </div>
      <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
        <p class="text-xs font-bold text-slate-500">వ్యక్తిగత సబ్‌స్క్రైబర్లు</p>
        <p class="text-2xl font-black text-emerald-600 mt-1">{total_subscribers}</p>
        <p class="text-[11px] text-slate-400 mt-1">డైరెక్ట్ చాట్ రిసీవర్స్</p>
      </div>
      <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
        <p class="text-xs font-bold text-slate-500">బోట్ కాన్ఫిగరేషన్</p>
        <p class="text-xs font-mono font-bold text-slate-800 mt-2 bg-slate-100 p-1.5 rounded">@venkat_telugu_ca_bot</p>
        <p class="text-[11px] text-emerald-600 font-bold mt-1">● లైవ్ & యాక్టివ్</p>
      </div>
    </div>

    <!-- 1-Click Instant Broadcast Card -->
    <div class="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-950 text-white p-6 rounded-3xl shadow-lg border border-blue-800 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <div class="flex items-center gap-2 mb-1">
          <span class="bg-amber-400 text-slate-950 text-[10px] font-black uppercase px-2 py-0.5 rounded">లైవ్ బ్రాడ్‌కాస్ట్</span>
          <span class="text-xs text-blue-200 font-semibold">షెడ్యూలర్: ప్రతిరోజూ ఉదయం 7:00 గంటలకు (IST)</span>
        </div>
        <h3 class="text-lg sm:text-xl font-black">🚀 ఇప్పుడే నేటి ఈ-పేపర్ & క్విజ్ బ్రాడ్‌కాస్ట్ చేయండి</h3>
        <p class="text-xs text-slate-300 mt-1 max-w-xl">
          ఒక్క క్లిక్‌తో నేటి 12 ప్యూర్ ఎగ్జామ్ వార్తలు, 5 క్విజ్ పోల్స్, మరియు పూర్తి ఈ-పేపర్ PDF ని కనెక్ట్ అయిన అన్ని ఛానల్స్‌కు పంపండి.
        </p>
      </div>
      <button onclick="broadcastNow()" id="broadcastBtn" class="shrink-0 bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black text-xs sm:text-sm px-5 py-3 rounded-2xl shadow-md transition flex items-center gap-2 cursor-pointer">
        <span id="bcText">🚀 ఇప్పుడే బ్రాడ్‌కాస్ట్ చేయి</span>
      </button>
    </div>

    <!-- Form: Add Channel / Group -->
    <div class="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
      <h3 class="text-base font-black text-slate-900 flex items-center gap-2">
        <span>➕</span> <span>కొత్త టెలిగ్రామ్ ఛానల్ లేదా గ్రూప్‌ను లింక్ చేయండి</span>
      </h3>

      <!-- 3-Step Setup Instructions -->
      <div class="bg-blue-50/70 border border-blue-200 rounded-2xl p-4 text-xs text-blue-950 space-y-1.5">
        <p class="font-black text-blue-900">📝 ఎలా సెటప్ చేయాలి (3 సులువైన దశలు):</p>
        <p>1️⃣ మీ టెలిగ్రామ్ ఛానల్ లేదా గ్రూప్‌లోకి <b>@venkat_telugu_ca_bot</b> ని అడ్మిన్ (Admin) గా యాడ్ చేసి <i>Post Messages</i> పర్మిషన్ ఇవ్వండి.</p>
        <p>2️⃣ మీ ఛానల్ యూజర్‌నేమ్ (ఉదా: <code>@appsc_study_group</code>) లేదా గ్రూప్ చాట్ ఐడీని క్రింద నమోదు చేయండి.</p>
        <p>3️⃣ <b>"ఛానల్ లింక్ చేయి"</b> క్లిక్ చేయండి. ఆటోమేటిక్‌గా రోజువారీ బ్రాడ్‌కాస్ట్‌లు ప్రారంభమవుతాయి!</p>
      </div>

      <form id="addChannelForm" onsubmit="handleAddChannel(event)" class="grid grid-cols-1 sm:grid-cols-12 gap-3 pt-2">
        <div class="sm:col-span-5">
          <label class="block text-xs font-bold text-slate-700 mb-1">ఛానల్ యూజర్‌నేమ్ / గ్రూప్ ID *</label>
          <input type="text" id="channelIdInput" placeholder="@my_channel లేదా -100..." required class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono">
        </div>
        <div class="sm:col-span-5">
          <label class="block text-xs font-bold text-slate-700 mb-1">ఛానల్ పేరు (గుర్తింపు కోసం)</label>
          <input type="text" id="channelTitleInput" placeholder="ఉదా: APPSC గ్రూప్-2 స్టడీ క్లబ్" class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
        </div>
        <div class="sm:col-span-2 flex items-end">
          <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs sm:text-sm py-2.5 px-3 rounded-xl transition shadow-xs cursor-pointer">
            ➕ లింక్ చేయి
          </button>
        </div>
      </form>
    </div>

    <!-- Active Connected Channels List -->
    <div class="space-y-3">
      <h3 class="text-base font-black text-slate-900 flex items-center gap-2">
        <span>📋</span> <span>కనెక్ట్ అయిన ఛానల్స్ & గ్రూప్స్ జాబితా ({len(channels)})</span>
      </h3>
      <div class="space-y-3" id="channelsListContainer">
        {channel_rows}
      </div>
    </div>

  </main>

  <script>
    async function handleAddChannel(e) {{
      e.preventDefault();
      const cid = document.getElementById('channelIdInput').value.trim();
      const title = document.getElementById('channelTitleInput').value.trim();
      if (!cid) return;

      try {{
        const res = await fetch('/api/telegram/channels/add', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ channel_id: cid, title: title }})
        }});
        const data = await res.json();
        if (data.success) {{
          alert('✅ ఛానల్ విజయవంతంగా లింక్ చేయబడింది!');
          window.location.reload();
        }} else {{
          alert('❌ లోపం: ' + data.error);
        }}
      }} catch (err) {{
        alert('❌ నెట్‌వర్క్ ఎర్రర్: ' + err.message);
      }}
    }}

    async function removeChannel(cid) {{
      if (!confirm('ఈ ఛానల్‌ను ఆటో-బ్రోడ్‌కాస్ట్ జాబితా నుండి తొలగించాలా?')) return;
      try {{
        const res = await fetch('/api/telegram/channels/remove', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ channel_id: cid }})
        }});
        const data = await res.json();
        if (data.success) {{
          alert('✅ ఛానల్ తొలగించబడింది.');
          window.location.reload();
        }}
      }} catch (err) {{
        alert('❌ ఎర్రర్: ' + err.message);
      }}
    }}

    async function testChannel(cid) {{
      try {{
        alert('🔔 టెస్ట్ మెసేజ్ పంపుతున్నాం...');
        const res = await fetch('/api/telegram/channels/test', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ channel_id: cid }})
        }});
        const data = await res.json();
        if (data.success) {{
          alert('🎉 టెస్ట్ మెసేజ్ విజయవంతంగా పంపబడింది! దయచేసి మీ టెలిగ్రామ్ ఛానల్‌లో సరిచూసుకోండి.');
        }} else {{
          alert('⚠️ పంపడంలో విఫలమైంది: ' + data.error + '\n(బోట్ ఆ ఛానల్‌లో అడ్మిన్‌గా చేర్చబడిందో లేదో సరిచూసుకోండి)');
        }}
      }} catch (err) {{
        alert('❌ ఎర్రర్: ' + err.message);
      }}
    }}

    async function broadcastNow() {{
      if (!confirm('నేటి డైలీ కరెంట్ అఫైర్స్, క్విజ్ పోల్స్ మరియు ఈ-పేపర్ PDF ని కనెక్ట్ అయిన అన్ని ఛానల్స్‌కు బ్రాడ్‌కాస్ట్ చేయాలా?')) return;
      const btn = document.getElementById('broadcastBtn');
      const text = document.getElementById('bcText');
      btn.disabled = true;
      text.innerText = '⏳ బ్రాడ్‌కాస్ట్ అవుతోంది...';

      try {{
        const res = await fetch('/api/telegram/channels/broadcast_now', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }}
        }});
        const data = await res.json();
        if (data.success) {{
          alert('🎉 బ్రాడ్‌కాస్ట్ విజయవంతమైంది!\n' + data.message);
        }} else {{
          alert('❌ బ్రాడ్‌కాస్ట్ లోపం: ' + data.error);
        }}
      }} catch (err) {{
        alert('❌ ఎర్రర్: ' + err.message);
      }} finally {{
        btn.disabled = false;
        text.innerText = '🚀 ఇప్పుడే బ్రాడ్‌కాస్ట్ చేయి';
      }}
    }}
  </script>
</body>
</html>
"""
    return html
