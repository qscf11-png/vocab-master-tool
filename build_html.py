import json
import os

def build_html():
    data_path = "vocab_data.js"
    output_path = "index.html"
    
    if not os.path.exists(data_path):
        print("Error: data not found.")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        raw_js = f.read()
        json_str = raw_js.replace("const VOCAB_DB = ", "").strip()
        if json_str.endswith(";"):
            json_str = json_str[:-1]

    content = []
    content.append("""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>英語詞彙大師 Vocab Master</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"><\/script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"><\/script>
    <script src="https://cdn.tailwindcss.com"><\/script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Outfit', sans-serif; background: #f1f5f9; margin: 0; padding: 0; }
        .glass { background: rgba(255, 255, 255, 0.88); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.4); }
        .perspective-1000 { perspective: 1000px; }
        .transform-style-3d { transform-style: preserve-3d; }
        .backface-hidden { backface-visibility: hidden; }
        .rotate-y-180 { transform: rotateY(180deg); }
        .custom-scrollbar::-webkit-scrollbar { width: 4px; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
    </style>
</head>
<body>
    <div id="root"></div>
    <script id="vocab-data" type="application/json">""")
    
    content.append(json_str)
    
    content.append("""<\/script>

    <script type="text/javascript">
        (function() {
            var h = React.createElement;
            var useState = React.useState;
            var useEffect = React.useEffect;
            var useMemo = React.useMemo;
            var STORAGE_KEY = 'vocab_master_v2';
            
            var rawData = document.getElementById('vocab-data').textContent;
            var VOCAB_DB = JSON.parse(rawData);

            function shuffle(arr) {
                var n = arr.slice();
                for(var i = n.length - 1; i > 0; i--) {
                    var j = Math.floor(Math.random() * (i + 1));
                    var tmp = n[i]; n[i] = n[j]; n[j] = tmp;
                }
                return n;
            }

            function speak(text, rate) {
                window.speechSynthesis.cancel();
                var u = new SpeechSynthesisUtterance(text);
                u.lang = 'en-US';
                u.rate = rate || 1.0;
                window.speechSynthesis.speak(u);
            }

            function App() {
                var _vl = useState([]);
                var vocabList = _vl[0], setVocabList = _vl[1];

                var _ti = useState(0);
                var totalInitial = _ti[0], setTotalInitial = _ti[1];

                var _st = useState({ again: 0, hard: 0, good: 0, easy: 0 });
                var stats = _st[0], setStats = _st[1];

                var _fin = useState(false);
                var isFinished = _fin[0], setIsFinished = _fin[1];

                var _setup = useState(false);
                var isSettingUp = _setup[0], setIsSettingUp = _setup[1];

                var _flip = useState(false);
                var isFlipped = _flip[0], setIsFlipped = _flip[1];

                var _rate = useState(1.0);
                var speechRate = _rate[0], setSpeechRate = _rate[1];

                var _lev = useState([1,2,3,4,5,6]);
                var levels = _lev[0], setLevels = _lev[1];

                var _let = useState('All');
                var letter = _let[0], setLetter = _let[1];

                var _pos = useState('All');
                var posFilter = _pos[0], setPosFilter = _pos[1];

                var _cnt = useState(50);
                var count = _cnt[0], setCount = _cnt[1];

                // 中翻英模式
                var _mode = useState('en2zh');
                var quizMode = _mode[0], setQuizMode = _mode[1];

                var allPOS = useMemo(function() {
                    var s = new Set(['All']);
                    VOCAB_DB.forEach(function(x) { if(x.p) s.add(x.p.split('/')[0].trim()); });
                    return Array.from(s).sort();
                }, []);

                var filteredCount = useMemo(function() {
                    return VOCAB_DB.filter(function(x) {
                        var lOk = levels.indexOf(x.l) !== -1;
                        var aOk = letter === 'All' || x.w.toLowerCase().charAt(0) === letter.toLowerCase();
                        var pOk = posFilter === 'All' || (x.p && x.p.indexOf(posFilter) !== -1);
                        return lOk && aOk && pOk;
                    }).length;
                }, [levels, letter, posFilter]);

                function startQuiz() {
                    var f = VOCAB_DB.filter(function(x) {
                        var lOk = levels.indexOf(x.l) !== -1;
                        var aOk = letter === 'All' || x.w.toLowerCase().charAt(0) === letter.toLowerCase();
                        var pOk = posFilter === 'All' || (x.p && x.p.indexOf(posFilter) !== -1);
                        return lOk && aOk && pOk;
                    });
                    if(f.length === 0) { alert("沒有符合條件的單字"); return; }
                    var sampled = shuffle(f).slice(0, Math.min(count, f.length));
                    setVocabList(sampled);
                    setTotalInitial(sampled.length);
                    setStats({ again: 0, hard: 0, good: 0, easy: 0 });
                    setIsSettingUp(false);
                    setIsFinished(false);
                    setIsFlipped(false);
                }

                function resetAll() {
                    if(confirm("確定要重新開始嗎？")) {
                        setVocabList([]);
                        setIsSettingUp(false);
                        setIsFinished(false);
                        setIsFlipped(false);
                    }
                }

                function handleSRS(type) {
                    setStats(function(s) {
                        var n = {}; for(var k in s) n[k] = s[k];
                        n[type] = n[type] + 1;
                        return n;
                    });
                    var rest = vocabList.slice(1);
                    var curr = vocabList[0];
                    var next;
                    if(type === 'again') next = rest.length > 0 ? [rest[0], curr].concat(rest.slice(1)) : [curr];
                    else if(type === 'hard') next = rest.length >= 4 ? rest.slice(0,4).concat([curr]).concat(rest.slice(4)) : rest.concat([curr]);
                    else if(type === 'good') next = rest.concat([curr]);
                    else next = rest;

                    if(next.length === 0) setIsFinished(true);
                    setVocabList(next);
                    setIsFlipped(false);
                }

                // ==================== 首頁 ====================
                if(vocabList.length === 0 && !isSettingUp && !isFinished) {
                    return h('div', { className: "flex flex-col items-center justify-center min-h-screen p-6" },
                        h('div', { className: "glass max-w-sm w-full rounded-[40px] shadow-2xl p-10 text-center" },
                            h('div', { className: "w-20 h-20 bg-indigo-600 rounded-3xl flex items-center justify-center mx-auto mb-8 shadow-xl text-white text-3xl" }, "V"),
                            h('h1', { className: "text-3xl font-black text-slate-800 mb-2" }, "Vocab Master"),
                            h('p', { className: "text-slate-400 mb-10 text-xs font-bold uppercase tracking-widest" }, VOCAB_DB.length + " Words Database"),
                            h('button', { onClick: function() { setIsSettingUp(true); }, className: "w-full py-5 bg-indigo-600 text-white rounded-3xl font-black shadow-lg hover:bg-indigo-700 transition-all" }, "進入設定")
                        )
                    );
                }

                // ==================== 設定頁面 ====================
                if(isSettingUp) {
                    return h('div', { className: "flex flex-col items-center justify-center min-h-screen p-4" },
                        h('div', { className: "glass max-w-md w-full rounded-[32px] shadow-2xl p-8" },
                            h('h2', { className: "text-xl font-black text-slate-800 mb-6 text-center" }, "抽籤篩選器"),
                            h('div', { className: "space-y-5" },
                                // 測驗模式
                                h('div', null,
                                    h('label', { className: "text-[10px] font-black text-slate-400 uppercase block mb-2" }, "測驗模式"),
                                    h('div', { className: "flex gap-2" },
                                        h('button', { onClick: function() { setQuizMode('en2zh'); }, className: "flex-1 py-2 rounded-xl text-xs font-bold border-2 transition-all " + (quizMode === 'en2zh' ? 'bg-indigo-600 border-indigo-600 text-white' : 'border-slate-100 text-slate-400') }, "英翻中"),
                                        h('button', { onClick: function() { setQuizMode('zh2en'); }, className: "flex-1 py-2 rounded-xl text-xs font-bold border-2 transition-all " + (quizMode === 'zh2en' ? 'bg-emerald-600 border-emerald-600 text-white' : 'border-slate-100 text-slate-400') }, "中翻英")
                                    )
                                ),
                                // Level
                                h('div', null,
                                    h('label', { className: "text-[10px] font-black text-slate-400 uppercase block mb-2" }, "Level 範圍"),
                                    h('div', { className: "flex flex-wrap gap-2" },
                                        [1,2,3,4,5,6].map(function(l) { return h('button', {
                                            key: l,
                                            onClick: function() { levels.indexOf(l) !== -1 ? setLevels(levels.filter(function(x){return x!==l;})) : setLevels(levels.concat([l])); },
                                            className: "px-3 py-1.5 rounded-lg text-xs font-bold border-2 transition-all " + (levels.indexOf(l) !== -1 ? 'bg-indigo-600 border-indigo-600 text-white' : 'border-slate-100 text-slate-400')
                                        }, "L" + l); })
                                    )
                                ),
                                // 首字母 + 詞性
                                h('div', { className: "grid grid-cols-2 gap-4" },
                                    h('div', null,
                                        h('label', { className: "text-[10px] font-black text-slate-400 uppercase block mb-2" }, "首字母 (A-Z)"),
                                        h('select', { value: letter, onChange: function(ev) { setLetter(ev.target.value); }, className: "w-full bg-slate-50 rounded-xl p-2 text-sm border-none ring-1 ring-slate-200" },
                                            ['All'].concat('abcdefghijklmnopqrstuvwxyz'.split('')).map(function(c) { return h('option', { key: c, value: c }, c.toUpperCase()); })
                                        )
                                    ),
                                    h('div', null,
                                        h('label', { className: "text-[10px] font-black text-slate-400 uppercase block mb-2" }, "詞性篩選"),
                                        h('select', { value: posFilter, onChange: function(ev) { setPosFilter(ev.target.value); }, className: "w-full bg-slate-50 rounded-xl p-2 text-sm border-none ring-1 ring-slate-200" },
                                            allPOS.map(function(p) { return h('option', { key: p, value: p }, p); })
                                        )
                                    )
                                ),
                                // 數量
                                h('div', null,
                                    h('div', { className: "flex justify-between mb-2" },
                                        h('label', { className: "text-[10px] font-black text-slate-400 uppercase" }, "抽樣數量"),
                                        h('span', { className: "text-sm font-black text-indigo-600" }, count)
                                    ),
                                    h('input', { type: 'range', min: '5', max: Math.min(filteredCount, 200), value: count, onChange: function(ev) { setCount(parseInt(ev.target.value)); }, className: "w-full h-2 bg-slate-100 rounded-lg appearance-none accent-indigo-600" })
                                ),
                                // 符合條件數
                                h('div', { className: "p-3 bg-indigo-50 rounded-2xl border border-indigo-100 flex justify-between items-center" },
                                    h('span', { className: "text-xs font-bold text-indigo-400" }, "符合條件"),
                                    h('span', { className: "text-xl font-black text-indigo-600" }, filteredCount)
                                ),
                                h('button', { onClick: startQuiz, className: "w-full py-4 bg-slate-800 text-white rounded-2xl font-black shadow-xl hover:bg-slate-900 transition-all" }, "開始學習"),
                                h('button', { onClick: function() { setIsSettingUp(false); }, className: "w-full text-xs font-bold text-slate-400 py-2" }, "取消")
                            )
                        )
                    );
                }

                // ==================== 完成頁 ====================
                if(isFinished) {
                    return h('div', { className: "flex flex-col items-center justify-center min-h-screen p-6" },
                        h('div', { className: "glass max-w-sm w-full rounded-[40px] shadow-2xl p-10 text-center" },
                            h('div', { className: "text-6xl mb-4" }, "🏆"),
                            h('h2', { className: "text-2xl font-black text-slate-800 mb-4" }, "測試完成！"),
                            h('div', { className: "grid grid-cols-2 gap-2 my-6" },
                                h('div', { className: "bg-red-50 p-3 rounded-2xl" }, h('p', { className: "text-[8px] font-black text-red-400 uppercase" }, "Again"), h('p', { className: "text-xl font-black text-red-600" }, stats.again)),
                                h('div', { className: "bg-orange-50 p-3 rounded-2xl" }, h('p', { className: "text-[8px] font-black text-orange-400 uppercase" }, "Hard"), h('p', { className: "text-xl font-black text-orange-600" }, stats.hard)),
                                h('div', { className: "bg-blue-50 p-3 rounded-2xl" }, h('p', { className: "text-[8px] font-black text-blue-400 uppercase" }, "Good"), h('p', { className: "text-xl font-black text-blue-600" }, stats.good)),
                                h('div', { className: "bg-green-50 p-3 rounded-2xl" }, h('p', { className: "text-[8px] font-black text-green-400 uppercase" }, "Easy"), h('p', { className: "text-xl font-black text-green-600" }, stats.easy))
                            ),
                            h('button', { onClick: function() { setVocabList([]); setIsFinished(false); setIsSettingUp(false); }, className: "w-full py-4 bg-indigo-600 text-white rounded-2xl font-black shadow-lg" }, "新學習")
                        )
                    );
                }

                // ==================== 學習卡片頁 ====================
                var current = vocabList[0];
                var progress = ((totalInitial - vocabList.length) / totalInitial) * 100;
                var isCn2En = quizMode === 'zh2en';

                // 正面內容（提問）
                var frontContent;
                if(isCn2En) {
                    // 中翻英：正面顯示中文定義
                    frontContent = h('div', { className: "absolute inset-0 backface-hidden bg-white rounded-[40px] shadow-2xl p-8 flex flex-col items-center justify-center border-8 border-white" },
                        h('div', { className: "absolute top-4 left-4 px-2 py-1 bg-emerald-100 text-emerald-600 text-[9px] font-black rounded" }, "中翻英"),
                        h('div', { className: "absolute top-4 right-4 flex gap-2" },
                            h('span', { className: "px-2 py-1 bg-indigo-100 text-indigo-600 text-[9px] font-black rounded" }, "L" + current.l),
                            h('span', { className: "px-2 py-1 bg-slate-100 text-slate-500 text-[9px] font-black rounded" }, current.p || "")
                        ),
                        h('p', { className: "text-sm font-bold text-slate-400 mb-4 uppercase tracking-widest" }, "這個英文單字是？"),
                        h('h2', { className: "text-3xl font-black text-slate-800 text-center mb-4" }, current.d),
                        current.c && h('p', { className: "text-sm text-indigo-400 font-bold" }, "搭配提示：" + current.c),
                        h('p', { className: "mt-8 text-[10px] font-black text-slate-300 uppercase tracking-[0.4em] animate-pulse" }, "點擊翻牌查看答案")
                    );
                } else {
                    // 英翻中：正面顯示英文單字
                    frontContent = h('div', { className: "absolute inset-0 backface-hidden bg-white rounded-[40px] shadow-2xl p-8 flex flex-col items-center justify-center border-8 border-white" },
                        h('button', { onClick: function(ev) { ev.stopPropagation(); speak(current.w, speechRate); }, className: "absolute top-6 right-6 p-2 bg-indigo-50 text-indigo-600 rounded-full text-xl" }, "🔊"),
                        h('div', { className: "absolute top-4 left-4 flex gap-2" },
                            h('span', { className: "px-2 py-1 bg-indigo-100 text-indigo-600 text-[9px] font-black rounded" }, "L" + current.l),
                            h('span', { className: "px-2 py-1 bg-slate-100 text-slate-500 text-[9px] font-black rounded" }, current.p || "")
                        ),
                        h('h2', { className: "text-4xl font-black text-slate-800 text-center mb-2" }, current.w),
                        current.i && h('p', { className: "text-sm text-slate-400 font-mono" }, current.i),
                        h('p', { className: "mt-8 text-[10px] font-black text-slate-300 uppercase tracking-[0.4em] animate-pulse" }, "點擊翻牌查看釋義")
                    );
                }

                // 背面內容（答案與完整資訊）
                var backContent = h('div', { className: "absolute inset-0 backface-hidden bg-white rounded-[40px] shadow-2xl p-6 flex flex-col rotate-y-180 border-8 border-white overflow-hidden" },
                    // 標題列
                    h('div', { className: "flex justify-between items-center mb-3 shrink-0" },
                        h('div', { className: "flex gap-2 items-center" },
                            h('span', { className: "px-2 py-0.5 bg-indigo-600 text-white text-[9px] font-black rounded" }, "L" + current.l),
                            h('span', { className: "px-2 py-0.5 bg-slate-100 text-slate-500 text-[9px] font-black rounded" }, current.p || "")
                        ),
                        h('button', { onClick: function(ev) { ev.stopPropagation(); speak(current.w, speechRate); }, className: "p-2 bg-indigo-50 text-indigo-600 rounded-full text-lg" }, "🔊")
                    ),
                    // 單字與音標
                    h('h2', { className: "text-2xl font-black text-indigo-600 mb-1 shrink-0" }, current.w),
                    current.i && h('p', { className: "text-xs text-slate-400 font-mono mb-3 shrink-0" }, current.i),
                    // 詳細內容（可捲動）
                    h('div', { className: "flex-grow overflow-y-auto custom-scrollbar pr-1 space-y-3" },
                        // 解釋
                        h('div', { className: "bg-indigo-50/50 rounded-xl p-3" },
                            h('p', { className: "text-[10px] font-black text-indigo-400 uppercase mb-1" }, "解釋"),
                            h('p', { className: "text-[15px] font-bold text-slate-800" }, current.d)
                        ),
                        // 搭配字
                        current.c && h('div', { className: "bg-amber-50/50 rounded-xl p-3" },
                            h('p', { className: "text-[10px] font-black text-amber-500 uppercase mb-1" }, "搭配字 Collocations"),
                            h('p', { className: "text-[13px] font-bold text-slate-700" }, current.c)
                        ),
                        // 例句
                        current.x && h('div', { className: "bg-blue-50/50 rounded-xl p-3" },
                            h('p', { className: "text-[10px] font-black text-blue-400 uppercase mb-1" }, "例句 Example"),
                            h('p', { className: "text-[13px] text-slate-700 italic" }, current.x)
                        ),
                        // 衍生詞
                        current.t && h('div', { className: "bg-emerald-50/50 rounded-xl p-3" },
                            h('p', { className: "text-[10px] font-black text-emerald-400 uppercase mb-1" }, "衍生詞 Related"),
                            h('p', { className: "text-[13px] text-slate-600" }, current.t)
                        )
                    ),
                    // SRS 按鈕
                    h('div', { className: "grid grid-cols-4 gap-2 mt-3 shrink-0" },
                        h('button', { onClick: function(ev) { ev.stopPropagation(); handleSRS('again'); }, className: "py-3 bg-red-50 text-red-600 rounded-2xl text-[9px] font-black hover:bg-red-100 transition-all" }, "AGAIN"),
                        h('button', { onClick: function(ev) { ev.stopPropagation(); handleSRS('hard'); }, className: "py-3 bg-orange-50 text-orange-600 rounded-2xl text-[9px] font-black hover:bg-orange-100 transition-all" }, "HARD"),
                        h('button', { onClick: function(ev) { ev.stopPropagation(); handleSRS('good'); }, className: "py-3 bg-blue-50 text-blue-600 rounded-2xl text-[9px] font-black hover:bg-blue-100 transition-all" }, "GOOD"),
                        h('button', { onClick: function(ev) { ev.stopPropagation(); handleSRS('easy'); }, className: "py-3 bg-green-50 text-green-600 rounded-2xl text-[9px] font-black hover:bg-green-100 transition-all" }, "EASY")
                    )
                );

                return h('div', { className: "flex flex-col items-center min-h-screen p-4 overflow-hidden" },
                    // 進度條
                    h('div', { className: "w-full max-w-md glass rounded-2xl shadow-lg p-4 mb-4 flex flex-col gap-3" },
                        h('div', { className: "flex justify-between items-center text-[10px] font-black text-slate-400" },
                            h('div', { className: "flex gap-1" },
                                h('span', { className: "text-red-500 bg-red-50 px-1.5 rounded" }, stats.again),
                                h('span', { className: "text-orange-500 bg-orange-50 px-1.5 rounded" }, stats.hard),
                                h('span', { className: "text-blue-500 bg-blue-50 px-1.5 rounded" }, stats.good),
                                h('span', { className: "text-green-500 bg-green-50 px-1.5 rounded" }, stats.easy)
                            ),
                            h('span', { className: "font-bold" }, vocabList.length + " / " + totalInitial),
                            h('button', { onClick: resetAll, className: "hover:text-red-500 text-lg" }, "↺")
                        ),
                        h('div', { className: "w-full h-1.5 bg-slate-100 rounded-full overflow-hidden" },
                            h('div', { className: "bg-indigo-500 h-full transition-all", style: { width: progress + "%" } })
                        )
                    ),
                    // 翻牌卡
                    h('div', { className: "w-full max-w-md flex-grow relative perspective-1000 mb-4" },
                        h('div', { 
                            onClick: function() { setIsFlipped(!isFlipped); },
                            className: "relative w-full h-full transition-all duration-700 transform-style-3d cursor-pointer " + (isFlipped ? 'rotate-y-180' : '')
                        },
                            frontContent,
                            backContent
                        )
                    ),
                    // 語速調整
                    h('div', { className: "w-full max-w-md flex items-center gap-4 py-2 shrink-0" },
                        h('span', { className: "text-sm" }, "🔈"),
                        h('input', { type: 'range', min: '0.5', max: '2.0', step: '0.1', value: speechRate, onChange: function(ev) { setSpeechRate(parseFloat(ev.target.value)); }, className: "flex-grow h-1 bg-white rounded-full appearance-none accent-indigo-600" }),
                        h('span', { className: "text-[10px] font-black text-indigo-600" }, speechRate.toFixed(1) + "x")
                    )
                );
            }
            
            var root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(h(App));
        })();
    <\/script>
</body>
</html>""")

    with open(output_path, "w", encoding="utf-8") as f:
        # 將 <\/script> 轉回正常的 </script>
        final = "".join(content).replace("<\\/script>", "</script>")
        f.write(final)
    
    print(f"Vocab Master Tool Build (Feature Complete) Success. Words: {len(json.loads(json_str))}")

if __name__ == "__main__":
    build_html()
