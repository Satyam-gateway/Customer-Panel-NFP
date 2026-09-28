import io, re

p = 'relay-prototype.html'
s = io.open(p, encoding='utf-8').read()

# ------------------------------------------------ 1. remove the old engineers blocks
old_ret = '''      <div class="quiet">
        <div class="quiet-h">Engineers who know your projects</div>
        <div class="faces">
          <button class="face" data-person="sj">
            <div class="av lg" data-dot="live" style="background:#00875A">SJ</div>
            <span>Satyam</span><small>Free now</small>
          </button>
          <button class="face" data-person="pn">
            <div class="av lg" data-dot="live" style="background:#2456C8">PN</div>
            <span>Priya</span><small>Free now</small>
          </button>
          <button class="face" data-person="ad">
            <div class="av lg" data-dot="off" style="background:#9AA1A6">AD</div>
            <span>Arjun</span><small>Back Friday</small>
          </button>
        </div>
        <div class="newprob">
          <span>Something new they have not seen before?</span>
          <button class="btn">Describe it and get matched</button>
        </div>
      </div>
'''
assert old_ret in s, 'returning engineers block not found'
s = s.replace(old_ret, '')

old_assist = '''        <div class="quiet">
          <div class="quiet-h">Engineers who know your projects</div>
          <div class="faces">
            <button class="face" data-person="sj">
              <div class="av lg" data-dot="live" style="background:#00875A">SJ</div>
              <span>Satyam</span><small>Free now</small>
            </button>
            <button class="face" data-person="pn">
              <div class="av lg" data-dot="live" style="background:#2456C8">PN</div>
              <span>Priya</span><small>Free now</small>
            </button>
            <button class="face" data-person="ad">
              <div class="av lg" data-dot="off" style="background:#9AA1A6">AD</div>
              <span>Arjun</span><small>Back Friday</small>
            </button>
          </div>
        </div>
'''
assert old_assist in s, 'assist engineers block not found'
s = s.replace(old_assist, '')

# ------------------------------------------------ 2. stories rail in the header
old_head = '''        <div class="viewswitch" title="Demo only &mdash; not part of the product">
          <span>Viewing as</span>
          <button class="vs on" data-view="returning">Returning</button>
          <button class="vs" data-view="assist">No contracts</button>
          <button class="vs" data-view="new">First time</button>
        </div>'''
new_head = '''        <div class="head-right">
          <div class="viewswitch" title="Demo only &mdash; not part of the product">
            <span>Viewing as</span>
            <button class="vs on" data-view="returning">Returning</button>
            <button class="vs" data-view="assist">No contracts</button>
            <button class="vs" data-view="new">First time</button>
          </div>

          <div class="stories v-greet">
            <button class="story add" title="Describe something new and get matched">
              <span class="ring"><span class="plus">+</span></span>
              <span class="s-name">New</span>
            </button>
            <button class="story live" data-person="sj">
              <span class="ring"><span class="av" style="background:#00875A">SJ</span></span>
              <span class="s-name">Satyam</span>
            </button>
            <button class="story live" data-person="pn">
              <span class="ring"><span class="av" style="background:#2456C8">PN</span></span>
              <span class="s-name">Priya</span>
            </button>
            <button class="story off" data-person="ad">
              <span class="ring"><span class="av" style="background:#9AA1A6">AD</span></span>
              <span class="s-name">Arjun</span>
            </button>
          </div>
        </div>'''
assert old_head in s
s = s.replace(old_head, new_head)

# ------------------------------------------------ 3. styles
css_anchor = '/* ---------- chats: thread switching ---------- */'
stories_css = '''/* ---------- home: engineer stories rail ---------- */
.head-right{display:flex;flex-direction:column;align-items:flex-end;gap:14px;flex:none}
.stories{display:flex;gap:11px;align-items:flex-start}
.story{background:none;border:0;padding:0;cursor:pointer;
  display:flex;flex-direction:column;align-items:center;gap:5px;width:56px}
.story .ring{width:48px;height:48px;border-radius:50%;padding:2.5px;
  display:grid;place-items:center;box-sizing:border-box;transition:transform .12s ease}
.story:hover .ring{transform:scale(1.06)}
.story .ring .av{width:100%;height:100%;box-shadow:0 0 0 2px var(--paper)}
.story.live .ring{background:conic-gradient(from 210deg,#00875A,#43C59E,#00875A)}
.story.busy .ring{background:conic-gradient(from 210deg,#B45309,#E3A14B,#B45309)}
.story.off .ring{background:var(--line)}
.story.off .av-img{filter:grayscale(.85);opacity:.75}
.story.add .ring{background:none;border:1.5px dashed var(--faint);place-items:center}
.story.add:hover .ring{border-color:var(--live);background:var(--live-bg)}
.plus{font-size:21px;font-weight:300;color:var(--faint);line-height:1}
.story.add:hover .plus{color:var(--live)}
.s-name{font-size:11px;font-weight:600;color:var(--muted);
  max-width:56px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.story.off .s-name{color:var(--faint)}
#home[data-view="new"] .stories{display:none}
@media (max-width:1100px){
  .home-head{flex-direction:column;align-items:stretch}
  .head-right{align-items:flex-start}
}

'''
assert css_anchor in s
s = s.replace(css_anchor, stories_css + css_anchor)

io.open(p, 'w', encoding='utf-8').write(s)
print('stories rail added')
