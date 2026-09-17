import asyncio, hashlib, hmac, json, os, sqlite3
from datetime import datetime, timedelta
from urllib.parse import parse_qsl
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (Message, InlineKeyboardMarkup, InlineKeyboardButton,
                           WebAppInfo, MenuButtonWebApp)
from aiohttp import web
BOT_TOKEN=os.getenv("BOT_TOKEN");WEBAPP_URL=os.getenv("WEBAPP_URL")
PORT=int(os.getenv("PORT",8080))
DB_PATH="/tmp/bot.db" if os.path.exists("/tmp") else "bot.db"
bot=Bot(token=BOT_TOKEN); dp=Dispatcher()
HTML=r"""<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no,viewport-fit=cover">
<title>App</title><script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent;margin:0;padding:0}
:root{--bg:#0a0a12;--c:rgba(255,255,255,.045);--b:rgba(255,255,255,.08);--t:#eaeaf2;--m:#8a8aa3;--a1:#7c5cff;--a2:#4a9eff}
body{font-family:-apple-system,system-ui,sans-serif;background:var(--bg);color:var(--t);padding-bottom:calc(84px + env(safe-area-inset-bottom));min-height:100vh}
body::before{content:"";position:fixed;inset:0;z-index:-1;background:radial-gradient(600px 400px at 10% -5%,rgba(124,92,255,.35),transparent 60%),radial-gradient(500px 400px at 100% 15%,rgba(74,158,255,.28),transparent 60%),linear-gradient(180deg,#0a0a12,#0d0d18)}
.h{padding:calc(20px + env(safe-area-inset-top)) 20px 12px}
.u{display:flex;align-items:center;gap:12px}
.av{width:48px;height:48px;border-radius:16px;display:grid;place-items:center;font-size:20px;font-weight:700;color:#fff;background:linear-gradient(135deg,var(--a1),var(--a2))}
.ni{flex:1;min-width:0}.nn{font-size:16px;font-weight:600}.ns{font-size:13px;color:var(--m)}
.bp{padding:8px 14px;border-radius:14px;font-weight:600;font-size:14px;background:linear-gradient(135deg,rgba(124,92,255,.25),rgba(74,158,255,.25));border:1px solid rgba(124,92,255,.4)}
main{padding:8px 20px 20px}
.st{font-size:22px;font-weight:700;margin:16px 0 12px}
.ss{color:var(--m);font-size:14px;margin-top:-8px;margin-bottom:16px}
.cd{background:var(--c);border:1px solid var(--b);border-radius:20px;padding:18px;margin-bottom:12px}
.hero{background:linear-gradient(135deg,rgba(124,92,255,.22),rgba(74,158,255,.18));border:1px solid rgba(124,92,255,.35);border-radius:24px;padding:22px;position:relative;overflow:hidden}
.hl{font-size:13px;color:rgba(255,255,255,.7);text-transform:uppercase;letter-spacing:1px;font-weight:600}
.hv{font-size:28px;font-weight:800;margin-top:6px}
.hm{margin-top:8px;font-size:14px;color:rgba(255,255,255,.75)}
.sts{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px}
.stt{background:var(--c);border:1px solid var(--b);border-radius:18px;padding:16px}
.si{font-size:22px;margin-bottom:8px}.sl{font-size:12px;color:var(--m);text-transform:uppercase}
.sv{font-size:22px;font-weight:700;margin-top:4px}
.pl{position:relative;background:var(--c);border:1px solid var(--b);border-radius:20px;padding:18px;margin-bottom:12px}
.pl.hit{border-color:rgba(124,92,255,.6);box-shadow:0 8px 32px rgba(124,92,255,.25)}
.pl.hit::before{content:"ТОП";position:absolute;top:12px;right:12px;font-size:10px;font-weight:700;padding:4px 8px;border-radius:8px;background:linear-gradient(135deg,var(--a1),var(--a2));color:#fff}
.pt{font-size:16px;font-weight:600}.pp{font-size:26px;font-weight:800;margin-top:6px}
.pp small{font-size:14px;color:var(--m);margin-left:6px}
.po{font-size:13px;color:var(--m);text-decoration:line-through;margin-left:8px}
.btn{width:100%;margin-top:14px;padding:14px;border:none;border-radius:14px;font-size:15px;font-weight:600;color:#fff;background:linear-gradient(135deg,var(--a1),var(--a2));font-family:inherit}
.btn.g{background:var(--c);border:1px solid var(--b)}
.tx{display:flex;align-items:center;gap:14px;padding:14px 0;border-bottom:1px solid rgba(255,255,255,.05)}
.tx:last-child{border:none}
.ti{width:42px;height:42px;border-radius:14px;display:grid;place-items:center;font-size:18px;background:linear-gradient(135deg,rgba(124,92,255,.25),rgba(74,158,255,.25))}
.tt{font-size:14px;font-weight:600}.td{font-size:12px;color:var(--m);margin-top:2px}
.ta{font-size:15px;font-weight:700;color:#ff5c7a;margin-left:auto}
.rl{display:flex;gap:10px;align-items:center;margin-top:12px;background:rgba(0,0,0,.25);border:1px solid var(--b);border-radius:14px;padding:12px 14px}
.rl span{flex:1;font-size:13px;color:var(--m);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rl button{background:linear-gradient(135deg,var(--a1),var(--a2));color:#fff;border:none;padding:8px 14px;border-radius:10px;font-size:13px;font-weight:600}
.empty{text-align:center;padding:40px 20px;color:var(--m)}
.nav{position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom));display:grid;grid-template-columns:repeat(4,1fr);background:rgba(20,20,32,.75);border:1px solid var(--b);backdrop-filter:blur(24px);border-radius:22px;padding:8px;z-index:100}
.nb{display:flex;flex-direction:column;align-items:center;gap:3px;background:none;border:none;color:var(--m);padding:8px 4px;border-radius:14px;font-size:10px;font-weight:600;font-family:inherit}
.nb .ico{font-size:20px;line-height:1}
.nb.active{color:#fff;background:linear-gradient(135deg,rgba(124,92,255,.3),rgba(74,158,255,.2))}
.toast{position:fixed;left:50%;bottom:110px;transform:translateX(-50%);background:rgba(30,30,45,.95);border:1px solid var(--b);padding:12px 18px;border-radius:14px;font-size:14px;opacity:0;transition:.3s;z-index:200}
.toast.show{opacity:1}
</style></head><body>
