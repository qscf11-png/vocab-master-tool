import json
import os
import re
from opencc import OpenCC

def build_html():
    vocab_data_path = "vocab_data.js"
    idiom_data_path = "idiom_data.js"
    math_data_path = "math_data.js"
    cc = OpenCC('s2t')

    def get_db_data(path):
        if not os.path.exists(path): return "[]"
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                start = content.find('[')
                end = content.rfind(']')
                if start != -1 and end != -1:
                    js_str = content[start:end+1]
                    return cc.convert(js_str)
        except Exception as e:
            print(f"Error reading {path}: {e}")
        return "[]"

    v_json = get_db_data(vocab_data_path)
    i_json = get_db_data(idiom_data_path)
    m_json = get_db_data(math_data_path)

    # 1. index.html - 專屬【英文單字】(2024 Gold Elite 究極金牌版)
    english_template = r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vocab Master Gold Elite</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.sheetjs.com/xlsx-0.20.0/package/dist/xlsx.full.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&family=Noto+Sans+TC:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Outfit', 'Noto Sans TC', sans-serif; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); margin: 0; padding: 0; min-height: 100vh; color: #1e293b; overflow-x: hidden; }
        .glass { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(25px); border: 1px solid rgba(255,255,255,0.4); box-shadow: 0 8px 32px rgba(31, 38, 135, 0.07); }
        .card-container { height: 520px; width: 100%; max-width: 460px; position: relative; perspective: 2000px; margin-top: 1rem; }
        .card { position: relative; width: 100%; height: 100%; transition: transform 0.8s cubic-bezier(0.34, 1.56, 0.64, 1); transform-style: preserve-3d; cursor: pointer; }
        .card.is-flipped { transform: rotateY(180deg); }
        .card-face { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; border-radius: 4rem; display: flex; flex-direction: column; padding: 2.5rem; box-shadow: 0 25px 60px -15px rgba(0,0,0,0.1); }
        .card-front { background: white; border: 1px solid #e2e8f0; align-items: center; justify-content: center; }
        .card-back { background: #ffffff; border: 1px solid #e2e8f0; transform: rotateY(180deg); overflow-y: auto; padding: 2.2rem; }
        .srs-btn { transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); font-weight: 900; height: 3.8rem; border-radius: 1.5rem; border: 2px solid transparent; text-transform: uppercase; letter-spacing: 0.05em; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .srs-btn:hover { transform: translateY(-3px); box-shadow: 0 10px 20px -5px rgba(0,0,0,0.1); }
        .btn-again { border-color: #fee2e2; color: #dc2626; background: #fff5f5; }
        .btn-hard { border-color: #ffedd5; color: #d97706; background: #fffafb; }
        .btn-good { border-color: #dcfce7; color: #16a34a; background: #f0fdf4; }
        .btn-easy { border-color: #dbeafe; color: #2563eb; background: #eff6ff; }
        .info-label { font-size: 0.65rem; font-weight: 900; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.3rem; display: block; }
        .content-box { border-radius: 1.25rem; padding: 1.25rem; margin-bottom: 1rem; width: 100%; text-align: left; transition: all 0.3s; }
        .box-def { background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%); color: #4338ca; }
        .box-col { background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); color: #92400e; }
        .box-exam { background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); color: #075985; border: 1px solid #bae6fd; }
        .ipa-text { color: #94a3b8; font-family: sans-serif; font-size: 1.1rem; font-weight: 500; margin-top: -0.5rem; }
        .progress-indicator { height: 10px; background: #e2e8f0; border-radius: 5px; overflow: hidden; flex-grow: 1; margin: 0 1rem; position: relative; }
        .progress-fill { height: 100%; background: linear-gradient(90deg, #6366f1, #10b981); transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
        .btn-icon { width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 14px; background: white; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); transition: all 0.2s; border: 1px solid #f1f5f9; }
        .btn-icon:hover { transform: scale(1.1); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
        .badge { padding: 2px 8px; border-radius: 6px; font-size: 0.6rem; font-weight: 900; }
        input[type="range"] { -webkit-appearance: none; height: 6px; background: #cbd5e1; border-radius: 5px; cursor: pointer; }
        input[type="range"]::-webkit-slider-thumb { -webkit-appearance: none; width: 16px; height: 16px; background: #6366f1; border-radius: 50%; box-shadow: 0 0 10px rgba(99, 102, 241, 0.5); }
    </style>
</head>
<body>
    <div id="root"></div>
    <script type="text/javascript">
        window.VOCAB_DB = VOCAB_DATA_PLACEHOLDER;
        (function() {
            const h = React.createElement; const { useState, useEffect, useRef } = React;

            function App() {
                const [view, setView] = useState('home'); 
                const [db, setDb] = useState(window.VOCAB_DB);
                const [quizList, setQuizList] = useState([]);
                const [isFlipped, setIsFlipped] = useState(false);
                const [lvlFilter, setLvlFilter] = useState('all'); 
                const [prefixFilter, setPrefixFilter] = useState('');
                const [limit, setLimit] = useState(20);
                const [stats, setStats] = useState({ again: 0, hard: 0, good: 0, easy: 0 });
                const [totalInitial, setTotalInitial] = useState(0);
                const [speechRate, setSpeechRate] = useState(0.9);
                const [isSoundOn, setIsSoundOn] = useState(true);
                const [showInfo, setShowInfo] = useState(false);

                useEffect(() => {
                    const saved = localStorage.getItem('vocab_master_gold_save_v3');
                    if (saved) {
                        try {
                            const data = JSON.parse(saved);
                            if (data.quizList && data.quizList.length > 0) {
                                setQuizList(data.quizList); setStats(data.stats); setTotalInitial(data.totalInitial || data.quizList.length); 
                                setLvlFilter(data.lvlFilter || 'all'); setSpeechRate(data.speechRate || 0.9); setView('quiz');
                            }
                        } catch(e) {}
                    }
                }, []);

                useEffect(() => {
                    if (view === 'quiz') {
                        localStorage.setItem('vocab_master_gold_save_v3', JSON.stringify({ quizList, stats, totalInitial, lvlFilter, speechRate }));
                    }
                }, [quizList, stats, speechRate]);

                const speak = (content) => {
                    if (!isSoundOn || !content) return;
                    window.speechSynthesis.cancel();
                    const u = new SpeechSynthesisUtterance(content);
                    u.lang = 'en-US'; u.rate = speechRate;
                    window.speechSynthesis.speak(u);
                };

                // 自動朗讀核心：處理翻面與切換卡片
                useEffect(() => {
                    if (view === 'quiz' && quizList.length > 0) {
                        const curr = quizList[0];
                        if (!isFlipped) {
                            // 正面：自動朗讀單字 (w)
                            speak(curr.w || curr.word);
                        } else {
                            // 背面：自動朗讀例句 (x)，若無理句則朗讀單字
                            const toSpeak = curr.x || curr.e || curr.w || curr.word;
                            speak(toSpeak);
                        }
                    }
                }, [quizList[0]?.w, isFlipped, view]); // 監聽單字變化與翻動

                const startQuiz = () => {
                    let filtered = [...db];
                    if (lvlFilter !== 'all') filtered = filtered.filter(i => String(i.l) === lvlFilter);
                    if (prefixFilter) filtered = filtered.filter(i => (i.w || i.word || "").toLowerCase().startsWith(prefixFilter.toLowerCase()));
                    const shuffled = filtered.sort(() => Math.random() - 0.5).slice(0, parseInt(limit));
                    setQuizList(shuffled); setTotalInitial(shuffled.length); setStats({ again: 0, hard: 0, good: 0, easy: 0 });
                    setView('quiz'); setIsFlipped(false);
                };

                const handleSRS = (type) => {
                    let newList = [...quizList];
                    const curr = newList.shift(); if (!curr) return;
                    setStats(prev => ({ ...prev, [type]: prev[type] + 1 }));

                    if (type === 'again') newList.splice(1, 0, curr); 
                    else if (type === 'hard') newList.splice(4, 0, curr); 
                    else if (type === 'good') newList.push(curr); 

                    if (newList.length === 0) { setView('result'); localStorage.removeItem('vocab_master_gold_save_v3'); }
                    else { setQuizList(newList); setIsFlipped(false); }
                };

                const resetAll = () => {
                    localStorage.removeItem('vocab_master_gold_save_v3');
                    window.location.reload();
                };

                const handleFileUpload = (e) => {
                    const file = e.target.files[0];
                    if (!file) return;
                    const reader = new FileReader();
                    
                    if (file.name.endsWith('.xlsx')) {
                        reader.onload = (ev) => {
                            try {
                                const data = new Uint8Array(ev.target.result);
                                const workbook = XLSX.read(data, { type: 'array' });
                                const sheet = workbook.Sheets[workbook.SheetNames[0]];
                                const json = XLSX.utils.sheet_to_json(sheet);
                                // 映射 Excel 到我們的格式
                                const mapped = json.map(row => ({
                                    w: row.Word || row.word || "",
                                    d: row.Definition || row.definition || "",
                                    i: row.IPA || row.ipa || "",
                                    p: row.POS || row.pos || "n.",
                                    c: row.Collocation || row.collocation || "",
                                    x: row.Example || row.example || "",
                                    l: row.Level || row.level || 1
                                }));
                                setDb(mapped);
                                alert("成功載入 " + mapped.length + " 筆 Excel 單字！");
                            } catch(err) { alert("Excel 解析錯誤: " + err.message); }
                        };
                        reader.readAsArrayBuffer(file);
                    } else {
                        reader.onload = (ev) => {
                            try {
                                const data = JSON.parse(ev.target.result);
                                setDb(data); alert("載入共 " + data.length + " 筆 JSON");
                            } catch(err) { alert("JSON 錯誤"); }
                        };
                        reader.readAsText(file);
                    }
                };

                const downloadExample = () => {
                    const data = [
                        ["Word", "Definition", "IPA", "POS", "Collocation", "Example", "Level"],
                        ["abundant", "豐富的；充沛的", "/əˈbʌndənt/", "adj.", "abundant natural resources", "The country has abundant natural resources.", 1],
                        ["perhaps", "也許；可能", "/pəˈhæps/", "adv.", "perhaps not", "Perhaps he will come tomorrow.", 2]
                    ];
                    const ws = XLSX.utils.aoa_to_sheet(data);
                    const wb = XLSX.utils.book_new();
                    XLSX.utils.book_append_sheet(wb, ws, "VocabTemplate");
                    XLSX.writeFile(wb, "VocabMaster_Template.xlsx");
                };

                // 全域鍵盤事件
                useEffect(() => {
                    const handleKey = (e) => {
                        if (view !== 'quiz') return;
                        const key = e.key;
                        const code = e.code;
                        
                        // 1. 翻轉卡片 (Space)
                        if (code === 'Space') { 
                            e.preventDefault(); 
                            setIsFlipped(f => !f); 
                        }
                        // 2. 朗讀 (Enter)
                        else if (key === 'Enter') {
                            const curr = quizList[0];
                            if (!isFlipped) speak(curr.w || curr.word);
                            else speak(curr.x || curr.e || curr.w || curr.word);
                        }
                        // 3. SRS 評級 (1-4) - 僅限背面翻開時
                        else if (isFlipped) {
                            if (key === '1') handleSRS('again');
                            else if (key === '2') handleSRS('hard');
                            else if (key === '3') handleSRS('good');
                            else if (key === '4') handleSRS('easy');
                        }
                        
                        // 4. 切換顯示說明 (i)
                        if (key === 'i' || key === 'I') setShowInfo(v => !v);
                    };
                    window.addEventListener('keydown', handleKey);
                    return () => window.removeEventListener('keydown', handleKey);
                }, [view, isFlipped, quizList, isSoundOn, speechRate]); // 確保監聽器獲取最新狀態

                if (view === 'home') return h('div', { className: "flex flex-col items-center justify-center min-h-screen p-6" },
                    h('div', { className: "glass max-w-sm w-full rounded-[4rem] p-12 text-center relative" },
                        h('div', { className: "w-24 h-24 bg-gradient-to-tr from-indigo-600 to-purple-500 rounded-[2.5rem] mx-auto mb-10 flex items-center justify-center shadow-2xl rotate-3" }, h('span', { className: "text-white text-5xl font-black -rotate-3" }, "V")),
                        h('h1', { className: "text-4xl font-black mb-10 tracking-tight" }, "Vocab Master", h('span', { className: "block text-sm text-indigo-500 mt-1 uppercase tracking-widest" }, "Gold Elite Edition")),
                        h('div', { className: "space-y-4" },
                            h('button', { onClick: () => setView('setup'), className: "w-full py-5 rounded-[2.2rem] bg-slate-900 text-white font-black text-xl shadow-xl hover:shadow-2xl transition-all active:scale-95" }, "開始練習"),
                            h('label', { className: "block w-full py-4 rounded-[2.2rem] bg-white border-2 border-slate-100 text-slate-600 font-black text-lg shadow-sm hover:bg-slate-50 cursor-pointer transition-all" }, "📁 載入 Excel/JSON", h('input', { type: 'file', accept: ".xlsx,.json", hidden: true, onChange: handleFileUpload })),
                            h('button', { onClick: downloadExample, className: "w-full py-3 text-indigo-500 font-bold text-sm hover:underline" }, "📥 下載範例 Excel"),
                            h('a', { href: 'entry.html', className: "block mt-6 text-slate-400 font-bold hover:text-slate-600 transition-colors" }, "← 結束並離開")
                        )
                    )
                );

                if (view === 'setup') return h('div', { className: "flex flex-col items-center justify-center min-h-screen p-6" },
                    h('div', { className: "glass max-w-sm w-full rounded-[3.5rem] p-10" },
                        h('h2', { className: "text-3xl font-black mb-10 text-center tracking-tight" }, "客製化學習"),
                        h('div', { className: "mb-8 text-left" }, h('label', { className: "info-label" }, "選擇等級"), h('select', { value: lvlFilter, onChange: e => setLvlFilter(e.target.value), className: "w-full p-5 rounded-[1.5rem] bg-white border border-slate-100 font-black shadow-inner" }, h('option', { value: 'all' }, "全部範圍 (All)"), [1,2,3,4,5,6].map(l => h('option', { key: l, value: l }, "Level " + l)))),
                        h('div', { className: "mb-8 text-left" }, h('label', { className: "info-label" }, "字首過濾 (A-Z)"), h('input', { value: prefixFilter, onChange: e => setPrefixFilter(e.target.value), placeholder: "例: a", className: "w-full p-5 rounded-[1.5rem] bg-white border border-slate-100 font-black shadow-inner" })),
                        h('div', { className: "mb-12 text-left" }, h('div', { className: "flex justify-between items-end mb-4" }, h('label', { className: "info-label" }, "練習字數"), h('span', { className: "font-black text-2xl text-indigo-600" }, limit)), h('input', { type: 'range', min: 5, max: 200, step: 5, value: limit, onChange: e => setLimit(e.target.value), className: "w-full" })),
                        h('button', { onClick: startQuiz, className: "w-full py-5 bg-indigo-600 text-white rounded-[2rem] font-black text-xl shadow-lg ring-4 ring-indigo-50 shadow-indigo-200 mb-4" }, "開始挑戰"),
                        h('label', { className: "block w-full py-4 rounded-[1.8rem] bg-slate-100 text-slate-600 font-black text-center cursor-pointer hover:bg-slate-200 transition-all" }, "📁 更換字庫檔案", h('input', { type: 'file', hidden: true, onChange: handleFileUpload })),
                        h('button', { onClick: () => setView('home'), className: "w-full mt-6 text-slate-400 font-bold" }, "返回首頁")
                    )
                );

                if (view === 'quiz') {
                    const curr = quizList[0]; if (!curr) return null;
                    const progress = totalInitial > 0 ? ((totalInitial - quizList.length) / totalInitial) * 100 : 0;
                    
                    return h('div', { className: "flex flex-col items-center min-h-screen p-4 pt-8" },
                        h('div', { className: "w-full max-w-5xl flex items-center justify-between gap-4 mb-2 px-2" },
                            h('button', { onClick: resetAll, className: "btn-icon" }, "🏠"),
                            h('div', { className: "progress-indicator" }, h('div', { className: "progress-fill", style: { width: progress + "%" } })),
                            h('div', { className: "flex items-center gap-3 text-[0.65rem] font-black" },
                                h('span', { className: "bg-slate-200 px-3 py-1 rounded-full" }, (totalInitial - quizList.length + 1) + " / " + totalInitial),
                                h('div', { className: "flex gap-2" },
                                    h('span', { className: "text-red-500" }, "A:" + stats.again), h('span', { className: "text-amber-500" }, "H:" + stats.hard),
                                    h('span', { className: "text-emerald-500" }, "G:" + stats.good), h('span', { className: "text-blue-500" }, "E:" + stats.easy)
                                )
                            ),
                            h('button', { onClick: () => setShowInfo(!showInfo), className: "btn-icon" }, "ℹ️")
                        ),

                        showInfo && h('div', { className: "w-full max-w-sm bg-slate-900/90 backdrop-blur-md text-white p-6 rounded-[2rem] my-4 text-xs leading-relaxed z-50 shadow-2xl" },
                            h('h4', { className: "font-black mb-3 text-indigo-400 text-sm" }, "快捷操作指南"),
                            h('div', { className: "grid grid-cols-2 gap-4" },
                                h('div', null, h('p', { className: "mb-1" }, h('b', null, "Space"), " 翻轉卡片"), h('p', null, h('b', null, "Enter"), " 再次朗讀")),
                                h('div', null, h('p', { className: "mb-1" }, h('b', null, "1 - 4"), " 快速評級"), h('p', null, h('b', null, "i"), " 開關說明"))
                            )
                        ),

                        h('div', { className: "card-container" },
                            h('div', { className: "card " + (isFlipped ? "is-flipped" : ""), onClick: () => setIsFlipped(!isFlipped) },
                                h('div', { className: "card-face card-front" },
                                    h('div', { className: "flex flex-col items-center gap-10" },
                                        h('div', { className: "bg-indigo-50 text-indigo-600 badge absolute top-10" }, "Level " + (curr.l || "X")),
                                        h('h2', { className: "text-7xl font-black tracking-tighter" }, curr.w || curr.word),
                                        h('button', { onClick: (e) => { e.stopPropagation(); speak(curr.w || curr.word); }, className: "w-20 h-20 bg-slate-50 border border-slate-100 rounded-[2rem] flex items-center justify-center text-4xl shadow-sm hover:scale-110 active:scale-90 transition-all" }, "🔊")
                                    )
                                ),
                                h('div', { className: "card-face card-back" },
                                    h('div', { className: "flex justify-between items-start mb-6" },
                                        h('div', null, 
                                            h('h3', { className: "text-indigo-600 font-black text-3xl tracking-tight leading-none mb-1" }, curr.w || curr.word),
                                            h('div', { className: "ipa-text" }, curr.i || curr.ipa || "/ /")
                                        ),
                                        h('button', { onClick: (e) => { e.stopPropagation(); speak(curr.x || curr.e || curr.w || curr.word); }, className: "btn-icon" }, "🔊")
                                    ),
                                    h('div', { className: "content-box box-def" }, 
                                        h('label', { className: "info-label text-indigo-400" }, "解釋 DEFINITION & POS"), 
                                        h('p', { className: "text-lg font-black" }, h('span', { className: "badge bg-indigo-200 text-indigo-700 mr-2" }, curr.p || curr.pos || "word"), curr.d || curr.definition || "N/A")
                                    ),
                                    (curr.c || curr.collocation) && h('div', { className: "content-box box-col" }, 
                                        h('label', { className: "info-label text-amber-500" }, "搭配與詞性變化 COLLOCATION"), 
                                        h('p', { className: "text-sm font-bold" }, (curr.c || curr.collocation) + (curr.t ? " | " + curr.t : ""))
                                    ),
                                    (curr.x || curr.e) && h('div', { className: "content-box box-exam" }, 
                                        h('label', { className: "info-label text-sky-500" }, "精選例句 EXAMPLE SENTENCE"), 
                                        h('p', { className: "text-sm font-medium leading-relaxed italic" }, "“" + (curr.x || curr.e) + "”")
                                    )
                                )
                            )
                        ),

                        h('div', { className: "w-full max-w-sm flex items-center gap-6 px-10 my-8" },
                            h('button', { onClick: () => setIsSoundOn(!isSoundOn), className: "text-3xl grayscale hover:grayscale-0 transition-all transform hover:scale-110" }, isSoundOn ? "🔊" : "🔇"),
                            h('div', { className: "flex-grow flex flex-col gap-1" },
                                h('input', { type: 'range', min: 0.5, max: 1.5, step: 0.1, value: speechRate, onChange: e => setSpeechRate(parseFloat(e.target.value)), className: "w-full" }),
                                h('div', { className: "flex justify-between text-[0.5rem] font-black text-slate-400 uppercase tracking-tighter" }, h('span', null, "Slow"), h('span', null, "Speed: " + speechRate + "x"), h('span', null, "Fast"))
                            )
                        ),

                        isFlipped && h('div', { className: "grid grid-cols-4 gap-4 w-full max-w-lg mb-8" },
                            ['Again', 'Hard', 'Good', 'Easy'].map((b, i) => h('button', { key: i, onClick: (e) => { e.stopPropagation(); handleSRS(b.toLowerCase()); }, className: `srs-btn btn-${b.toLowerCase()}` }, 
                                h('span', { className: "text-xs" }, h('b', null, i + 1)), h('span', null, b)
                            ))
                        )
                    );
                }

                if (view === 'result') return h('div', { className: "flex flex-col items-center justify-center min-h-screen p-6" },
                    h('div', { className: "glass max-w-sm w-full rounded-[4rem] p-12 text-center" }, 
                        h('div', { className: "text-6xl mb-8" }, "🏆"),
                        h('h3', { className: "text-4xl font-black mb-10 tracking-tight" }, "完成學習！"), 
                        h('button', { onClick: resetAll, className: "w-full py-5 bg-indigo-600 text-white rounded-[2rem] font-black text-xl shadow-lg" }, "再次訓練")
                    )
                );
            }
            ReactDOM.createRoot(document.getElementById('root')).render(h(App));
        })();
    </script>
</body>
</html>"""

    # 2. idiom.html - 專屬【成語】
    idiom_template = r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Idiom Master Gold</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans TC', sans-serif; background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); min-height: 100vh; color: #064e3b; }
        .glass { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(20px); border-radius: 3.5rem; border: 1px solid rgba(255,255,255,0.4); box-shadow: 0 8px 32px rgba(0,0,0,0.05); }
        .card-container { height: 480px; width: 100%; max-width: 400px; position: relative; perspective: 1000px; }
        .card { position: absolute; width: 100%; height: 100%; transition: transform 0.6s; transform-style: preserve-3d; cursor: pointer; }
        .card.is-flipped { transform: rotateY(180deg); }
        .card-face { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; border-radius: 3rem; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2rem; text-align: center; }
        .card-front { background: white; border: 1px solid #d1fae5; }
        .card-back { background: white; border: 3px solid #10b981; transform: rotateY(180deg); }
        .content-box { background: #f0fdf4; border-radius: 1.5rem; padding: 1.25rem; margin-bottom: 1rem; width: 100%; text-align: left; }
    </style>
</head>
<body>
    <div id="root"></div>
    <script type="text/javascript">
        window.IDIOM_DB = IDIOM_DATA_PLACEHOLDER;
        (function() {
            const h = React.createElement; const { useState } = React;
            function App() {
                const [view, setView] = useState('home'); const [mode, setMode] = useState('flash');
                const [quizList, setQuizList] = useState([]); const [currIdx, setCurrIdx] = useState(0);
                const [isFlipped, setIsFlipped] = useState(false); const [userInput, setUserInput] = useState('');
                const [isSubmitted, setIsSubmitted] = useState(false); const [isCorrect, setIsCorrect] = useState(false);

                const startQuiz = (m) => {
                    const shuffled = [...window.IDIOM_DB].sort(() => Math.random() - 0.5).slice(0, 20);
                    setQuizList(shuffled); setMode(m); setCurrIdx(0); setView('quiz'); setIsFlipped(false); setIsSubmitted(false); setUserInput('');
                };

                if (view === 'home') return h('div', { className: "flex flex-col items-center justify-center min-h-screen p-6" },
                    h('div', { className: "glass max-w-sm w-full p-12 text-center" },
                        h('div', { className: "w-20 h-20 bg-emerald-600 rounded-3xl mx-auto mb-8 flex items-center justify-center" }, h('span', { className: "text-white text-4xl font-black" }, "成")),
                        h('h1', { className: "text-4xl font-black mb-10" }, "成語大師"),
                        h('div', { className: "space-y-4" },
                            h('button', { onClick: () => startQuiz('flash'), className: "w-full py-5 rounded-[2rem] bg-emerald-600 text-white font-black" }, "閃卡測試"),
                            h('button', { onClick: () => startQuiz('fill'), className: "w-full py-5 rounded-[2rem] bg-emerald-500 text-white font-black" }, "填空挑戰"),
                            h('a', { href: 'entry.html', className: "block mt-8 text-slate-400 font-bold" }, "← 返回入口")
                        )
                    )
                );

                if (view === 'quiz') {
                    const curr = quizList[currIdx]; const t = curr.word || curr.w || "";
                    if (mode === 'flash') return h('div', { className: "flex flex-col items-center justify-center min-h-screen p-6" },
                        h('div', { className: "card-container mb-8", onClick: () => setIsFlipped(!isFlipped) },
                            h('div', { className: "card " + (isFlipped ? "is-flipped" : "") },
                                h('div', { className: "card-face card-front" }, h('h2', { className: "text-5xl font-black" }, t)),
                                h('div', { className: "card-face card-back" },
                                    h('div', { className: "content-box" }, h('p', { className: "text-xl font-black text-emerald-900" }, curr.definition || curr.d || ""))
                                )
                            )
                        ),
                        h('button', { onClick: () => { setCurrIdx(currIdx+1 < quizList.length ? currIdx+1 : 0); setIsFlipped(false); }, className: "py-4 px-12 bg-emerald-600 text-white rounded-full font-black" }, "下一題")
                    );
                    else return h('div', { className: "flex flex-col items-center justify-center min-h-screen" },
                        h('div', { className: "glass max-w-lg w-full p-12 text-center" },
                            h('h2', { className: "text-2xl font-black mb-8" }, curr.definition || curr.d || ""),
                            !isSubmitted ? h('div', null,
                                h('input', { value: userInput, onChange: e => setUserInput(e.target.value), className: "w-full p-4 text-2xl font-bold bg-emerald-50 rounded-2xl text-center mb-6" }),
                                h('button', { onClick: () => { const ok = (userInput === t); setIsCorrect(ok); setIsSubmitted(true); }, className: "w-full py-4 bg-emerald-600 text-white rounded-2xl font-black" }, "檢查")
                            ) : h('div', null,
                                h('h3', { className: "text-4xl font-black text-emerald-600 mb-6" }, t),
                                h('button', { onClick: () => { setCurrIdx(currIdx+1); setIsSubmitted(false); setUserInput(''); }, className: "w-full py-4 bg-slate-800 text-white rounded-2xl font-black" }, "下一題")
                            )
                        )
                    );
                }
                return null;
            }
            ReactDOM.createRoot(document.getElementById('root')).render(h(App));
        })();
    </script>
</body>
</html>"""

    # 3. math.html - 專屬【數學】
    math_template = r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Math Master Gold</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
    <style>
        body { font-family: sans-serif; background: #f8fafc; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .glass { background: white; border-radius: 3rem; padding: 2.5rem; max-width: 480px; width: 100%; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.05); }
        .card-container { height: 400px; width: 100%; position: relative; perspective: 1000px; }
        .card { position: absolute; width: 100%; height: 100%; transition: transform 0.6s; transform-style: preserve-3d; cursor: pointer; }
        .card.is-flipped { transform: rotateY(180deg); }
        .card-face { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; border-radius: 2rem; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2rem; text-align: center; border: 1px solid #e2e8f0; }
        .card-back { background: #f0f9ff; border: 2px solid #0ea5e9; transform: rotateY(180deg); }
        .srs-btn { height: 4rem; border-radius: 1rem; font-weight: 900; border: 2px solid #e2e8f0; }
    </style>
</head>
<body>
    <div id="root"></div>
    <script>
        window.M_DATA = MATH_DATA_PLACEHOLDER;
        (function() {
            const h = React.createElement; const { useState, useEffect } = React;
            function App() {
                const [idx, setIdx] = useState(0); const [flipped, setFlipped] = useState(false);
                useEffect(() => { window.renderMathInElement(document.body, { delimiters: [{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}] }); }, [idx, flipped]);
                const next = () => { if(idx+1 < window.M_DATA.length) { setIdx(idx+1); setFlipped(false); } };
                const item = window.M_DATA[idx];
                return h('div', {className:"glass"},
                    h('div', {className:"flex justify-between mb-6"}, h('a', {href:'entry.html'}, "✕"), h('span', null, (idx+1)+"/"+window.M_DATA.length)),
                    h('div', {className:"card-container mb-8", onClick:()=>setFlipped(!flipped)},
                        h('div', {className:"card "+(flipped?"is-flipped":"")},
                            h('div', {className:"card-face card-front"}, h('h2', {className:"text-2xl font-bold"}, item.w)),
                            h('div', {className:"card-face card-back"}, h('div', {className:"font-bold"}, item.d))
                        )
                    ),
                    flipped ? h('div', {className:"grid grid-cols-4 gap-2"}, ['Again','Hard','Good','Easy'].map((b,i)=>h('button',{key:i, onClick:next, className:"srs-btn"}, b))) : h('p', null, "點擊翻面")
                );
            }
            ReactDOM.createRoot(document.getElementById('root')).render(h(App));
        })();
    </script>
</body>
</html>"""

    # 替換資料並生成檔案
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(english_template.replace("VOCAB_DATA_PLACEHOLDER", v_json))
    with open("idiom.html", "w", encoding="utf-8") as f:
        f.write(idiom_template.replace("IDIOM_DATA_PLACEHOLDER", i_json))
    with open("math.html", "w", encoding="utf-8") as f:
        f.write(math_template.replace("MATH_DATA_PLACEHOLDER", m_json))
    
    print("Build Success: index.html (English), idiom.html (Idiom), math.html (Math) generated.")

if __name__ == "__main__":
    build_html()
