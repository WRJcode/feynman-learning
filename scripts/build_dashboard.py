"""Build a dependency-free, read-only dashboard from the learning records."""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'web' / 'index.html'

def esc(value):
    return escape(str(value), quote=True)

def github(path):
    return 'https://github.com/WRJcode/feynman-learning/blob/main/' + path.as_posix()

def render_links(value, base):
    parts, pos = [], 0
    for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', value):
        parts.append(esc(value[pos:match.start()]))
        target = match[2]
        path, _, anchor = target.partition('#')
        resolved = (base / path).resolve()
        try:
            relative = resolved.relative_to(ROOT)
        except ValueError:
            parts.append(esc(match[1]))
        else:
            if resolved.is_file():
                url = github(relative) + ('#' + anchor if anchor else '')
                parts.append(f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(match[1])} ↗</a>')
            else:
                raise ValueError(f'Broken evidence link: {resolved}')
        pos = match.end()
    return ''.join(parts) + esc(value[pos:])

topics, items = [], []
for index in sorted((ROOT / 'topics').glob('*/index.md')):
    content = index.read_text()
    title = content.splitlines()[0].removeprefix('# ')
    entries = []
    for line in content.splitlines():
        if not line.startswith('|'):
            continue
        fields = [s.strip() for s in line.strip('|').split('|')]
        if len(fields) != 4 or fields[0] == '知识点' or re.fullmatch(r'[- :]+', fields[0]):
            continue
        point, state, evidence, boundary = fields
        bucket = '能解释' if state.startswith('能解释') else '复测通过' if state.startswith('复测通过') else '能应用' if state.startswith('能应用') else '待验证／补充'
        item = dict(title=title, point=point, state=state, evidence=render_links(evidence,index.parent), boundary=boundary, bucket=bucket)
        entries.append(item)
        items.append(item)
    docs = []
    for path in [index.parent/'synthesis.md', index.parent/'sources.md', *sorted((index.parent/'sessions').glob('*.md'))]:
        if path.exists():
            label = {'synthesis.md':'当前总结与理解图','sources.md':'来源与证据'}.get(path.name, '学习会话 · ' + path.stem)
            docs.append(f'<a class="doc" href="{esc(github(path.relative_to(ROOT)))}" target="_blank" rel="noopener">{esc(label)} <span>↗</span></a>')
    topics.append(f'<article class="topic"><div class="eyebrow">学习主题</div><h3>{esc(title)}</h3><p>{len(entries)} 个知识点 · 复测待安排</p><details><summary>查看记录与来源</summary><div class="docs">{"".join(docs)}</div></details></article>')

columns = []
for bucket in ['待验证／补充','能解释','能应用','复测通过']:
    cards = []
    for item in items:
        if item['bucket'] != bucket:
            continue
        search = esc(' '.join([item['title'],item['point'],item['state'],item['boundary']]))
        cards.append(f'''<article class="card" data-search="{search}"><span class="tag">{esc(item['title'])}</span><h3>{esc(item['point'])}</h3><p class="state">{esc(item['state'])}</p><details><summary>证据与边界</summary><p class="evidence">{item['evidence']}</p><p>{esc(item['boundary'])}</p></details></article>''')
    columns.append(f'<section class="column"><h2>{bucket}<span>{len(cards)}</span></h2><div class="cards">{"".join(cards)}</div><p class="empty" {"hidden" if cards else ""}>暂无对应证据记录</p></section>')

html = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>费曼学习工作室 · 学习看板</title><style>
:root{--ink:#18372f;--muted:#6c7871;--line:#dce3da;--green:#27694e;--paper:#f7f8f2}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.65 system-ui,-apple-system,"PingFang SC",sans-serif}a{color:var(--green)}button,input{font:inherit}header{padding:22px 5vw;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;background:#fffefa}header strong{font-size:18px}nav{display:flex;gap:25px}nav a{text-decoration:none;font-size:14px}main{max-width:1500px;margin:auto;padding:48px 5vw}.eyebrow{font-size:11px;letter-spacing:2px;color:var(--green);font-weight:700}h1{font-size:clamp(30px,4vw,48px);line-height:1.25;letter-spacing:-1px;margin:12px 0 18px}h2{font-size:18px}h3{font-size:16px;line-height:1.5;margin:12px 0}p{color:var(--muted)}.hero{display:flex;justify-content:space-between;gap:30px;align-items:end}.hero p{max-width:650px}.notice{font-size:12px;background:#edf0e4;border:1px solid #dde2ce;padding:12px 16px;border-radius:10px;max-width:280px}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:30px 0 42px}.stat{padding:18px 22px;border:1px solid var(--line);border-radius:12px;background:#fffefa}.stat b{display:block;font-size:30px;font-weight:600}.stat span{font-size:12px;color:var(--muted)}.section-head{display:flex;align-items:center;justify-content:space-between;gap:20px;margin:25px 0 18px}.section-head h2{margin:0}.section-head p{margin:4px 0;font-size:13px}input{border:1px solid #bdcbbf;border-radius:9px;padding:10px 14px;background:#fff;min-width:260px;color:var(--ink)}input:focus,summary:focus,a:focus{outline:3px solid #97bba3;outline-offset:3px}.board{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;align-items:start}.column{background:#edf0e9;border-radius:14px;padding:14px;min-height:260px}.column>h2{font-size:14px;margin:2px 2px 16px;display:flex;justify-content:space-between}.column>h2 span{background:#dde4d9;border-radius:5px;padding:0 7px}.column:nth-child(2){background:#e8f0e9}.column:nth-child(3){background:#e7edf0}.column:nth-child(4){background:#eeeae2}.card{background:#fffefa;border:1px solid #dce2d7;border-radius:10px;padding:16px;margin-bottom:12px;box-shadow:0 2px 3px #1c382904}.tag{font-size:11px;letter-spacing:.3px;color:#47614d;background:#eef2e9;border-radius:4px;padding:3px 7px}.card .state{font-size:12px;margin-bottom:12px}.card p{font-size:12px}.evidence a{word-break:break-word}summary{cursor:pointer;color:var(--green);font-size:12px;font-weight:600}.empty{font-size:12px;text-align:center;margin:50px 0}.topics{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.topic{padding:24px;background:#fffefa;border:1px solid var(--line);border-radius:12px}.topic h3{font-size:24px;margin:6px 0}.topic p{font-size:13px}.docs{margin-top:15px}.doc{display:flex;justify-content:space-between;font-size:13px;padding:8px 0;border-top:1px solid var(--line);text-decoration:none}.next{margin-top:32px;padding:24px 28px;border-radius:12px;border:1px solid #c8d7c8;background:#edf3e9}.next p{margin-bottom:0;font-size:14px}footer{font-size:12px;color:var(--muted);margin:36px 0 0;border-top:1px solid var(--line);padding-top:20px}[hidden]{display:none!important}@media(max-width:1000px){.board{grid-template-columns:repeat(2,minmax(0,1fr))}.hero{display:block}.notice{max-width:none}.topics{grid-template-columns:1fr}.stats{gap:8px}.stat{padding:14px}}@media(max-width:600px){main{padding:28px 18px}.board{grid-template-columns:1fr}.stats{grid-template-columns:repeat(2,1fr)}nav{gap:12px}header{padding:18px}.section-head{align-items:stretch;flex-direction:column}input{min-width:0;width:100%}}
</style><header><strong>◈ 费曼学习工作室</strong><nav aria-label="页面导航"><a href="#board">理解看板</a><a href="#topics">主题档案</a></nav></header><main>
<div class="hero"><div><div class="eyebrow">FEYNMAN LEARNING STUDIO</div><h1>让理解留下证据。</h1><p>从材料出发，用自己的话解释，建立关联，再到真实问题中检验。这里记录走到了哪里，也保留尚未确定的地方。</p></div><aside class="notice">本地设计预览 · 只读<br>取自仓库真实记录；不会自动提升掌握状态。尚未发布至 GitHub Pages。</aside></div>
<div class="stats">STATS</div>
<div class="section-head" id="board"><div><h2>理解看板</h2><p>按知识点查看证据状态。同一主题可以处于不同阶段。</p></div><label><span class="eyebrow">搜索知识点</span><br><input id="search" type="search" placeholder="搜索主题、概念或未决问题…"></label></div>
<div class="board">BOARD</div><p id="result" aria-live="polite"></p>
<div class="section-head" id="topics"><div><h2>主题档案</h2><p>回到原话、来源和理解图，检查每个判断从哪里来。</p></div></div><div class="topics">TOPICS</div>
<section class="next"><div class="eyebrow">下一次学习可以从这里开始 · AI 建议</div><h2>把一个解释，用到一个真实问题里。</h2><p>例如：观察一次 Codex 工具执行失败，区分模型决策、执行框架和环境权限各自的作用。是否开始、何时复测，由你决定。</p></section>
<footer>基于 topics/*/index.md 自动生成 · 当前记录日期 2026-11-12（UTC） · 复测均待安排，无后台提醒 · 证据链接前往原 GitHub 仓库，私有记录需要登录。</footer></main><script>
const input=document.querySelector('#search');const cards=[...document.querySelectorAll('.card')];input.addEventListener('input',()=>{const term=input.value.trim().toLocaleLowerCase();let visible=0;for(const card of cards){card.hidden=!card.dataset.search.toLocaleLowerCase().includes(term);if(!card.hidden)visible++}for(const column of document.querySelectorAll('.column')){const n=[...column.querySelectorAll('.card')].filter(c=>!c.hidden).length;column.querySelector('h2 span').textContent=n;column.querySelector('.empty').hidden=n>0;column.querySelector('.empty').textContent=term?'没有匹配的知识点':'暂无对应证据记录'}document.querySelector('#result').textContent=term?`找到 ${visible} 个知识点`:''});
</script></html>'''
counts = [len(topics), len(items), sum(i['bucket']=='能解释' for i in items), sum(i['bucket']=='复测通过' for i in items)]
labels = ['已归档主题','有记录的知识点','有解释证据的知识点','复测通过的知识点']
stats = ''.join(f'<div class="stat"><b>{n:02}</b><span>{label}</span></div>' for n,label in zip(counts,labels))
OUT.write_text(html.replace('STATS',stats).replace('BOARD',''.join(columns)).replace('TOPICS',''.join(topics)))
print(f'Built {OUT}: {len(topics)} topics, {len(items)} knowledge points.')
