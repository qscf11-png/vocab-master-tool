import json
import os
from opencc import OpenCC

def build_html():
    vocab_data_path = "vocab_data.js"
    idiom_data_path = "idiom_data.js"
    output_path = "index.html"
    
    cc = OpenCC('s2t') # 簡體轉繁體

    # 讀取英文資料
    if not os.path.exists(vocab_data_path):
        print(f"Error: {vocab_data_path} not found.")
        return
    with open(vocab_data_path, "r", encoding="utf-8") as f:
        read_v = f.read()
        v_js = read_v.replace("const VOCAB_DB = ", "").strip()
        if v_js.endswith(";"): v_js = v_js[:-1]
    
    # 英文資料繁體化 (針對翻譯部分)
    v_js = cc.convert(v_js)

    # 讀取成語資料
    idiom_js = "[]"
    if os.path.exists(idiom_data_path):
        with open(idiom_data_path, "r", encoding="utf-8") as f:
            read_i = f.read()
            idiom_js = read_i.replace("const IDIOM_DB = ", "").strip()
            if idiom_js.endswith(";"): idiom_js = idiom_js[:-1]
    
    # 成語資料繁體化
    idiom_js = cc.convert(idiom_js)

    content = []
    content.append(r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>全能學習大師 Vocab & Idiom Master</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&family=Noto+Sans+TC:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Outfit', 'Noto Sans TC', sans-serif; background: linear-gradient(135deg, #e0e7ff 0%, #f1f5f9 50%, #dbeafe 100%); margin: 0; padding: 0; min-height: 100vh; }
        .glass { background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.5); }
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
        
        /* SRS 按鈕顏色 */
        .btn-again { border-color: #fee2e2; color: #dc2626; background: #fff5f5; }
        .btn-again:hover { background: #fee2e2; }
        .btn-hard { border-color: #ffedd5; color: #d97706; background: #fffafb; }
        .btn-hard:hover { background: #ffedd5; }
        .btn-good { border-color: #dcfce7; color: #16a34a; background: #f0fdf4; }
        .btn-good:hover { background: #dcfce7; }
        .btn-easy { border-color: #dbeafe; color: #2563eb; background: #eff6ff; }
        .btn-easy:hover { background: #dbeafe; }
    </style>
</head>
<body>
    <div id="root"></div>
    <script id="vocab-data" type="application/json">""")
    content.append(v_js)
    content.append(r"""</script>
    <script id="idiom-data" type="application/json">""")
    content.append(idiom_js)
    content.append(r"""</script>

    <script type="text/javascript">
        (function() {
            var h = React.createElement;
            var useState = React.useState;
            var useEffect = React.useEffect;
            var useMemo = React.useMemo;
            var useRef = React.useRef;
            
            var VOCAB_DB_RAW = JSON.parse(document.getElementById('vocab-data').textContent);
            var IDIOM_DB_RAW = JSON.parse(document.getElementById('idiom-data').textContent);

            function shuffle(arr) {
                var n = arr.slice();
                for(var i = n.length - 1; i > 0; i--) {
                    var j = Math.floor(Math.random() * (i + 1));
                    var tmp = n[i]; n[i] = n[j]; n[j] = tmp;
                }
                return n;
            }

            function IdiomFillIn(props) {
                var word = props.word;
                var onComplete = props.onComplete;
                var inputsRef = useRef([]);
                var chars = word.split('');
                var [values, setValues] = useState(() => {
                    var arr = new Array(chars.length).fill('');
                    arr[0] = chars[0]; // 預填首字
                    return arr;
                });
                var [submitted, setSubmitted] = useState(false);

                function handleChange(idx, val) {
                    if (submitted || idx === 0) return;
                    var nv = [...values]; nv[idx] = val.slice(-1);
                    setValues(nv);
                    if (val !== '' && idx < chars.length - 1) {
                        setTimeout(() => inputsRef.current[idx + 1]?.focus(), 10);
                    }
                }

                function handleKeyDown(idx, e) {
                    if (e.key === 'Backspace' && values[idx] === '' && idx > 1) {
                        setTimeout(() => inputsRef.current[idx - 1]?.focus(), 10);
                    }
                    if (e.key === 'Enter') {
                        setSubmitted(true);
                        var isCorrect = values.join('') === word;
                        onComplete(isCorrect);
                    }
                }

                return h('div', { className: 'flex flex-col items-center gap-6' },
                    h('div', { className: 'flex justify-center gap-2' }, chars.map((ch, i) => (
                        h('input', {
                            key: i,
                            ref: el => inputsRef.current[i] = el,
                            className: 'w-14 h-16 text-center text-2xl font-black rounded-xl border-2 transition-all ' + 
                                (i === 0 ? 'bg-slate-50 border-slate-200 text-slate-400' : 
                                 submitted ? (values[i] === chars[i] ? 'border-green-500 bg-green-50 text-green-700' : 'border-red-500 bg-red-50 text-red-700') :
                                 'border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100'),
                            value: values[i],
                            onChange: e => handleChange(i, e.target.value),
                            onKeyDown: e => handleKeyDown(i, e),
                            disabled: submitted || i === 0,
                            autoComplete: 'off'
                        })
                    ))),
                    !submitted && h('p', { className: 'text-xs font-black text-slate-300 animate-pulse' }, "輸入完成後按 Enter 檢查")
                );
            }

            function App() {
                var [subject, setSubject] = useState(null);
                var [mode, setMode] = useState('flashcard'); // flashcard or fillin
                var [activeList, setActiveList] = useState([]);
                var [totalInitial, setTotalInitial] = useState(0);
                var [stats, setStats] = useState({ again: 0, hard: 0, good: 0, easy: 0 });
                var [isSettingUp, setIsSettingUp] = useState(false);
                var [isFlipped, setIsFlipped] = useState(false);
                var [speechRate, setSpeechRate] = useState(1.0);
                var [levels, setLevels] = useState([1,2,3,4,5,6]);
                var [count, setCount] = useState(50);
                var [isFinished, setIsFinished] = useState(false);

                var currentDB = useMemo(() => {
                    if (!subject) return [];
                    return subject === 'idiom' ? IDIOM_DB_RAW : VOCAB_DB_RAW;
                }, [subject]);

                var filteredCount = useMemo(() => {
                    if (!subject) return 0;
                    if (subject === 'idiom') return currentDB.length;
                    return currentDB.filter(x => levels.indexOf(x.l)!==-1).length;
                }, [currentDB, levels, subject]);

                function startQuiz() {
                    var f = (subject === 'idiom') ? currentDB : currentDB.filter(x => levels.indexOf(x.l)!==-1);
                    if (f.length === 0) return;
                    var sampled = shuffle(f).slice(0, Math.min(count, f.length));
                    setActiveList(sampled); setTotalInitial(sampled.length);
                    setStats({ again: 0, hard: 0, good: 0, easy: 0 });
                    setIsSettingUp(false); setIsFinished(false); setIsFlipped(false);
                }

                function handleSRS(type) {
                    setStats(prev => { var n = {...prev}; n[type]++; return n; });
                    var rest = activeList.slice(1); var curr = activeList[0]; var next;
                    if(type === 'again') next = rest.length > 0 ? [rest[0], curr, ...rest.slice(1)] : [curr];
                    else if(type === 'hard') next = rest.length >= 4 ? [...rest.slice(0,4), curr, ...rest.slice(4)] : [...rest, curr];
                    else if(type === 'good') next = [...rest, curr];
                    else next = rest;
                    if(next.length === 0) setIsFinished(true);
                    setActiveList(next); setIsFlipped(false);
                }

                useEffect(() => {
                    if (activeList.length > 0 && !isFlipped && !isSettingUp && !isFinished) {
                        var item = activeList[0];
                        var l = (subject === 'idiom') ? 'zh-TW' : 'en-US';
                        if (mode === 'flashcard') {
                            setTimeout(() => speak(item.w, speechRate, l), 300);
                        } else if (mode === 'fillin') {
                            // 填空模式正面朗讀解釋
                            setTimeout(() => speak(item.d, speechRate, 'zh-TW'), 300);
                        }
                    }
                }, [activeList.length, isFlipped, isSettingUp, subject, mode]);

                useEffect(() => {
                    if (activeList.length > 0 && isFlipped && !isFinished) {
                        var item = activeList[0];
                        var l = (subject === 'idiom') ? 'zh-TW' : 'en-US';
                        var textToSpeak = item.x ? item.x : item.w;
                        setTimeout(() => speak(textToSpeak, speechRate, l), 100);
                    }
                }, [isFlipped]);

                useEffect(() => {
                    function handleK(e) {
                        if(e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
                        if(activeList.length === 0 || isFinished) return;
                        if (mode === 'flashcard' && (e.key === ' ' || e.code === 'Space')) { 
                            e.preventDefault(); setIsFlipped(true); 
                        }
                        if(isFlipped) {
                            if(e.key === '1') handleSRS('again'); if(e.key === '2') handleSRS('hard');
                            if(e.key === '3') handleSRS('good'); if(e.key === '4') handleSRS('easy');
                        }
                    }
                    window.addEventListener('keydown', handleK);
                    return () => window.removeEventListener('keydown', handleK);
                });

                if (!subject || (!activeList.length && !isSettingUp && !isFinished)) {
                    return h('div', { className: "flex flex-col items-center justify-center min-h-screen p-6" },
                        h('div', { className: "glass max-w-sm w-full rounded-3xl p-10 text-center" },
                            h('h1', { className: "text-3xl font-black mb-6" }, "全能學習大師"),
                            h('div', { className: "grid grid-cols-1 gap-3 mb-6" },
                                h('button', { onClick: () => { setSubject('vocab'); setMode('flashcard'); setIsSettingUp(true); }, className: "py-4 rounded-2xl border-2 hover:bg-indigo-50 transition-all font-bold" }, "英文單字 (閃卡)"),
                                h('button', { onClick: () => { setSubject('idiom'); setMode('flashcard'); setIsSettingUp(true); }, className: "py-4 rounded-2xl border-2 hover:bg-emerald-50 transition-all font-bold" }, "中文成語 (閃卡)"),
                                h('button', { onClick: () => { setSubject('idiom'); setMode('fillin'); setIsSettingUp(true); }, className: "py-4 rounded-2xl border-2 hover:bg-amber-50 transition-all font-bold" }, "中文成語 (填空)")
                            ),
                             h('p', { className: "text-xs text-slate-400" }, "選擇科目與模式開始學習")
                        )
                    );
                }

                if(isSettingUp) {
                    return h('div', { className: "flex flex-col items-center justify-center min-h-screen p-4" },
                        h('div', { className: "glass max-w-md w-full rounded-3xl p-8" },
                            h('div', { className: "flex justify-between items-center mb-6" },
                                h('h2', { className: "text-xl font-black" }, "測驗設定"),
                                h('button', { onClick: () => setSubject(null), className: "text-sm text-slate-400 hover:text-slate-600" }, "返回首頁")
                            ),
                            h('div', { className: "space-y-6" },
                                subject === 'vocab' && h('div', null,
                                    h('p', { className: "text-xs font-black text-slate-400 mb-2" }, "選擇等級"),
                                    h('div', { className: "flex flex-wrap gap-2" }, [1,2,3,4,5,6].map(l=>h('button', { key: l, onClick: ()=>setLevels(levels.includes(l)?levels.filter(x=>x!==l):levels.concat(l)), className: "px-4 py-2 rounded-lg border-2 " + (levels.includes(l)?'bg-indigo-600 text-white border-indigo-600':'border-slate-100') }, "L"+l)))
                                ),
                                h('div', null,
                                    h('div', { className: "flex justify-between mb-2" }, h('span', { className: "text-sm font-bold" }, "抽樣數量"), h('span', { className: "text-sm font-black text-indigo-600" }, count)),
                                    h('input', { type: 'range', min: 5, max: Math.min(filteredCount, 200), value: count, onChange: e=>setCount(parseInt(e.target.value)), className: "w-full accent-indigo-600" })
                                ),
                                h('button', { onClick: startQuiz, className: "w-full py-4 bg-slate-900 text-white rounded-2xl font-black shadow-xl shadow-slate-200" }, "開始測驗")
                            )
                        )
                    );
                }

                if(isFinished) {
                    return h('div', { className: "flex flex-col items-center justify-center min-h-screen p-6" },
                        h('div', { className: "glass max-w-sm w-full rounded-3xl p-10 text-center" },
                            h('h2', { className: "text-2xl font-black mb-6" }, "完成！"),
                            h('button', { onClick: ()=>setSubject(null), className: "w-full py-4 bg-indigo-600 text-white rounded-2xl font-bold" }, "返回首頁")
                        )
                    );
                }

                var curr = activeList[0];
                var prog = ((totalInitial - activeList.length) / totalInitial) * 100;
                var l_tag = (subject === 'idiom') ? 'zh-TW' : 'en-US';

                return h('div', { className: "flex flex-col items-center min-h-screen p-4" },
                    h('div', { className: "w-full max-w-lg flex items-center gap-4 mb-4" }, 
                        h('button', { onClick: () => setSubject(null), className: "p-2 glass rounded-xl text-slate-400 hover:text-slate-600" }, "🏠"),
                        h('div', { className: "flex-1 h-2 bg-white/50 rounded-full overflow-hidden" }, h('div', { className: "bg-indigo-500 h-full transition-all duration-500", style: { width: prog + "%" } }))
                    ),
                    !isFlipped ? h('div', { className: "glass max-w-lg w-full rounded-3xl p-10 text-center" },
                        mode === 'flashcard' ? h('div', { onClick: () => setIsFlipped(true), className: "cursor-pointer py-10" },
                            h('h2', { className: "text-5xl font-black mb-6 " + (subject==='idiom'?'tracking-widest':'') }, curr.w),
                            curr.py && h('p', { className: "text-lg text-slate-400 font-mono mb-10" }, curr.py),
                            h('p', { className: "text-xs font-black text-slate-300 animate-pulse" }, "點擊查看解答")
                        ) : h('div', { className: "py-4 text-left" },
                            h('div', { className: "info-block bg-indigo-50 border-indigo-400 mb-10" }, 
                                h('p', { className: "text-[10px] uppercase font-black text-indigo-400 mb-1" }, "請根據解釋提供成語"),
                                h('p', { className: "text-lg font-bold" }, curr.d)
                            ),
                            h(IdiomFillIn, { word: curr.w, onComplete: () => setIsFlipped(true) })
                        )
                    ) : h('div', { className: "glass max-w-lg w-full rounded-3xl p-8" },
                        h('div', { className: "flex justify-between items-center mb-4" },
                            h('h2', { className: "text-3xl font-black text-indigo-600" }, curr.w),
                            h('button', { onClick: ()=>speak(curr.w, speechRate, l_tag), className: "p-3 bg-indigo-50 rounded-2xl text-xl transition-all active:scale-90" }, "\uD83D\uDD0A")
                        ),
                        h('hr', { className: "mb-6 border-slate-100" }),
                        h('div', { className: "space-y-4" },
                            h('div', { className: "info-block bg-indigo-50 border-indigo-400" }, h('p', { className: "text-[10px] uppercase font-black text-indigo-400" }, "解釋"), h('p', { className: "text-base font-bold" }, curr.d)),
                            curr.o && h('div', { className: "info-block bg-amber-50 border-amber-400" }, h('p', { className: "text-[10px] uppercase font-black text-amber-400" }, "出處"), h('p', { className: "text-sm" }, curr.o)),
                            curr.x && h('div', { className: "info-block bg-blue-50 border-blue-400" }, h('p', { className: "text-[10px] uppercase font-black text-blue-400" }, "例句"), h('p', { className: "text-sm italic" }, curr.x))
                        ),
                        h('div', { className: "grid grid-cols-4 gap-2 mt-10" }, ['again', 'hard', 'good', 'easy'].map(t=>h('button', { key: t, onClick: ()=>handleSRS(t), className: "btn-" + t + " py-4 rounded-2xl border-2 text-xs font-black transition-all transform active:scale-95" }, t.toUpperCase())))
                    )
                );
            }
            ReactDOM.createRoot(document.getElementById('root')).render(h(App));
        })();
    </script>
</body>
</html>""")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("".join(content))
    
    print(f"Build Success. Vocab & Idiom converted to Traditional. UI Updated.")

if __name__ == "__main__":
    build_html()
