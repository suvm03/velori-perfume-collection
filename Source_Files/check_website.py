"""Exercise the static website in real headless Chrome via the DevTools protocol."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import threading, subprocess, tempfile, time, urllib.request, json, base64
import websocket

root=Path(__file__).resolve().parents[1]
checks=root/'Quality_Checks';checks.mkdir(exist_ok=True)
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw): super().__init__(*a,directory=str(root),**kw)
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
profile=tempfile.mkdtemp(prefix='velori-browser-')
chrome=Path('C:/Program Files/Google/Chrome/Application/chrome.exe')
startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW
process=subprocess.Popen([str(chrome),'--headless=new','--enable-unsafe-swiftshader','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--remote-allow-origins=*',f'--user-data-dir={profile}','about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,startupinfo=startup)
ws=None;seq=0
def call(method,params=None):
    global seq
    seq+=1;expected=seq
    ws.send(json.dumps({'id':seq,'method':method,'params':params or {}}))
    while True:
        response=json.loads(ws.recv())
        if response.get('id')==expected:
            if 'error' in response:raise RuntimeError(response['error'])
            return response.get('result',{})
def js(expression):
    r=call('Runtime.evaluate',{'expression':expression,'returnByValue':True,'awaitPromise':True})
    if 'exceptionDetails' in r: raise RuntimeError(r['exceptionDetails'])
    return r['result'].get('value')
try:
    for _ in range(50):
        try:
            port=(Path(profile)/'DevToolsActivePort').read_text().splitlines()[0]
            pages=json.loads(urllib.request.urlopen(f'http://127.0.0.1:{port}/json',timeout=1).read());break
        except Exception:time.sleep(.2)
    else:raise RuntimeError('Chrome did not start')
    target=next(p for p in pages if p['type']=='page')
    ws=websocket.create_connection(target['webSocketDebuggerUrl'],origin=f'http://localhost:{port}',http_no_proxy=['localhost','127.0.0.1'],timeout=20)
    call('Page.enable');call('Runtime.enable')
    call('Emulation.setDeviceMetricsOverride',{'width':1440,'height':1000,'deviceScaleFactor':1,'mobile':False})
    url=f'http://127.0.0.1:{server.server_address[1]}/'
    call('Page.navigate',{'url':url})
    for _ in range(60):
        if js('document.querySelectorAll(".product-card").length')==24:break
        time.sleep(.2)
    assert js('document.querySelectorAll(".product-card").length')==24
    for _ in range(100):
        if js('document.getElementById("studio-canvas").dataset.ready')=='true':break
        time.sleep(.2)
    assert js('document.getElementById("studio-canvas").dataset.ready')=='true','3D studio did not initialise'
    for code in [f'V{i:02}' for i in range(1,25)]:
        js(f'document.getElementById("studio-select").value="{code}";document.getElementById("studio-select").dispatchEvent(new Event("change"))')
        assert js('document.getElementById("studio-canvas").dataset.model')==code
    js('document.getElementById("studio-select").value="V18";document.getElementById("studio-select").dispatchEvent(new Event("change"));document.getElementById("studio").scrollIntoView()')
    js('document.querySelector("#studio [data-action=\\"box\\"]").click();document.querySelector("#studio [data-action=\\"cap\\"]").click()')
    assert js('window.VELORI3D.studio.openCap && window.VELORI3D.studio.showBox')
    time.sleep(1)
    (checks/'Website_3D_Studio.png').write_bytes(base64.b64decode(call('Page.captureScreenshot',{'format':'png'})['data']))
    js('document.querySelector("[data-group=\\"0\\"]").click()')
    assert js('document.querySelectorAll(".product-card").length')==4
    js('document.getElementById("category").value="Boys";document.getElementById("category").dispatchEvent(new Event("change"))')
    assert js('document.querySelectorAll(".product-card").length')==1
    js('document.getElementById("reset").click();document.getElementById("search").value="bear";document.getElementById("search").dispatchEvent(new Event("input"))')
    assert js('document.querySelectorAll(".product-card").length')==1
    js('document.querySelector(".product-card").click()')
    assert js('document.getElementById("design-dialog").open')
    assert js('document.getElementById("dialog-title").textContent')=='Hush Bear'
    assert js('!document.getElementById("dialog-three").hidden')
    assert js('document.getElementById("dialog-canvas").dataset.ready')=='true'
    time.sleep(.5)
    (checks/'Website_3D_Detail.png').write_bytes(base64.b64decode(call('Page.captureScreenshot',{'format':'png'})['data']))
    js('document.querySelector("[data-view=\\"Back\\"]").click()')
    assert js('document.getElementById("dialog-image").getAttribute("src")').endswith('/Back.webp')
    call('Page.captureScreenshot',{'format':'png'})
    (checks/'Website_Design_Detail.png').write_bytes(base64.b64decode(call('Page.captureScreenshot',{'format':'png'})['data']))
    js('document.getElementById("close-dialog").click();document.getElementById("reset").click();window.scrollTo(0,0)')
    assert not js('document.getElementById("design-dialog").open')
    time.sleep(1)
    assert js('document.documentElement.scrollWidth <= window.innerWidth')
    (checks/'Website_Desktop.png').write_bytes(base64.b64decode(call('Page.captureScreenshot',{'format':'png'})['data']))
    call('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'deviceScaleFactor':1,'mobile':True})
    time.sleep(.5)
    assert js('document.documentElement.scrollWidth <= window.innerWidth')
    (checks/'Website_Mobile.png').write_bytes(base64.b64decode(call('Page.captureScreenshot',{'format':'png'})['data']))
    local_links=js('Array.from(document.querySelectorAll("a[href],img[src],script[src],link[href]")).map(e=>e.getAttribute("href")||e.getAttribute("src")).filter(x=>x&&!x.startsWith("#")&&!x.startsWith("http"))')
    missing=[p for p in local_links if not (root/p.split('#')[0]).is_file()]
    assert not missing,missing
    report={'verified':True,'browser':'Chrome headless','designs':24,'3d_models_built':24,'3d_cap_control':True,'3d_box_control':True,'3d_dialog':True,'collection_filter':True,'category_filter':True,'search':True,'detail_dialog':True,'gallery_view_switch':True,'close_dialog':True,'desktop_no_horizontal_overflow':True,'mobile_no_horizontal_overflow':True,'local_link_targets_exist':True}
    (checks/'Website_Verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
finally:
    if ws:ws.close()
    process.terminate()
    try:process.wait(timeout=8)
    except subprocess.TimeoutExpired:process.kill()
    server.shutdown()
