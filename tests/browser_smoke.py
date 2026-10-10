"""Browser smoke test for LEAN / 30.
Run: pip install playwright && playwright install chromium && python tests/browser_smoke.py
Uses inlined resources and a localStorage shim to run without a web server.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text()
CSS = (ROOT / 'styles.css').read_text()
JS = (ROOT / 'app.js').read_text()
DOC = (HTML.replace('<link rel="stylesheet" href="styles.css">',f'<style>{CSS}</style>')
       .replace('<script src="app.js" defer></script>','')
       .replace('</head>', '''<script>
       window.__testStore={};
       Object.defineProperty(window,'localStorage',{value:{
         getItem:k=>window.__testStore[k]??null,
         setItem:(k,v)=>window.__testStore[k]=String(v),
         removeItem:k=>delete window.__testStore[k]
       }});
       </script></head>''')
       .replace('</body>',f'<script>{JS}</script></body>'))


def check(page, expr, message):
    assert page.evaluate(expr), message


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--no-proxy-server'])
        results=[]
        for width,height in [(1440,900),(768,1024),(390,844),(320,720)]:
            page=browser.new_page(viewport={'width':width,'height':height},accept_downloads=True)
            errors=[]
            page.on('pageerror',lambda err:errors.append(str(err)))
            page.set_content(DOC)
            assert not errors, f'page load error @ {width}: {errors}'
            for route in ['overview','daily','training','nutrition','progress']:
                btn = page.locator(f'.nav-btn[data-page="{route}"]')
                if width<=600:
                    page.locator(f'.bottom-nav .nav-btn[data-page="{route}"]').click()
                elif width<=890:
                    page.evaluate(f'go("{route}")')
                else:
                    btn.first.click()
                assert page.locator(f'#page-{route}').evaluate('(e)=>e.classList.contains("active")')
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), f'horizontal overflow: {route} @ {width}'
                assert not errors, f'JS error @ {width}, {route}: {errors}'
            results.append(f'{width}px: five routes, no overflow, zero exceptions')
            page.close()

        page=browser.new_page(viewport={'width':1280,'height':900},accept_downloads=True)
        errors=[]
        page.on('pageerror',lambda err:errors.append(str(err)))
        page.set_content(DOC)
        page.evaluate('go("daily")')
        page.locator('[data-field="protein"]').fill('162')
        page.locator('[data-field="calories"]').fill('2300')
        page.locator('[data-field="steps"]').fill('7650')
        page.locator('[data-field="weight"]').fill('80.5')
        page.locator('[data-field="waist"]').fill('93')
        page.locator('[data-field="workout"]').check()
        page.locator('[data-field="walk1"]').check()
        page.locator('[data-field="notes"]').fill('Good session, 2km walk.')
        page.locator('#mark-complete').click()
        check(page,"JSON.parse(__testStore['lean30-tracker-v1']).entries[0].logged===true",'day not logged')
        check(page,"JSON.parse(__testStore['lean30-tracker-v1']).entries[0].protein===162",'protein not stored')
        page.evaluate('go("overview")')
        assert page.locator('#logged-count').inner_text()=='1'
        page.locator('#prev-day').count() # ensure present
        assert page.locator('#pulse-protein').inner_text().strip()=='162 / 160 g'
        results.append('Daily data saved; overview stats and today pulse updated')

        page.evaluate('go("daily")')
        page.locator('[data-field="protein"]').fill('999')
        assert page.locator('[data-field="protein"]').get_attribute('aria-invalid')=='true'
        check(page,"JSON.parse(__testStore['lean30-tracker-v1']).entries[0].protein===162",'Invalid input persisted')
        page.locator('#mark-complete').click()
        assert page.locator('#logged-count').inner_text()=='1'
        page.locator('[data-field="protein"]').fill('155')
        assert page.locator('[data-field="protein"]').get_attribute('aria-invalid') is None
        results.append('Out-of-range input rejected, valid input accepted')

        page.evaluate('go("progress")')
        page.locator('#setting-protein').fill('180')
        page.locator('#setting-calories').fill('2450')
        page.locator('#setting-steps').fill('8500')
        page.locator('#save-settings').click()
        page.evaluate('go("daily")')
        assert page.locator('#daily-protein-target').inner_text()=='180'
        assert page.locator('#daily-calories-target').inner_text()=='2,450'
        assert page.locator('#daily-steps-target').inner_text()=='8,500'
        page.evaluate('go("nutrition")')
        assert page.locator('#nutrition-calories').inner_text()=='2,450'
        assert page.locator('#nutrition-protein').inner_text()=='180 g'
        assert page.locator('#nutrition-carbs').inner_text()=='~286 g'
        results.append('Custom targets synchronized across daily tracker, overview and nutrition')

        page.evaluate('go("progress")')
        with page.expect_download() as d:
            page.locator('#export-csv').click()
        assert d.value.suggested_filename.endswith('.csv')
        with page.expect_download() as d:
            page.locator('#backup-btn').click()
        assert d.value.suggested_filename.endswith('.json')
        results.append('CSV export and JSON backup trigger downloads')

        page.on('dialog',lambda dialog:dialog.accept())
        page.locator('#reset-btn').click()
        assert page.locator('#stat-days').inner_text().startswith('0')
        assert page.locator('#setting-protein').input_value()=='160'
        results.append('Reset clears data and resets targets')

        page.locator('#restore-file').set_input_files({'name':'restore.json','mimeType':'application/json','buffer':bytes('{"version":1,"startDate":"2026-10-11","targets":{"protein":160,"calories":2300,"steps":7000},"entries":{"0":{"protein":159,"logged":true},"1":{"weight":80.1,"logged":true},"2":{"weight":79.6,"logged":true}}}','utf-8')})
        assert page.locator('#stat-days').inner_text().startswith('3')
        assert page.locator('#weight-chart svg').count()==1
        check(page,"JSON.parse(__testStore['lean30-tracker-v1']).entries[1].weight===80.1",'Restore missing weight')
        results.append('JSON restore, chart rendering, and persisted values work')
        assert not errors, f'Page errors: {errors}'
        browser.close()
        print('PASS —  '+ '\nPASS —  '.join(results))

if __name__=='__main__':
    run()
