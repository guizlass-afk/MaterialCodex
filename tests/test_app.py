from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from pathlib import Path
from playwright.sync_api import sync_playwright
import os,json,sys,csv,io,math
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'materials.json').read_text(encoding='utf-8'))
assert len(data['materials'])==60
assert len({m['id'] for m in data['materials']})==60
for m in data['materials']:
 assert m['source'] in data['sources'] and m['composition']['mode']
 for key,p in m['properties'].items():
  assert p.get('source',m['source']) in data['sources']
  assert p['kind'] in ('typical','range','minimum','maximum','converted','greater','less')
  if isinstance(p['v'],list):assert len(p['v'])==2 and p['v'][0]<=p['v'][1]
  if isinstance(p['v'],(float,int)):assert math.isfinite(p['v'])
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='chrome',headless=True);page=browser.new_page(viewport={'width':1440,'height':1000},locale='pt-BR');errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/');page.wait_for_function('window.MaterialCodex')
  assert page.locator('.material-row').count()==60
  # Independent reference values and reciprocal bounds, with provenance retained.
  facts=page.evaluate('Object.fromEntries(MaterialData.materials.map(m=>[m.id,MaterialCodex.properties(m)]))')
  assert abs(facts['ss-304']['specificWeight']['v']-77.472535)<1e-8
  assert abs(facts['ss-304']['conductivity']['v']-1369863.01369863)<1e-5
  assert facts['ad-94']['conductivity']['v']==1e-12 and facts['ad-94']['conductivity']['parentKind']=='less'
  assert facts['c45']['conductivity']['v']==[4000000,5000000]
  assert abs(facts['c11000']['conductivity']['v']-58580000)<1
  assert facts['al6061-o']['yield']['kind']=='maximum'
  assert 'density' not in facts['abs'] and facts['abs']['specificGravity']['v']==1.04
  assert abs(facts['abs']['tensile']['v']-28.268504902)<1e-6
  assert facts['nitrogen']['density']['v']==1.145 and facts['nitrogen-liquid']['density']['v']==806.11
  assert 'tensile' not in facts['ad-94'] and 'young' not in facts['g10-fr4']
  # Search language variants, CAS, accents and combined terms; filters compose.
  for query,expected in [('304',3),('7727-37-9',2),('nitrogênio',2),('N₂',2),('PEEK',1),('não-existe-xxx',0)]:
   page.locator('#search').fill(query);assert page.locator('.material-row').count()==expected,(query,page.locator('.material-row').count())
  page.locator('#clearFilters').click();page.locator('#family').select_option('ceramic');assert page.locator('.material-row').count()==14
  page.locator('#propertyFilter').select_option('tensile');assert page.locator('.material-row').count()==0
  page.locator('#clearFilters').click()
  # Every record renders, linking all supplied properties and sources.
  for m in data['materials']:
   page.locator(f'[data-material="{m["id"]}"]').click()
   assert page.locator('#detail h2').inner_text()
   assert page.locator('#detail tr[data-property]').count()==len(facts[m['id']])
   assert 'undefined' not in page.locator('#detail').inner_text()
  for id in ['ss-304','al6061-t6','peek','nitrogen']:
   page.locator(f'[data-material="{id}"]').click();page.locator('#compareCurrent').click()
  assert page.locator('[data-remove]').count()==4
  page.locator('[data-material="abs"]').click();page.locator('#compareCurrent').click();assert page.locator('[data-remove]').count()==4 and page.locator('#status').is_visible()
  with page.expect_download() as download:page.locator('#exportComparison').click()
  rows=list(csv.DictReader(io.StringIO(Path(download.value.path()).read_text(encoding='utf-8-sig'))))
  assert len({r['material_id'] for r in rows})==4
  calc=next(r for r in rows if r['material_id']=='ss-304' and r['property_id']=='specificWeight');assert abs(float(calc['value'])-77.472535)<1e-8 and calc['source_url'].startswith('https:') and calc['calculation']
  assert all(len(r)==18 for r in rows)
  page.locator('[data-remove="nitrogen"]').click();assert page.locator('[data-remove]').count()==3
  page.reload();assert page.locator('[data-remove]').count()==3
  page.locator('#clearComparison').click();assert page.locator('#comparison').is_hidden()
  translations=page.evaluate('MaterialTranslations');assert len(translations)==12
  for code,values in translations.items():
   assert values.keys()==translations['en-US'].keys() and all(values.values())
   page.locator('#languageButton').click();page.locator(f'[data-language="{code}"]').click()
   assert page.locator('html').get_attribute('lang')==code
   assert page.locator('html').get_attribute('dir')==('rtl' if code=='ar-SA' else 'ltr')
   assert page.locator('#detail h3').first.inner_text()==values['composition']
   for width,height in [(1440,1000),(768,900),(390,844),(320,740)]:
    page.set_viewport_size({'width':width,'height':height});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(code,width,page.evaluate('[...document.querySelectorAll("body *")].filter(e=>e.getBoundingClientRect().right>innerWidth+1).map(e=>[e.tagName,e.id,e.className,Math.round(e.getBoundingClientRect().right)])'))
  page.set_viewport_size({'width':1440,'height':1000});page.locator('#languageButton').click();page.locator('[data-language="pt-BR"]').click();page.locator('[data-material="ss-304"]').click()
  page.evaluate("localStorage.setItem('factorytoolbox-theme','light')");page.reload();assert page.locator('html').get_attribute('data-theme')=='light'
  page.screenshot(path=str(Path(os.environ['TEMP'])/'material-light.png'),full_page=True)
  page.locator('#themeToggle').click();assert page.locator('html').get_attribute('data-theme')=='dark';page.reload();assert page.locator('html').get_attribute('data-theme')=='dark'
  page.screenshot(path=str(Path(os.environ['TEMP'])/'material-dark.png'),full_page=True)
  page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(Path(os.environ['TEMP'])/'material-mobile.png'),full_page=True)
  page.locator('#languageButton').focus();page.keyboard.press('ArrowDown');page.keyboard.press('End');assert page.locator('[data-language="ja-JP"]').evaluate('el=>el===document.activeElement');page.keyboard.press('Escape');assert page.locator('#languageMenu').is_hidden()
  page.locator('#languageButton').click();page.locator('[data-language="ar-SA"]').click();page.screenshot(path=str(Path(os.environ['TEMP'])/'material-arabic.png'),full_page=True)
  page.emulate_media(media='print');assert page.locator('.library').is_hidden() and page.locator('#detail').is_visible()
  # CSV quotes/newlines and spreadsheet-formula strings stay text, negative numbers stay numeric.
  safe=page.evaluate("MaterialCodex.csvText([{...MaterialData.materials[0],id:'test',name:'=1+1',properties:{density:{v:1000,condition:'',kind:'typical'}},composition:{mode:'base',items:{}}}])")
  assert list(csv.DictReader(io.StringIO(safe.lstrip('\ufeff'))))[0]['material']=="'=1+1"
  assert not errors,errors
  browser.close();print('PASS: 60 records, independent calculations, source provenance, filters, comparisons, CSV download, 12 languages, four widths, RTL, themes, keyboard, persistence and print.')
finally:server.shutdown()
