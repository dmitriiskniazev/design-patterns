(() => {
  'use strict';
  const topics = window.COURSE_TOPICS;
  const $ = selector => document.querySelector(selector);
  const categories = {behavioral:'Поведенческие',creational:'Порождающие',structural:'Структурные',practical:'Практические подходы · вне GoF'};
  const views = ['explanation','examples','implementation'];
  const escape = value => String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const preference = key => {try{return localStorage.getItem(`patterns.${key}`);}catch{return null;}};
  const savePreference = (key,value) => {try{localStorage.setItem(`patterns.${key}`,value);}catch{}};
  let savedPosition = null;
  try { savedPosition = JSON.parse(preference('reading') || 'null'); } catch {}
  const resume = !location.hash && savedPosition && typeof savedPosition.hash === 'string' && savedPosition.hash.startsWith('#');
  if (resume) history.replaceState(null, '', savedPosition.hash);
  const rememberPosition = () => savePreference('reading', JSON.stringify({hash: location.hash, y: window.scrollY}));
  window.addEventListener('pagehide', rememberPosition);
  document.addEventListener('visibilitychange', () => { if (document.hidden) rememberPosition(); });
  let scrollTimer;
  window.addEventListener('scroll', () => {
    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(rememberPosition, 250);
  }, {passive: true});
  let state;
  let outlineObserver;
  let showSourceDiff=true;
  const sourceSelections = new Map();

  function parseHash() {
    let parts;
    try {parts=decodeURIComponent(location.hash.slice(1)).split('/');} catch {parts=[];}
    const topic=topics.find(t=>t.id===parts[0]) || topics.find(t=>t.id==='strategy');
    const language=['cpp','python'].includes(parts[1]),offset=language?2:1;
    const requested=parts[offset] || 'explanation';
    let section=parts.slice(offset+1).find(part=>/^s[1-5]$/.test(part));
    section=/^s[1-5]$/.test(section || '')?section:null;
    let view=views.includes(requested)?requested:({code:'examples',extension:'examples',practice:'explanation'}[requested] || 'explanation');
    if(!views.includes(requested)){
      section=section || ({code:'s2',extension:'s3',practice:'s4'}[requested] || null);
    }
    if(section)view=({s1:'explanation',s2:'examples',s3:'examples',s4:'explanation',s5:'implementation'})[section];
    let compare=null,implementation=null,mode=null,beforeFile=null,afterFile=null;
    if(view==='implementation' && topic.ready){
      const marker=parts[offset+1],previous=sourceSelections.get(topic.id) || {};
      let selection=previous;
      if(marker==='extension')selection={compare:'extension',implementation:parts[offset+2]==='without-pattern'?'before':'after',beforeFile:parts[offset+3],afterFile:parts[offset+4]};
      else if(['base','extended'].includes(marker))selection={compare:'pattern',mode:marker,beforeFile:parts[offset+2],afterFile:parts[offset+3]};
      else if(/^v[1-9]\d*$/.test(marker || '')){
        const legacy=Number(marker.slice(1))-1,index=topic.guide.legacyVersionIndices[legacy] ?? 1;
        const version=topic.guide.versions[index],side=version.key.startsWith('before')?'beforeFile':'afterFile';
        selection={compare:'pattern',mode:version.extended?'extended':'base',[side]:parts[offset+2]};
      }
      const pair=sourcePair(topic.guide,selection);
      compare=pair.compare;implementation=pair.implementation;mode=pair.mode;
      beforeFile=pair.before.ref.name;afterFile=pair.after.ref.name;
    }
    return {topic:topic.id,view,step:0,section,compare,implementation,mode,beforeFile,afterFile};
  }
  function hash(selection) {
    let source='';
    if(selection.view==='implementation'&&selection.compare==='extension'){
      source='/extension/'+(selection.implementation==='before'?'without-pattern':'with-pattern');
    }else if(selection.view==='implementation'&&selection.mode){
      source='/'+selection.mode;
    }
    if(source)source+='/'+encodeURIComponent(selection.beforeFile || '-')+'/'+encodeURIComponent(selection.afterFile || '-');
    return `#${selection.topic}/${selection.view}${source}${selection.section?'/'+selection.section:''}`;
  }
  function readingPosition(topic) {
    const ready=topics.filter(item=>item.ready),index=ready.indexOf(topic);
    return {index,total:ready.length,
      previous:index>0?{topic:ready[index-1].id,view:'explanation',step:0}:null,
      next:index<ready.length-1?{topic:ready[index+1].id,view:'explanation',step:0}:null};
  }
  function readingNavigation(topic) {
    const position=readingPosition(topic);
    const next=position.next;
    const label=!next?'':next.topic!==topic.id?`Следующая тема: ${topics.find(item=>item.id===next.topic).name}`:
      next.view!==state.view?({code:'Перейти к решению',practice:'Попробовать самостоятельно',extension:'Разобрать расширение'}[next.view]):'Следующий шаг';
    return `<nav class="step-actions" aria-label="Порядок чтения">${position.previous?`<a class="subtle-button" href="${hash(position.previous)}">← Назад</a>`:'<span></span>'}${next?`<a class="next-button" href="${hash(next)}">${escape(label)} →</a>`:'<p class="course-complete" role="status">Последняя тема курса.</p>'}</nav>`;
  }
  function closeCatalog(restoreFocus=false) {
    const focusInside=$('#catalog').contains(document.activeElement);
    document.body.classList.remove('catalog-open');
    $('#catalog-toggle').setAttribute('aria-expanded','false');
    $('.backdrop').hidden=true;
    $('.workspace').inert=false;
    if(restoreFocus) $('#catalog-toggle').focus();
    else if(focusInside) $('#topic-title').focus({preventScroll:true});
  }
  function renderCatalog() {
    const query=$('#topic-search').value.trim().toLocaleLowerCase('ru');
    const matches=topics.filter(t=>`${t.name} ${t.ru}`.toLocaleLowerCase('ru').includes(query));
    $('#search-status').textContent=`Найдено тем: ${matches.length}`;
    $('#topic-list').innerHTML=Object.entries(categories).map(([category,label])=>{
      const group=matches.filter(t=>t.category===category);
      if(!group.length)return '';
      return `<section class="topic-group"><h2>${label}</h2>${group.map(t=>`<a class="topic-link" href="${hash({...state,topic:t.id,section:null,step:0,view:'explanation'})}" ${state.topic===t.id?'aria-current="page"':''} title="${escape(t.ru)}"><span class="number">${String(topics.indexOf(t)+1).padStart(2,'0')}</span><span class="topic-name">${escape(t.name)}</span>${t.ready?'':'<span class="planned-marker">В плане</span>'}</a>`).join('')}</section>`;
    }).join('') || '<div class="empty-state"><p>Тем с таким названием нет.</p><button class="text-button" id="clear-search">Очистить поиск</button></div>';
    $('#clear-search')?.addEventListener('click',()=>{$('#topic-search').value='';renderCatalog();$('#topic-search').focus();});
    $('#topic-list').querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>closeCatalog()));
  }
  function guideDiagramPair(topic) {
    const diagrams=topic.guide.diagrams,id=`map-${topic.id}`,nodes=new Map(),refs={before:new Map(),after:new Map()};
    for(const side of ['before','after'])diagrams[side].nodes.forEach((node,index)=>{
      const key=JSON.stringify([node.label,node.role]);
      if(!nodes.has(key))nodes.set(key,{...node,key,row:index,sides:[]});
      const item=nodes.get(key);item.row=Math.max(item.row,index);item.sides.push(side);refs[side].set(node.id,item);
    });
    const width=800,height=Math.max(...[...nodes.values()].map(n=>n.row))*76+86;
    const position=node=>({x:node.sides.length===2?245:node.sides[0]==='before'?20:470,y:30+node.row*76});
    const edges=new Map();
    for(const side of ['before','after'])for(const edge of diagrams[side].edges){
      const a=refs[side].get(edge.from),b=refs[side].get(edge.to),key=JSON.stringify([a.key,b.key,edge.label]);
      if(!edges.has(key))edges.set(key,{a,b,label:edge.label,sides:[]});edges.get(key).sides.push(side);
    }
    const paths=[...edges.values()].map((edge,i)=>{
      const a=position(edge.a),b=position(edge.b),forward=b.y>a.y,shared=edge.sides.length===2,side=edge.sides[0];
      const offset=node=>node.sides.length===2&&!shared?(side==='before'?-90:90):0;
      const ax=a.x+155+offset(edge.a),bx=b.x+155+offset(edge.b),ay=a.y+44,by=b.y-5;
      const adjacent=forward&&b.y-a.y===76,port=side==='before'?310:0,lane=side==='before'?375:425;
      const path=adjacent?`M ${ax} ${ay} C ${ax} ${(ay+by)/2}, ${bx} ${(ay+by)/2}, ${bx} ${by}`:
        `M ${a.x+port} ${a.y+22} C ${lane} ${a.y+22}, ${lane} ${b.y+22}, ${b.x+port+(port?6:-6)} ${b.y+22}`;
      const tx=adjacent?(ax+bx)/2:lane+(side==='before'?-5:12),ty=adjacent?(ay+by)/2-4:(a.y+b.y)/2+22;
      return `<path class="guide-edge ${shared?'shared':side}" d="${path}" marker-end="url(#${id}-arrow)"/><text class="guide-edge-label" text-anchor="middle" x="${tx}" y="${ty}" ${adjacent?'':`transform="rotate(90 ${tx} ${ty})"`}>${escape(edge.label)}</text>`;
    }).join('');
    const boxes=[...nodes.values()].map(node=>{
      const p=position(node),kind=node.sides.length===2?'shared':node.sides[0];
      return `<g class="guide-node ${kind}"><rect x="${p.x}" y="${p.y}" width="310" height="44" rx="5"/><text x="${p.x+12}" y="${p.y+18}" class="guide-node-name">${escape(node.label)}</text><text x="${p.x+12}" y="${p.y+34}" class="guide-node-role">${escape(node.role)}</text></g>`;
    }).join('');
    const description=['before','after'].map(side=>`${side==='before'?'Без паттерна':'С паттерном'}: `+diagrams[side].edges.map(edge=>`${diagrams[side].nodes.find(n=>n.id===edge.from).label} → ${diagrams[side].nodes.find(n=>n.id===edge.to).label}: ${edge.label}`).join('; ')).join('. ');
    return `<figure class="guide-diagram guide-combined"><figcaption>Один вызов: где расходятся подходы <small>Общие участники показаны один раз в центре.</small></figcaption><svg viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="${id}-title ${id}-desc"><title id="${id}-title">${escape(topic.name)}: сравнение подходов</title><desc id="${id}-desc">${escape(description)}</desc><defs><marker id="${id}-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker></defs><text x="175" y="18" text-anchor="middle" class="guide-column-label">Без паттерна</text><text x="625" y="18" text-anchor="middle" class="guide-column-label">С паттерном</text>${paths}${boxes}</svg></figure>`;
  }
  function fragmentLocation(selectors) {
    return selectors.map(selector=>selector==='@usage'?'запуск примера':selector==='@module'?'модуль':selector.startsWith('body:')?'тело метода '+selector.slice(5):selector.startsWith('fields:')?'поля '+selector.slice(7):selector).join(', ');
  }
  function guideFragment(snippet, label) {
    return `<section class="guide-variant"><p class="guide-side">${label}</p><p class="code-note"><code>${escape(snippet.path.split('/').pop())}</code> · ${escape(fragmentLocation(snippet.selectors))}</p>${snippet.differenceHtml?`<div class="code-window"><div class="code-heading"><span>Различающиеся строки</span><button class="copy-button" data-copy-file>Копировать строки</button></div><pre tabindex="0" aria-label="Различающиеся строки: ${label}"><code class="source-code">${snippet.differenceHtml}</code></pre><div class="code-caption"><span class="file-copy-status" role="status"></span></div></div>`:'<p class="code-note">Дополнительного кода нет.</p>'}</section>`;
  }
  function guideShared(html, label) {
    return html.trim()?`<div class="guide-shared"><p class="code-note">${label} · одинаково в обеих версиях</p><div class="code-window"><pre tabindex="0"><code class="source-code">${html}</code></pre></div></div>`:'';
  }
  function sourceSelection(guide, selection={}) {
    const index=Number.isInteger(selection.version)&&selection.version>=0&&selection.version<guide.versions.length?selection.version:1;
    const version=guide.versions[index],fallback=version.defaultFile;
    const name=guide.fileAliases?.[selection.file] || selection.file;
    const ref=version.files.find(file=>file.name===name) || version.files.find(file=>file.name===fallback);
    return {index,version,ref,file:guide.sources.find(file=>file.id===ref.id)};
  }
  function sourcePair(guide, selection={}) {
    const compare=selection.compare==='extension'?'extension':'pattern';
    const implementation=selection.implementation==='before'?'before':'after';
    const mode=selection.mode==='extended'?'extended':'base';
    const indices=compare==='extension'?
      {before:guide.pairs.base[implementation],after:guide.pairs.extended[implementation]}:guide.pairs[mode];
    return {compare,implementation,mode,hasExtension:compare==='extension'||mode==='extended',
      labels:compare==='extension'?{before:'Без расширения',after:'С расширением'}:{before:'Без паттерна',after:'С паттерном'},
      before:sourceSelection(guide,{version:indices.before,file:selection.beforeFile}),
      after:sourceSelection(guide,{version:indices.after,file:selection.afterFile})};
  }
  function sourceHref(pair, side, name) {
    return hash({...state,view:'implementation',compare:pair.compare,implementation:pair.implementation,mode:pair.mode,
      beforeFile:side==='before'?name:pair.before.ref.name,afterFile:side==='after'?name:pair.after.ref.name,section:null});
  }
  function handleSourceComparisonChange(event) {
    location.hash=hash({...state,view:'implementation',compare:event.target.value,implementation:'after',mode:'base',beforeFile:null,afterFile:null,section:null});
  }
  function handleSourceModeChange(event) {
    location.hash=hash({...state,view:'implementation',mode:event.target.value,beforeFile:null,afterFile:null,section:null});
  }
  function handleSourceImplementationChange(event) {
    location.hash=hash({...state,view:'implementation',implementation:event.target.value,beforeFile:null,afterFile:null,section:null});
  }
  function visibleSourceDiff(selected) {
    return selected.version.extended&&showSourceDiff&&selected.ref.change!=='unchanged'?selected.ref.diff:null;
  }
  function sourceRows(guide, pair) {
    const files=side=>pair[side].version.files.map(ref=>sourceSelection(guide,{version:pair[side].index,file:ref.name}));
    const before=files('before'),after=files('after');
    const key=file=>file.file.id+JSON.stringify(visibleSourceDiff(file));
    const left=before.map(key),right=after.map(key);
    // Common anchors must preserve the reading order in both columns.
    const lengths=Array.from({length:left.length+1},()=>Array(right.length+1).fill(0));
    for(let i=left.length-1;i>=0;i--)for(let j=right.length-1;j>=0;j--){
      lengths[i][j]=left[i]===right[j]?1+lengths[i+1][j+1]:Math.max(lengths[i+1][j],lengths[i][j+1]);
    }
    const anchors=[];
    let i=0,j=0;
    while(i<left.length&&j<right.length){
      if(left[i]===right[j]){anchors.push([i++,j++]);}
      else if(lengths[i+1][j]>=lengths[i][j+1])i++;
      else j++;
    }
    const rows=[];
    i=0;j=0;
    for(const [endLeft,endRight] of [...anchors,[before.length,after.length]]){
      while(i<endLeft||j<endRight)rows.push({before:i<endLeft?before[i++]:null,after:j<endRight?after[j++]:null,common:false});
      if(endLeft<before.length&&endRight<after.length)rows.push({before:before[i++],after:after[j++],common:true});
    }
    return rows;
  }
  function focusSourceFile(previous, preferredSide=null) {
    if(state.view!=='implementation'||state.section)return;
    const guide=topics.find(topic=>topic.id===state.topic).guide,pair=sourcePair(guide,state);
    const samePair=previous?.topic===state.topic&&previous.view===state.view&&
      previous.compare===state.compare&&previous.implementation===state.implementation&&previous.mode===state.mode;
    const side=preferredSide || (samePair&&previous.beforeFile!==state.beforeFile?'before':
      samePair&&previous.afterFile!==state.afterFile?'after':
      state.afterFile!==pair.after.version.entry?'after':state.beforeFile!==pair.before.version.entry?'before':'after');
    const name=state[side+'File'];
    const card=[...document.querySelectorAll('.source-file')].find(element=>element.dataset[side+'File']===name);
    if(card){card.scrollIntoView({block:'start'});card.focus({preventScroll:true});}
  }
  function sourceCode(selected, side) {
    const {ref,file}=selected,lineCount=file.code.replace(/\n$/,'').split('\n').length;
    const diff=visibleSourceDiff(selected);
    const code=diff?`<div class="source-code-scroll"><pre class="source-diff" tabindex="0" aria-label="Изменения файла ${escape(file.name)}"><code class="source-code">${diff.rows.map(row=>`<span class="diff-line diff-${row.kind}"><span class="diff-number" aria-hidden="true">${row.beforeLine ?? ''}</span><span class="diff-number" aria-hidden="true">${row.afterLine ?? ''}</span><span class="diff-marker" aria-hidden="true">${{added:'+',removed:'−',equal:' '}[row.kind]}</span>${row.kind==='equal'?'':`<span class="sr-only">${row.kind==='added'?'Добавлено: ':'Удалено: '}</span>`}<span class="diff-content">${row.html || ' '}</span></span>`).join('')}</code></pre></div>`:
      `<div class="source-code-scroll"><pre class="source-line-numbers" aria-hidden="true">${Array.from({length:lineCount},(_,i)=>i+1).join('\n')}</pre><pre tabindex="0" aria-label="Полный файл ${escape(file.name)}"><code class="source-code">${file.html}</code></pre></div>`;
    const caption=diff?(diff.baseName?`Изменения относительно ${escape(diff.baseName)}`:'Новый файл · все строки добавлены'):`${lineCount} строк · полный файл`;
    return `<div class="code-window source-code-window" data-source-side="${side}" data-source-path="${escape(ref.path)}"><div class="code-heading"><span>${caption}</span><button class="copy-button" data-copy-file data-copy-source="${file.id}">Копировать файл</button></div>${code}<div class="code-caption"><span class="file-copy-status" role="status"></span></div></div>`;
  }
  function sourcePane(pair, side) {
    const {version}=pair[side];
    return `<header class="source-pane" data-side="${side}"><h3>${pair.labels[side]}</h3>${version.command?`<div class="run-command"><code>${escape(version.command)}</code></div>`:''}</header>`;
  }
  function sourceCard(pair, selected, side, common=false) {
    const {version,ref,file}=selected;
    const imports=file.imports.map(name=>version.files.find(item=>item.name===name)).filter(Boolean);
    const change=version.extended?{added:'Новый файл',modified:'Изменён',unchanged:'Без изменений'}[ref.change]:'';
    const anchors=common?`data-before-file="${escape(ref.name)}" data-after-file="${escape(ref.name)}"`:`data-${side}-file="${escape(ref.name)}"`;
    const heading=`source-heading-${side}-${file.id}`;
    return `<section class="source-file${common?' source-common':''}" data-side="${common?'common':side}" ${anchors} tabindex="-1" aria-labelledby="${heading}"><div class="source-purpose"><span class="source-file-side${common?' source-common-label':''}">${common?'Общий файл':pair.labels[side]}</span><h4 id="${heading}">${escape(ref.name)}</h4>${change?`<span class="file-change">${change}</span>`:''}<p>${escape(ref.role)}</p>${imports.length?`<p class="source-imports">Использует: ${imports.map(item=>`<a data-source-side="${side}" data-source-file="${escape(item.name)}" href="${sourceHref(pair,side,item.name)}">${escape(item.name)}</a>`).join(' · ')}</p>`:''}</div>${sourceCode(selected,common?'common':side)}</section>`;
  }
  function guideSources(guide) {
    const pair=sourcePair(guide,state.view==='implementation'?state:sourceSelections.get(state.topic));
    const files=sourceRows(guide,pair).map(row=>row.common?sourceCard(pair,row.before,'before',true):
      ['before','after'].map(side=>row[side]?sourceCard(pair,row[side],side):'<div class="source-gap" aria-hidden="true"></div>').join('')).join('');
    const options=pair.compare==='extension'?[['before','Без паттерна'],['after','С паттерном']]:[['base','Базовый'],['extended','С расширением']];
    const control=pair.compare==='extension'?'implementation':'mode';
    const selected=pair.compare==='extension'?pair.implementation:pair.mode;
    const controls=`<div class="source-controls"><label class="source-compare-label" for="source-compare">Сравнить<select id="source-compare">${[['pattern','Без паттерна / С паттерном'],['extension','Без расширения / С расширением']].map(([value,label])=>`<option value="${value}" ${pair.compare===value?'selected':''}>${label}</option>`).join('')}</select></label><fieldset class="source-mode"><legend>${pair.compare==='extension'?'Реализация':'Пример'}</legend>${options.map(([value,label])=>`<label><input type="radio" name="source-${control}" id="source-${control}-${value}" value="${value}" ${selected===value?'checked':''}>${label}</label>`).join('')}</fieldset></div>`;
    return `<section class="source-reader"><h2 data-section-target="s5">Полная реализация</h2>${controls}${pair.hasExtension?`<label class="source-diff-toggle"><input type="checkbox" id="source-diff" ${showSourceDiff?'checked':''}> Изменения</label><p class="source-requirement"><strong>Новое требование:</strong> ${escape(guide.extensionRequirement)}</p>`:''}<div class="source-pair">${sourcePane(pair,'before')}${sourcePane(pair,'after')}${files}</div></section>`;
  }
  function handleChapterTabKey(event) {
      if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
      const tabs=[...event.currentTarget.querySelectorAll('[role="tab"]')];
      const index=tabs.indexOf(document.activeElement);if(index<0)return;
      event.preventDefault();
      const next=event.key==='Home'?0:event.key==='End'?tabs.length-1:(index+(event.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;
      tabs[next].focus();tabs[next].click();
  }
  function guideLesson(topic) {
    const g=topic.guide,t=g.trace;
    const additionalRoles=g.roles.filter(role=>!g.terms.some(term=>term.term===role.name&&term.definition===role.purpose));
    const explanation=`<section class="guide-section"><h2 data-section-target="s1">Задача и устройство</h2><dl class="guide-definition"><dt>Цель</dt><dd>${escape(g.goal)}</dd><dt>Вход</dt><dd>${escape(g.input)}</dd><dt>Инвариант<small>Что остаётся верным</small></dt><dd>${escape(g.invariant)}</dd></dl><details class="guide-terms"><summary>Термины и роли</summary><dl>${g.terms.map(item=>`<dt>${escape(item.term)}</dt><dd>${escape(item.definition)}</dd>`).join('')}</dl><dl class="role-list">${additionalRoles.map(role=>`<dt><code>${escape(role.name)}</code></dt><dd>${escape(role.purpose)}</dd>`).join('')}</dl></details>${guideDiagramPair(topic)}<details class="guide-trace"><summary>Проследить вызов</summary><p class="section-label">Один и тот же вход</p><p><code>${escape(t.input)}</code></p><div class="guide-trace-pair"><p><strong>Без паттерна</strong><br>${escape(t.before)}</p><p><strong>С паттерном</strong><br>${escape(t.after)}</p></div><p class="guide-result"><strong>Результат:</strong> ${escape(t.result)}</p></details><div class="guide-design"><h3>Почему так устроено</h3>${g.designNotes.map(note=>`<p>${escape(note)}</p>`).join('')}</div></section><section class="guide-section"><h2 data-section-target="s4">Где применять и когда остановиться</h2><div class="guide-decision"><p><strong>Применять</strong><br>${escape(g.decision.use)}</p><p><strong>Оставить простое решение</strong><br>${escape(g.decision.skip)}</p></div><details class="guide-more"><summary>Другие применения</summary><div class="guide-applications">${g.applications.map(example=>`<article><h4>${escape(example.case)}</h4><p>${escape(example.why)}</p></article>`).join('')}</div></details><h3>Проверьте понимание</h3><p>${escape(topic.fileComparison?.architecture.exercise || topic.exercise)}</p><details><summary>Вопрос для собеседования</summary><p>${escape(topic.interview)}</p></details></section>`;
    const examples=`<section class="guide-section"><h2 data-section-target="s2">Разница в реализации</h2><p class="code-note">Только существенные фрагменты из исходников. Общие строки показаны один раз; импорты и полные файлы — во вкладке «Полная реализация».</p>${g.contrasts.map((row,i)=>`<section class="guide-contrast"><h3>${i+1}. ${escape(row.title)}</h3>${guideShared(row.commonBefore,'Общее начало')}<div class="guide-code-pair">${guideFragment(row.before,'Без паттерна')}${guideFragment(row.after,'С паттерном')}</div>${guideShared(row.commonAfter,'Общее завершение')}<p class="guide-takeaway">${escape(row.explanation)}</p></section>`).join('')}</section><section class="guide-section"><h2 data-section-target="s3">Что происходит при росте</h2><div class="guide-table-wrap"><table class="guide-growth"><thead><tr><th scope="col">Изменение</th><th scope="col">Без паттерна</th><th scope="col">С паттерном</th></tr></thead><tbody>${g.growth.map(row=>`<tr><th scope="row">${escape(row.change)}<small>${escape(row.verdict)}</small></th><td>${escape(row.before)}</td><td>${escape(row.after)}</td></tr>`).join('')}</tbody></table></div><p class="code-note">Здесь масштабирование означает рост вариантов и требований. Производительность эти примеры не измеряют.</p></section>`;
    const implementation=guideSources(g);
    const labels={explanation:'Объяснение',examples:'Примеры',implementation:'Полная реализация'};
    const panels={explanation,examples,implementation};
    return `<nav class="chapter-tabs" role="tablist" aria-label="Разделы главы">${views.map(view=>`<a role="tab" id="chapter-tab-${view}" aria-controls="chapter-panel-${view}" aria-selected="${state.view===view}" tabindex="${state.view===view?0:-1}" href="${hash({...state,view,section:null})}">${labels[view]}</a>`).join('')}</nav>${views.map(view=>`<section class="guide-panel" role="tabpanel" id="chapter-panel-${view}" aria-labelledby="chapter-tab-${view}" tabindex="0" ${state.view===view?'':'hidden'}>${panels[view]}</section>`).join('')}<p class="code-note"><a href="${escape(topic.source)}" target="_blank" rel="noopener">${escape(topic.sourceLabel || `Источник: ${topic.name}`)} ↗</a></p>`;
  }

  function focusSection() {
    const heading=state.section?(document.getElementById(`lesson-${state.section}`) || document.querySelector(`[data-section-target="${state.section}"]`)):null;
    if(!heading)return;
    const disclosure=heading.closest('details');
    if(disclosure)disclosure.open=true;
    heading.scrollIntoView({block:'start'});
    heading.focus({preventScroll:true});
    $('.mobile-toc').open=false;
    markSection(state.section);
  }
  function markSection(section) {
    document.querySelectorAll('[data-section]').forEach(link=>{
      if(link.dataset.section===section)link.setAttribute('aria-current','location');
      else link.removeAttribute('aria-current');
    });
  }
  function renderOutline() {
    outlineObserver?.disconnect();
    const headings=[...$('#lesson-body').querySelectorAll('.guide-panel:not([hidden]) h2')];
    headings.forEach((heading,i)=>{heading.id=`lesson-${heading.dataset.sectionTarget}`;heading.tabIndex=-1;});
    const markup=headings.map((heading,i)=>`<a data-section="${heading.dataset.sectionTarget}" href="${hash({...state,section:heading.dataset.sectionTarget})}">${escape(heading.textContent)}</a>`).join('');
    $('#page-toc').innerHTML=markup;
    $('#mobile-page-toc').innerHTML=markup;
    document.querySelectorAll('[data-section]').forEach(link=>link.addEventListener('click',event=>{
      if(link.getAttribute('href')===location.hash){event.preventDefault();focusSection();}
    }));
    $('.page-outline').hidden=!headings.length;
    $('.mobile-toc').hidden=!headings.length;
    if(typeof IntersectionObserver==='function'){
      const visibleHeadings=new Set();
      outlineObserver=new IntersectionObserver(entries=>{
        entries.forEach(entry=>{if(entry.isIntersecting)visibleHeadings.add(entry.target);else visibleHeadings.delete(entry.target);});
        const visible=[...visibleHeadings].sort((a,b)=>a.getBoundingClientRect().top-b.getBoundingClientRect().top);
        const current=visible[0] || [...headings].reverse().find(heading=>heading.getBoundingClientRect().top<=80);
        if(current)markSection(current.dataset.sectionTarget || current.id.replace('lesson-',''));
      },{rootMargin:'-80px 0px -55% 0px',threshold:0});
      headings.forEach(heading=>outlineObserver.observe(heading));
    }
    markSection(state.section || ({explanation:'s1',examples:'s2',implementation:'s5'})[state.view]);
  }
  function render(initial=false) {
    const previous=state;
    const hasFileAnchor=location.hash.includes('.py');
    const restoreSourceFocus=document.activeElement?.id?.startsWith('source-')?document.activeElement.id:document.activeElement?.dataset?.sourceSide?'source-file-'+document.activeElement.dataset.sourceSide:null;
    state=parseHash();
    if(location.hash!==hash(state))history.replaceState(null,'',hash(state));
    const topic=topics.find(t=>t.id===state.topic);
    if(state.view==='implementation')sourceSelections.set(topic.id,{compare:state.compare,implementation:state.implementation,mode:state.mode,beforeFile:state.beforeFile,afterFile:state.afterFile});
    if(!initial&&previous?.topic===state.topic&&previous?.view===state.view&&previous?.step===state.step&&previous?.compare===state.compare&&previous?.implementation===state.implementation&&previous?.mode===state.mode){
      $('#permalink').href=hash(state);
      if(state.view==='implementation'){
        const pair=sourcePair(topic.guide,state);
        document.querySelectorAll('a[data-source-file]').forEach(link=>{
          link.href=sourceHref(pair,link.dataset.sourceSide,link.dataset.sourceFile);
        });
        $('#chapter-tab-implementation').href=hash(state);
        document.querySelectorAll('[data-section]').forEach(link=>{link.href=hash({...state,section:link.dataset.section});});
        if(previous.beforeFile!==state.beforeFile||previous.afterFile!==state.afterFile)focusSourceFile(previous);
      }
      focusSection();
      return;
    }
    document.title=`${topic.name} · Python — patterns`;
    $('#topic-meta').textContent=`${categories[topic.category]} · ${topic.ready?`${topic.minutes} минут`:'В плане курса'}`;
    $('#topic-title').textContent=`${topic.name} / ${topic.ru}`;
    $('#topic-subtitle').textContent=(state.view==='extension'?topic.extension.brief:topic.subtitle) || 'Материал этой темы готовится.';
    document.body.classList.toggle('comparison-active',Boolean(topic.ready));
    $('#permalink').href=hash(state);
    $('#lesson-body').innerHTML=topic.ready?guideLesson(topic):`<section class="panel planned-panel"><h2>${escape(topic.name)} — в плане курса</h2><p>Урок готовится. Начните с готовых тем:</p><div class="source-actions">${topics.filter(t=>t.ready).map(t=>`<a href="#${t.id}/theory">${t.name}</a>`).join('')}</div></section>`;
    if(topic.ready)$('#lesson-body').insertAdjacentHTML('beforeend',readingNavigation(topic));
    renderCatalog();
    renderOutline();
    $('.chapter-tabs')?.addEventListener('keydown',handleChapterTabKey);
    $('#source-compare')?.addEventListener('change',handleSourceComparisonChange);
    document.querySelectorAll('[name=source-implementation]').forEach(control=>control.addEventListener('change',handleSourceImplementationChange));
    document.querySelectorAll('[name=source-mode]').forEach(control=>control.addEventListener('change',handleSourceModeChange));
    document.querySelectorAll('a[data-source-file]').forEach(link=>link.addEventListener('click',event=>{
      if(event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
      const pair=sourcePair(topic.guide,state),side=link.dataset.sourceSide;
      const target=sourceHref(pair,side,link.dataset.sourceFile);
      event.preventDefault();
      if(target===location.hash)focusSourceFile(state,side);
      else location.hash=target;
    }));
    $('#source-diff')?.addEventListener('change',event=>{
      showSourceDiff=event.target.checked;
      render(true);
      $('#source-diff')?.focus({preventScroll:true});
    });
    document.querySelectorAll('[data-copy-file]').forEach(button=>button.addEventListener('click',async()=>{
      const block=button.closest('.code-window');
      const source=button.dataset.copySource?topic.guide.sources.find(file=>file.id===button.dataset.copySource):null;
      const text=source?source.code:block.querySelector('pre code').textContent;
      let copied=false;
      try{await navigator.clipboard.writeText(text);copied=true;}catch{
        const area=document.createElement('textarea');area.value=text;area.className='sr-only';document.body.append(area);area.select();
        try{copied=document.execCommand('copy');}catch{}finally{area.remove();button.focus();}
      }
      block.querySelector('.file-copy-status').textContent=copied?'Скопировано':block.querySelector('.source-diff')?'Отключите «Изменения», затем выделите и скопируйте код.':'Выделите и скопируйте показанный код.';
    }));
    if(!initial&&previous?.topic!==state.topic){closeCatalog();$('#topic-title').focus({preventScroll:true});window.scrollTo(0,0);}
    else if(!initial&&state.view==='implementation'&&previous?.view===state.view){(document.getElementById(restoreSourceFocus) || $('#source-compare'))?.focus({preventScroll:true});}
    else if(!initial&&previous?.step!==state.step){$('#lesson-body').scrollIntoView({block:'start'});$('#lesson-body').focus({preventScroll:true});}
    else if(!initial&&previous?.view!==state.view){$(`#chapter-tab-${state.view}`)?.focus({preventScroll:true});if(!state.section)$('.chapter-tabs')?.scrollIntoView({block:'start'});}
    const sourcePairChanged=!previous||previous.topic!==state.topic||previous.view!==state.view||
      previous.compare!==state.compare||previous.mode!==state.mode||previous.implementation!==state.implementation;
    if(hasFileAnchor&&sourcePairChanged&&state.view==='implementation')focusSourceFile(previous);
    focusSection();
  }
  $('#lesson-count').textContent=`${topics.length} тем`;
  $('.skip-link').addEventListener('click',event=>{event.preventDefault();$('#content').focus();$('#content').scrollIntoView({block:'start'});});
  $('#topic-search').addEventListener('input',renderCatalog);
  $('#catalog-toggle').addEventListener('click',()=>{const open=document.body.classList.toggle('catalog-open');$('#catalog-toggle').setAttribute('aria-expanded',String(open));$('.backdrop').hidden=!open;$('.workspace').inert=open;if(open)$('#topic-search').focus();});
  $('.backdrop').addEventListener('click',()=>closeCatalog(true));
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&document.body.classList.contains('catalog-open'))closeCatalog(true);});
  document.addEventListener('keydown',event=>{
    if(event.key!=='Tab'||!document.body.classList.contains('catalog-open'))return;
    const controls=[...$('#catalog').querySelectorAll('a, button, input')].filter(element=>!element.disabled);
    const first=controls[0],last=controls.at(-1);
    if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}
    else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}
  });
  window.matchMedia('(min-width: 960px)').addEventListener('change',event=>{if(event.matches)closeCatalog();});
  function setTheme(theme){document.documentElement.dataset.theme=theme;$('#theme-toggle').setAttribute('aria-pressed',String(theme==='dark'));$('#theme-toggle').textContent=theme==='dark'?'Verdandi Alter':'Verdandi';$('#theme-toggle').setAttribute('aria-label',theme==='dark'?'Тема Verdandi Alter. Включить светлую Verdandi':'Тема Verdandi. Включить тёмную Verdandi Alter');savePreference('theme',theme);}
  setTheme(preference('theme')==='dark'?'dark':'light');
  $('#theme-toggle').addEventListener('click',()=>setTheme(document.documentElement.dataset.theme==='dark'?'light':'dark'));
  window.addEventListener('hashchange',()=>{render();rememberPosition();});
  render(true);
  if (resume && Number.isFinite(savedPosition.y)) requestAnimationFrame(() => window.scrollTo(0, Math.max(0, savedPosition.y)));
})();
