"""Descarga el precio PVPC por horas de Red Eléctrica (apidatos.ree.es) para hoy y mañana y lo guarda en pvpc.json."""
import json, urllib.request, datetime, zoneinfo, os
tz = zoneinfo.ZoneInfo('Europe/Madrid'); hoy = datetime.datetime.now(tz).date(); man = hoy + datetime.timedelta(days=1)
url = f"https://apidatos.ree.es/es/datos/mercados/precios-mercados-tiempo-real?start_date={hoy}T00:00&end_date={man}T23:59&time_trunc=hour"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (GastoLuz)', 'Accept': 'application/json'})
d = json.load(urllib.request.urlopen(req, timeout=60))
pv = next(i for i in d['included'] if i['type'] == 'PVPC')
dias = {}
for v in pv['attributes']['values']:
    t = datetime.datetime.fromisoformat(v['datetime']).astimezone(tz)
    dias.setdefault(str(t.date()), []).append([t.hour, round(v['value'] / 1000, 5)])
old = {}
if os.path.exists('pvpc.json'):
    try: old = json.load(open('pvpc.json'))
    except Exception: pass
out = {"fuente": "Red Eléctrica (REE), PVPC", "actualizado": pv['attributes'].get('last-update'), "dias": {k: dias[k] for k in sorted(dias) if len(dias[k]) >= 23}}
if out['dias'] and out != old:
    json.dump(out, open('pvpc.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    print('actualizado', list(out['dias']))
else:
    print('sin cambios')
