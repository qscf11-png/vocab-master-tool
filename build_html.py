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
    content.append(r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>英語詞彙大師 Vocab Master</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Outfit', sans-serif; background: linear-gradient(135deg, #e0e7ff 0%, #f1f5f9 50%, #dbeafe 100%); margin: 0; padding: 0; min-height: 100vh; }
        .glass { background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.5); }
        .custom-scrollbar::-webkit-scrollbar { width: 4px; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
        .info-block { border-left: 4px solid; padding: 8px 12px; border-radius: 0 8px 8px 0; margin-bottom: 8px; }
        .letter-input {
            width: 32px; height: 40px; text-align: center; font-size: 20px; font-weight: 900;
            border: 2px solid #cbd5e1; border-radius: 8px; outline: none; text-transform: lowercase;
            transition: all 0.2s; font-family: 'Outfit', monospace;
        }
        .letter-input:focus { border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.15); }
        .letter-correct { border-color: #10b981 !important; background: #ecfdf5 !important; color: #059669 !important; }
        .letter-wrong { border-color: #ef4444 !important; background: #fef2f2 !important; color: #dc2626 !important; }
        .letter-fixed { background: #f1f5f9; color: #334155; font-weight: 900; border-color: #94a3b8; }
        .letter-space { width: 16px; height: 40px; border: none; background: transparent; }
    </style>
</head>
<body>
    <div id="root"></div>
    <script id="vocab-data" type="application/json">""")
    
    content.append(json_str)
    
    content.append(r"""</script>

    <script type="text/javascript">
        (function() {
            var h = React.createElement;
            var useState = React.useState;
            var useEffect = React.useEffect;
            var useMemo = React.useMemo;
            var useRef = React.useRef;
            var useCallback = React.useCallback;
            
            var rawData = document.getElementById('vocab-data').textContent;
            var BUILTIN_DB = JSON.parse(rawData);

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

            // Excel 解析函式
            function parseExcel(file, callback) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    try {
                        var data = new Uint8Array(e.target.result);
                        var wb = XLSX.read(data, { type: 'array' });
                        var ws = wb.Sheets[wb.SheetNames[0]];
                        var rows = XLSX.utils.sheet_to_json(ws);
                        var vocab = [];
                        rows.forEach(function(r) {
                            var w = r.word || r.Word || r.WORD || r['單字'] || '';
                            var d = r.definition || r.Definition || r.DEFINITION || r['解釋'] || r['定義'] || '';
                            if(w && d) {
                                vocab.push({
                                    w: String(w).trim(),
                                    d: String(d).trim(),
                                    i: String(r.pronunciation || r.Pronunciation || r['音標'] || '').trim(),
                                    t: String(r.related || r.Related || r['衍生詞'] || '').trim(),
                                    c: String(r.collocations || r.Collocations || r['搭配字'] || '').trim(),
                                    x: String(r.example || r.Example || r['例句'] || '').trim(),
                                    p: String(r.pos || r.POS || r['詞性'] || '').trim(),
                                    l: parseInt(r.level || r.Level || r['等級'] || 1) || 1
                                });
                            }
                        });
                        callback(null, vocab);
                    } catch(err) {
                        callback(err, null);
                    }
                };
                reader.readAsArrayBuffer(file);
            }

            // ==================== 字母填空元件 ====================
            function LetterInputRow(props) {
                var word = props.word;
                var onComplete = props.onComplete;
                var inputsRef = useRef([]);
                
                // 將單字拆成字元陣列，標記哪些是可輸入的
                var chars = word.toLowerCase().split('');
                var slots = chars.map(function(ch, idx) {
                    if(ch === ' ') return { type: 'space', char: ' ', idx: idx };
                    if(idx === 0 || idx === chars.length - 1) return { type: 'fixed', char: ch, idx: idx };
                    // 片語中每個單詞的首尾也固定
                    if(idx > 0 && chars[idx-1] === ' ') return { type: 'fixed', char: ch, idx: idx };
                    if(idx < chars.length - 1 && chars[idx+1] === ' ') return { type: 'fixed', char: ch, idx: idx };
                    return { type: 'input', char: ch, idx: idx };
                });
                
                var inputCount = slots.filter(function(s) { return s.type === 'input'; }).length;
                var _vals = useState(function() { return new Array(chars.length).fill(''); });
                var values = _vals[0], setValues = _vals[1];
                var _submitted = useState(false);
                var submitted = _submitted[0], setSubmitted = _submitted[1];

                function handleChange(slotIdx, val) {
                    if(submitted) return;
                    var ch = val.slice(-1).toLowerCase();
                    if(!/^[a-z]$/.test(ch) && ch !== '') return;
                    var nv = values.slice();
                    nv[slotIdx] = ch;
                    setValues(nv);
                    
                    // 自動跳到下一個 input
                    if(ch !== '') {
                        var nextInputs = slots.filter(function(s, i) { return s.type === 'input' && i > slotIdx; });
                        if(nextInputs.length > 0) {
                            var nextIdx = nextInputs[0].idx;
                            setTimeout(function() {
                                if(inputsRef.current[nextIdx]) inputsRef.current[nextIdx].focus();
                            }, 30);
                        }
                    }
                }

                function handleKeyDown(slotIdx, e) {
                    if(submitted) return;
                    if(e.key === 'Backspace' && values[slotIdx] === '') {
                        // 回到上一個 input
                        var prevInputs = slots.filter(function(s, i) { return s.type === 'input' && i < slotIdx; });
                        if(prevInputs.length > 0) {
                            var prevIdx = prevInputs[prevInputs.length-1].idx;
                            setTimeout(function() {
                                if(inputsRef.current[prevIdx]) inputsRef.current[prevIdx].focus();
                            }, 30);
                        }
                    }
                    if(e.key === 'Enter') {
                        doSubmit();
                    }
                }

                function doSubmit() {
                    setSubmitted(true);
                    var allCorrect = slots.every(function(s) {
                        if(s.type !== 'input') return true;
                        return values[s.idx] === s.char;
                    });
                    if(onComplete) onComplete(allCorrect);
                }

                function getInputClass(slot) {
                    if(!submitted) return 'letter-input';
                    if(values[slot.idx] === slot.char) return 'letter-input letter-correct';
                    return 'letter-input letter-wrong';
                }

                // 建立顯示元素
                var elements = slots.map(function(slot) {
                    if(slot.type === 'space') {
                        return h('div', { key: 's' + slot.idx, className: 'letter-space' });
                    }
                    if(slot.type === 'fixed') {
                        return h('div', { key: 'f' + slot.idx, className: 'letter-input letter-fixed flex items-center justify-center', style: { cursor: 'default' } }, slot.char.toUpperCase());
                    }
                    // input type
                    return h('input', {
                        key: 'i' + slot.idx,
                        ref: function(el) { inputsRef.current[slot.idx] = el; },
                        type: 'text',
                        maxLength: 1,
                        value: submitted ? (values[slot.idx] || '_') : (values[slot.idx] || ''),
                        onChange: function(e) { handleChange(slot.idx, e.target.value); },
                        onKeyDown: function(e) { handleKeyDown(slot.idx, e); },
                        className: getInputClass(slot),
                        disabled: submitted,
                        autoComplete: 'off'
                    });
                });

                return h('div', { className: 'flex flex-col items-center gap-4' },
                    h('div', { className: 'flex flex-wrap justify-center gap-1' }, elements),
                    !submitted && h('button', {
                        onClick: doSubmit,
                        className: 'px-8 py-2.5 bg-emerald-600 text-white rounded-xl font-black text-sm hover:bg-emerald-700 transition-all shadow-lg'
                    }, '送出答案'),
                    submitted && h('div', { className: 'text-center' },
                        h('p', { className: 'text-lg font-black mb-2 ' + (slots.every(function(s) { return s.type !== 'input' || values[s.idx] === s.char; }) ? 'text-emerald-600' : 'text-red-600') },
                            slots.every(function(s) { return s.type !== 'input' || values[s.idx] === s.char; }) ? '✅ 正確！' : '❌ 正確答案：' + word
                        )
                    )
                );
            }

            // ==================== 主應用 ====================
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
                var _mode = useState('en2zh');
                var quizMode = _mode[0], setQuizMode = _mode[1];
                // 自訂字庫（臨時）
                var _customDB = useState(null);
                var customDB = _customDB[0], setCustomDB = _customDB[1];
                var _dataSource = useState('builtin');
                var dataSource = _dataSource[0], setDataSource = _dataSource[1];
                // 中翻英填空後是否已送出
                var _zh2enSubmitted = useState(false);
                var zh2enSubmitted = _zh2enSubmitted[0], setZh2enSubmitted = _zh2enSubmitted[1];

                // 當前使用的資料庫
                var activeDB = (dataSource === 'custom' && customDB) ? customDB : BUILTIN_DB;

                var allPOS = useMemo(function() {
                    var s = new Set(['All']);
                    activeDB.forEach(function(x) { if(x.p) s.add(x.p.split('/')[0].trim()); });
                    return Array.from(s).sort();
                }, [activeDB]);

                var filteredCount = useMemo(function() {
                    return activeDB.filter(function(x) {
                        return (levels.indexOf(x.l) !== -1) &&
                               (letter === 'All' || x.w.toLowerCase().charAt(0) === letter.toLowerCase()) &&
                               (posFilter === 'All' || (x.p && x.p.indexOf(posFilter) !== -1));
                    }).length;
                }, [activeDB, levels, letter, posFilter]);

                function handleFileUpload(ev) {
                    var file = ev.target.files[0];
                    if(!file) return;
                    parseExcel(file, function(err, vocab) {
                        if(err) { alert('Excel 解析失敗：' + err.message); return; }
                        if(vocab.length === 0) { alert('找不到有效的單字資料。請確認欄位名稱（word, definition）'); return; }
                        setCustomDB(vocab);
                        setDataSource('custom');
                        alert('成功匯入 ' + vocab.length + ' 個單字！（臨時使用，重新整理後消失）');
                    });
                    ev.target.value = '';
                }

                function startQuiz() {
                    var f = activeDB.filter(function(x) {
                        return (levels.indexOf(x.l) !== -1) &&
                               (letter === 'All' || x.w.toLowerCase().charAt(0) === letter.toLowerCase()) &&
                               (posFilter === 'All' || (x.p && x.p.indexOf(posFilter) !== -1));
                    });
                    if(f.length === 0) { alert("沒有符合條件的單字"); return; }
                    var sampled = shuffle(f).slice(0, Math.min(count, f.length));
                    setVocabList(sampled);
                    setTotalInitial(sampled.length);
                    setStats({ again: 0, hard: 0, good: 0, easy: 0 });
                    setIsSettingUp(false);
                    setIsFinished(false);
                    setIsFlipped(false);
                    setZh2enSubmitted(false);
                }

                function resetAll() {
                    if(confirm("確定要重新開始嗎？")) {
                        setVocabList([]);
                        setIsSettingUp(false);
                        setIsFinished(false);
                        setIsFlipped(false);
                        setZh2enSubmitted(false);
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
                    setZh2enSubmitted(false);
                }

                // ==================== 自動朗讀 ====================
                // 英翻中正面出現時自動朗讀單字
                useEffect(function() {
                    if(vocabList.length > 0 && !isFlipped && !isSettingUp && !isFinished && quizMode === 'en2zh') {
                        setTimeout(function() { speak(vocabList[0].w, speechRate); }, 300);
                    }
                }, [vocabList.length > 0 && vocabList[0] && vocabList[0].w, isFlipped, quizMode]);

                // 翻面後自動朗讀例句
                useEffect(function() {
                    if(vocabList.length > 0 && isFlipped && !isFinished) {
                        var curr = vocabList[0];
                        if(curr.x) {
                            setTimeout(function() { speak(curr.x, speechRate); }, 300);
                        }
                    }
                }, [isFlipped]);

                // ==================== 鍵盤快速鍵 ====================
                useEffect(function() {
                    function handleKey(e) {
                        // 如果正在輸入框打字（中翻英填空），不攔截
                        if(e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;
                        // 只在卡片頁面有效
                        if(vocabList.length === 0 || isSettingUp || isFinished) return;

                        if(e.key === ' ' || e.code === 'Space') {
                            e.preventDefault();
                            if(!isFlipped) setIsFlipped(true);
                        }
                        if(isFlipped) {
                            if(e.key === '1') { e.preventDefault(); handleSRS('again'); }
                            if(e.key === '2') { e.preventDefault(); handleSRS('hard'); }
                            if(e.key === '3') { e.preventDefault(); handleSRS('good'); }
                            if(e.key === '4') { e.preventDefault(); handleSRS('easy'); }
                        }
                    }
                    window.addEventListener('keydown', handleKey);
                    return function() { window.removeEventListener('keydown', handleKey); };
                });

                // ==================== 首頁 ====================
                if(vocabList.length === 0 && !isSettingUp && !isFinished) {
                    return h('div', { className: "flex flex-col items-center justify-center min-h-screen p-6" },
                        h('div', { className: "glass max-w-sm w-full rounded-3xl shadow-2xl p-10 text-center" },
                            h('div', { className: "w-20 h-20 bg-indigo-600 rounded-3xl flex items-center justify-center mx-auto mb-8 shadow-xl text-white text-3xl font-black" }, "V"),
                            h('h1', { className: "text-3xl font-black text-slate-800 mb-2" }, "Vocab Master"),
                            h('p', { className: "text-slate-400 mb-6 text-xs font-bold uppercase tracking-widest" },
                                (dataSource === 'custom' && customDB) ? (customDB.length + " Custom Words") : (BUILTIN_DB.length + " Words")
                            ),
                            // 資料來源切換
                            customDB && h('div', { className: "flex gap-2 mb-6" },
                                h('button', { onClick: function() { setDataSource('builtin'); }, className: "flex-1 py-2 rounded-xl text-xs font-bold border-2 transition-all " + (dataSource === 'builtin' ? 'bg-indigo-600 border-indigo-600 text-white' : 'border-slate-200 text-slate-400') }, "內建字庫"),
                                h('button', { onClick: function() { setDataSource('custom'); }, className: "flex-1 py-2 rounded-xl text-xs font-bold border-2 transition-all " + (dataSource === 'custom' ? 'bg-amber-500 border-amber-500 text-white' : 'border-slate-200 text-slate-400') }, "自訂字庫")
                            ),
                            h('button', { onClick: function() { setIsSettingUp(true); }, className: "w-full py-5 bg-indigo-600 text-white rounded-2xl font-black text-lg shadow-lg hover:bg-indigo-700 transition-all mb-3" }, "進入設定"),
                            // Excel 匯入
                            h('label', { className: "w-full py-3 bg-white border-2 border-dashed border-slate-200 text-slate-500 rounded-2xl font-bold text-sm cursor-pointer hover:border-indigo-400 hover:text-indigo-500 transition-all flex items-center justify-center gap-2" },
                                h('span', null, "\uD83D\uDCC1 匯入 Excel 字庫"),
                                h('input', { type: 'file', accept: '.xlsx,.xls', onChange: handleFileUpload, className: "hidden" })
                            ),
                            h('p', { className: "text-[9px] text-slate-300 mt-3" }, "Excel 欄位：word, definition, pronunciation, related, collocations, example, pos, level")
                        )
                    );
                }

                // ==================== 設定頁面 ====================
                if(isSettingUp) {
                    return h('div', { className: "flex flex-col items-center justify-center min-h-screen p-4" },
                        h('div', { className: "glass max-w-md w-full rounded-3xl shadow-2xl p-8" },
                            h('h2', { className: "text-xl font-black text-slate-800 mb-6 text-center" }, "抽籤篩選器"),
                            (dataSource === 'custom' && customDB) && h('div', { className: "p-3 bg-amber-50 rounded-2xl border border-amber-200 text-center mb-4" },
                                h('span', { className: "text-xs font-bold text-amber-600" }, "\uD83D\uDCC1 使用自訂字庫 (" + customDB.length + " 字)")
                            ),
                            h('div', { className: "space-y-5" },
                                // 測驗模式
                                h('div', null,
                                    h('label', { className: "text-[10px] font-black text-slate-400 uppercase block mb-2" }, "測驗模式"),
                                    h('div', { className: "flex gap-2" },
                                        h('button', { onClick: function() { setQuizMode('en2zh'); }, className: "flex-1 py-2.5 rounded-xl text-sm font-bold border-2 transition-all " + (quizMode === 'en2zh' ? 'bg-indigo-600 border-indigo-600 text-white' : 'border-slate-200 text-slate-400') }, "英翻中"),
                                        h('button', { onClick: function() { setQuizMode('zh2en'); }, className: "flex-1 py-2.5 rounded-xl text-sm font-bold border-2 transition-all " + (quizMode === 'zh2en' ? 'bg-emerald-600 border-emerald-600 text-white' : 'border-slate-200 text-slate-400') }, "中翻英 (填空)")
                                    )
                                ),
                                // Level
                                h('div', null,
                                    h('label', { className: "text-[10px] font-black text-slate-400 uppercase block mb-2" }, "Level 範圍"),
                                    h('div', { className: "flex flex-wrap gap-2" },
                                        [1,2,3,4,5,6].map(function(l) { return h('button', {
                                            key: l,
                                            onClick: function() { levels.indexOf(l) !== -1 ? setLevels(levels.filter(function(x){return x!==l;})) : setLevels(levels.concat([l])); },
                                            className: "px-4 py-2 rounded-lg text-sm font-bold border-2 transition-all " + (levels.indexOf(l) !== -1 ? 'bg-indigo-600 border-indigo-600 text-white' : 'border-slate-200 text-slate-400')
                                        }, "L" + l); })
                                    )
                                ),
                                h('div', { className: "grid grid-cols-2 gap-4" },
                                    h('div', null,
                                        h('label', { className: "text-[10px] font-black text-slate-400 uppercase block mb-2" }, "首字母"),
                                        h('select', { value: letter, onChange: function(ev) { setLetter(ev.target.value); }, className: "w-full bg-white rounded-xl p-2.5 text-sm border ring-0 border-slate-200" },
                                            ['All'].concat('abcdefghijklmnopqrstuvwxyz'.split('')).map(function(c) { return h('option', { key: c, value: c }, c.toUpperCase()); })
                                        )
                                    ),
                                    h('div', null,
                                        h('label', { className: "text-[10px] font-black text-slate-400 uppercase block mb-2" }, "詞性篩選"),
                                        h('select', { value: posFilter, onChange: function(ev) { setPosFilter(ev.target.value); }, className: "w-full bg-white rounded-xl p-2.5 text-sm border ring-0 border-slate-200" },
                                            allPOS.map(function(p) { return h('option', { key: p, value: p }, p); })
                                        )
                                    )
                                ),
                                h('div', null,
                                    h('div', { className: "flex justify-between mb-2" },
                                        h('label', { className: "text-[10px] font-black text-slate-400 uppercase" }, "抽樣數量"),
                                        h('span', { className: "text-lg font-black text-indigo-600" }, count)
                                    ),
                                    h('input', { type: 'range', min: '5', max: Math.min(filteredCount || 200, 200), value: count, onChange: function(ev) { setCount(parseInt(ev.target.value)); }, className: "w-full h-2 bg-slate-200 rounded-lg appearance-none accent-indigo-600" })
                                ),
                                h('div', { className: "p-4 bg-indigo-50 rounded-2xl border border-indigo-100 flex justify-between items-center" },
                                    h('span', { className: "text-sm font-bold text-indigo-400" }, "符合條件"),
                                    h('span', { className: "text-2xl font-black text-indigo-600" }, filteredCount)
                                ),
                                h('button', { onClick: startQuiz, className: "w-full py-4 bg-slate-800 text-white rounded-2xl font-black text-lg shadow-xl hover:bg-slate-900 transition-all" }, "開始學習"),
                                h('button', { onClick: function() { setIsSettingUp(false); }, className: "w-full text-sm font-bold text-slate-400 py-2" }, "取消")
                            )
                        )
                    );
                }

                // ==================== 完成頁 ====================
                if(isFinished) {
                    return h('div', { className: "flex flex-col items-center justify-center min-h-screen p-6" },
                        h('div', { className: "glass max-w-sm w-full rounded-3xl shadow-2xl p-10 text-center" },
                            h('div', { className: "text-6xl mb-4" }, "\uD83C\uDFC6"),
                            h('h2', { className: "text-2xl font-black text-slate-800 mb-4" }, "測試完成！"),
                            h('div', { className: "grid grid-cols-2 gap-3 my-6" },
                                h('div', { className: "bg-red-50 p-4 rounded-2xl" }, h('p', { className: "text-[9px] font-black text-red-400 uppercase" }, "Again"), h('p', { className: "text-2xl font-black text-red-600" }, stats.again)),
                                h('div', { className: "bg-orange-50 p-4 rounded-2xl" }, h('p', { className: "text-[9px] font-black text-orange-400 uppercase" }, "Hard"), h('p', { className: "text-2xl font-black text-orange-600" }, stats.hard)),
                                h('div', { className: "bg-blue-50 p-4 rounded-2xl" }, h('p', { className: "text-[9px] font-black text-blue-400 uppercase" }, "Good"), h('p', { className: "text-2xl font-black text-blue-600" }, stats.good)),
                                h('div', { className: "bg-green-50 p-4 rounded-2xl" }, h('p', { className: "text-[9px] font-black text-green-400 uppercase" }, "Easy"), h('p', { className: "text-2xl font-black text-green-600" }, stats.easy))
                            ),
                            h('button', { onClick: function() { setVocabList([]); setIsFinished(false); setIsSettingUp(false); }, className: "w-full py-4 bg-indigo-600 text-white rounded-2xl font-black text-lg shadow-lg" }, "新學習")
                        )
                    );
                }

                // ==================== 學習卡片頁 ====================
                var current = vocabList[0];
                var progress = ((totalInitial - vocabList.length) / totalInitial) * 100;
                var isCn2En = quizMode === 'zh2en';

                var progressBar = h('div', { className: "w-full max-w-lg glass rounded-2xl shadow-lg p-4 mb-4" },
                    h('div', { className: "flex justify-between items-center text-xs font-black text-slate-500 mb-2" },
                        h('div', { className: "flex gap-2" },
                            h('span', { className: "text-red-500 bg-red-50 px-2 py-0.5 rounded-md" }, "A:" + stats.again),
                            h('span', { className: "text-orange-500 bg-orange-50 px-2 py-0.5 rounded-md" }, "H:" + stats.hard),
                            h('span', { className: "text-blue-500 bg-blue-50 px-2 py-0.5 rounded-md" }, "G:" + stats.good),
                            h('span', { className: "text-green-500 bg-green-50 px-2 py-0.5 rounded-md" }, "E:" + stats.easy)
                        ),
                        h('span', { className: "text-sm font-black text-indigo-600" }, vocabList.length + " / " + totalInitial),
                        h('button', { onClick: resetAll, className: "text-slate-400 hover:text-red-500 text-lg ml-2" }, "\u21BA")
                    ),
                    h('div', { className: "w-full h-2 bg-slate-100 rounded-full overflow-hidden" },
                        h('div', { className: "bg-indigo-500 h-full rounded-full transition-all duration-500", style: { width: progress + "%" } })
                    )
                );

                if(isCn2En && !isFlipped) {
                    // ===== 中翻英：互動填空模式 =====
                    return h('div', { className: "flex flex-col items-center min-h-screen p-4" },
                        progressBar,
                        h('div', { className: "glass max-w-lg w-full rounded-3xl shadow-2xl p-8" },
                            h('div', { className: "flex justify-between items-center mb-6" },
                                h('span', { className: "px-3 py-1 bg-emerald-100 text-emerald-700 text-xs font-black rounded-lg" }, "中翻英"),
                                h('div', { className: "flex gap-2" },
                                    h('span', { className: "px-3 py-1 bg-indigo-100 text-indigo-700 text-xs font-black rounded-lg" }, "L" + current.l),
                                    current.p && h('span', { className: "px-3 py-1 bg-slate-100 text-slate-600 text-xs font-black rounded-lg" }, current.p)
                                )
                            ),
                            h('p', { className: "text-sm font-bold text-slate-400 mb-2 text-center" }, "請根據中文意思拼出英文單字"),
                            h('h2', { className: "text-2xl font-black text-slate-800 mb-6 text-center leading-relaxed" }, current.d),
                            // 字母填空
                            h(LetterInputRow, {
                                key: current.w + '_' + vocabList.length,
                                word: current.w,
                                onComplete: function(correct) {
                                    setZh2enSubmitted(true);
                                    setTimeout(function() { setIsFlipped(true); }, 1500);
                                }
                            })
                        ),
                        h('div', { className: "w-full max-w-lg flex items-center gap-3 mt-4 py-2" },
                            h('span', { className: "text-sm" }, "\uD83D\uDD08"),
                            h('input', { type: 'range', min: '0.5', max: '2.0', step: '0.1', value: speechRate, onChange: function(ev) { setSpeechRate(parseFloat(ev.target.value)); }, className: "flex-grow h-1 bg-white rounded-full appearance-none accent-indigo-600" }),
                            h('span', { className: "text-xs font-black text-indigo-600 w-8" }, speechRate.toFixed(1) + "x")
                        )
                    );
                }

                if(!isCn2En && !isFlipped) {
                    // ===== 英翻中：正面 =====
                    return h('div', { className: "flex flex-col items-center min-h-screen p-4" },
                        progressBar,
                        h('div', { className: "glass max-w-lg w-full rounded-3xl shadow-2xl p-8 text-center cursor-pointer hover:shadow-indigo-200/50 transition-all", onClick: function() { setIsFlipped(true); } },
                            h('div', { className: "flex justify-between items-center mb-6" },
                                h('span', { className: "px-3 py-1 bg-indigo-100 text-indigo-700 text-xs font-black rounded-lg" }, "英翻中"),
                                h('div', { className: "flex gap-2" },
                                    h('span', { className: "px-3 py-1 bg-indigo-100 text-indigo-700 text-xs font-black rounded-lg" }, "L" + current.l),
                                    current.p && h('span', { className: "px-3 py-1 bg-slate-100 text-slate-600 text-xs font-black rounded-lg" }, current.p)
                                )
                            ),
                            h('button', { onClick: function(ev) { ev.stopPropagation(); speak(current.w, speechRate); }, className: "mx-auto mb-6 p-3 bg-indigo-50 text-indigo-600 rounded-full hover:bg-indigo-100 transition-all text-xl block" }, "\uD83D\uDD0A"),
                            h('h2', { className: "text-5xl font-black text-slate-800 mb-3" }, current.w),
                            current.i && h('p', { className: "text-lg text-slate-400 font-mono mb-4" }, current.i),
                            h('p', { className: "text-xs font-black text-slate-300 uppercase tracking-[0.3em] mt-8 animate-pulse" }, "\uD83D\uDC46 點擊查看釋義")
                        ),
                        h('div', { className: "w-full max-w-lg flex items-center gap-3 mt-4 py-2" },
                            h('span', { className: "text-sm" }, "\uD83D\uDD08"),
                            h('input', { type: 'range', min: '0.5', max: '2.0', step: '0.1', value: speechRate, onChange: function(ev) { setSpeechRate(parseFloat(ev.target.value)); }, className: "flex-grow h-1 bg-white rounded-full appearance-none accent-indigo-600" }),
                            h('span', { className: "text-xs font-black text-indigo-600 w-8" }, speechRate.toFixed(1) + "x")
                        )
                    );
                }

                // ===== 背面（答案 + 完整資訊 + SRS 按鈕） =====
                return h('div', { className: "flex flex-col items-center min-h-screen p-4" },
                    progressBar,
                    h('div', { className: "glass max-w-lg w-full rounded-3xl shadow-2xl p-6" },
                        h('div', { className: "flex justify-between items-center mb-4" },
                            h('div', { className: "flex gap-2 items-center" },
                                h('span', { className: "px-3 py-1 bg-indigo-600 text-white text-xs font-black rounded-lg" }, "L" + current.l),
                                current.p && h('span', { className: "px-3 py-1 bg-slate-200 text-slate-700 text-xs font-black rounded-lg" }, current.p)
                            ),
                            h('button', { onClick: function() { speak(current.w, speechRate); }, className: "p-2 bg-indigo-50 text-indigo-600 rounded-full hover:bg-indigo-100 text-xl" }, "\uD83D\uDD0A")
                        ),
                        h('h2', { className: "text-3xl font-black text-indigo-600 mb-1" }, current.w),
                        current.i && h('p', { className: "text-sm text-slate-500 font-mono mb-4" }, current.i),
                        h('hr', { className: "border-slate-100 mb-4" }),
                        h('div', { className: "info-block bg-indigo-50", style: { borderColor: '#6366f1' } },
                            h('p', { className: "text-[10px] font-black text-indigo-500 uppercase mb-1" }, "解釋 Definition"),
                            h('p', { className: "text-base font-bold text-slate-800" }, current.d)
                        ),
                        current.c && h('div', { className: "info-block bg-amber-50", style: { borderColor: '#f59e0b' } },
                            h('p', { className: "text-[10px] font-black text-amber-600 uppercase mb-1" }, "搭配字 Collocations"),
                            h('p', { className: "text-sm font-bold text-slate-700" }, current.c)
                        ),
                        current.x && h('div', { className: "info-block bg-blue-50", style: { borderColor: '#3b82f6' } },
                            h('p', { className: "text-[10px] font-black text-blue-500 uppercase mb-1" }, "例句 Example"),
                            h('p', { className: "text-sm text-slate-700 italic" }, current.x)
                        ),
                        current.t && h('div', { className: "info-block bg-emerald-50", style: { borderColor: '#10b981' } },
                            h('p', { className: "text-[10px] font-black text-emerald-600 uppercase mb-1" }, "衍生詞 Related"),
                            h('p', { className: "text-sm text-slate-700" }, current.t)
                        ),
                        h('div', { className: "grid grid-cols-4 gap-2 mt-6" },
                            h('button', { onClick: function() { handleSRS('again'); }, className: "py-3 bg-red-100 text-red-700 rounded-2xl text-xs font-black hover:bg-red-200 transition-all" }, "AGAIN"),
                            h('button', { onClick: function() { handleSRS('hard'); }, className: "py-3 bg-orange-100 text-orange-700 rounded-2xl text-xs font-black hover:bg-orange-200 transition-all" }, "HARD"),
                            h('button', { onClick: function() { handleSRS('good'); }, className: "py-3 bg-blue-100 text-blue-700 rounded-2xl text-xs font-black hover:bg-blue-200 transition-all" }, "GOOD"),
                            h('button', { onClick: function() { handleSRS('easy'); }, className: "py-3 bg-green-100 text-green-700 rounded-2xl text-xs font-black hover:bg-green-200 transition-all" }, "EASY")
                        )
                    )
                );
            }
            
            var root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(h(App));
        })();
    </script>
</body>
</html>""")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("".join(content))
    
    print("Vocab Master Build (Interactive + Excel) Success. Words: " + str(len(json.loads(json_str))))

if __name__ == "__main__":
    build_html()
