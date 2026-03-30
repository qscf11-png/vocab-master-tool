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

    # 1. index.html - 專屬【英文單字】(2024 究極金牌版)
    english_template = r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vocab Master Gold Elite</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&family=Noto+Sans+TC:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Outfit', 'Noto Sans TC', sans-serif; background: #f1f5f9; margin: 0; padding: 0; min-height: 100vh; color: #1e293b; overflow-x: hidden; }
        .glass { background: rgba(255, 255, 255, 0.82); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.3); }
        .card-container { height: auto; min-height: 480px; width: 100%; max-width: 440px; position: relative; perspective: 2000px; }
        .card { position: relative; width: 100%; height: 100%; transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1); transform-style: preserve-3d; cursor: pointer; }
        .card.is-flipped { transform: rotateY(180deg); }
        .card-face { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; border-radius: 3.5rem; display: flex; flex-direction: column; padding: 2.5rem; box-shadow: 0 20px 50px rgba(0,0,0,0.05); }
        .card-front { background: white; border: 1px solid #e2e8f0; align-items: center; justify-content: center; }
        .card-back { background: #ffffff; border: 1px solid #e2e8f0; transform: rotateY(180deg); overflow-y: auto; padding: 2rem; }
        .srs-btn { transition: all 0.2s; font-weight: 900; height: 3.8rem; border-radius: 1.25rem; border: 2px solid transparent; font-size: 0.95rem; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px; }
        .btn-again { border-color: #fee2e2; color: #dc2626; background: #fff5f5; }
        .btn-hard { border-color: #ffedd5; color: #d97706; background: #fffafb; }
        .btn-good { border-color: #dcfce7; color: #16a34a; background: #f0fdf4; }
        .btn-easy { border-color: #dbeafe; color: #2563eb; background: #eff6ff; }
        .info-label { font-size: 0.6rem; font-weight: 900; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.1rem; }
        .content-box { border-radius: 1rem; padding: 0.75rem 1rem; margin-bottom: 0.75rem; width: 100%; text-align: left; border-left: 4px solid #e2e8f0; line-height: 1.4; }
        .box-def { background: #f5f3ff; border-left-color: #6366f1; }
        .box-col { background: #fffbeb; border-left-color: #f59e0b; }
        .box-exam { background: #f0f9ff; border-left-color: #0ea5e9; }
        .progress-indicator { height: 8px; background: #e2e8f0; border-radius: 4px; overflow: hidden; flex-grow: 1; margin: 0 1rem; }
        .progress-fill { height: 100%; background: linear-gradient(90deg, #6366f1, #10b981); transition: width 0.5s ease; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
        .btn-icon { width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; border-radius: 10px; background: #f1f5f9; transition: all 0.2s; }
        .btn-icon:hover { background: #e2e8f0; transform: scale(1.1); }
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
                const [currIdx, setCurrIdx] = useState(0); 
                const [isFlipped, setIsFlipped] = useState(false);
                const [lvlFilter, setLvlFilter] = useState('all'); 
                const [prefixFilter, setPrefixFilter] = useState('');
                const [limit, setLimit] = useState(20);
                const [stats, setStats] = useState({ again: 0, hard: 0, good: 0, easy: 0 });
                const [totalInitial, setTotalInitial] = useState(0);
                const [speechRate, setSpeechRate] = useState(0.9);
                const [isSoundOn, setIsSoundOn] = useState(true);
                const [showInfo, setShowInfo] = useState(false);

                // 持久化加載
                useEffect(() => {
                    const saved = localStorage.getItem('vocab_master_gold_save');
                    if (saved) {
                        const data = JSON.parse(saved);
                        setQuizList(data.quizList); setStats(data.stats); setTotalInitial(data.totalInitial); 
                        setLvlFilter(data.lvlFilter); setSpeechRate(data.speechRate || 0.9); setView('quiz');
                    }
                }, []);

                // 自動存檔
                useEffect(() => {
                    if (view === 'quiz') {
                        localStorage.setItem('vocab_master_gold_save', JSON.stringify({ quizList, stats, totalInitial, lvlFilter, speechRate }));
                    }
                }, [quizList, stats, speechRate]);

                const speak = (t) => {
                    if (!isSoundOn) return;
                    window.speechSynthesis.cancel();
                    const u = new SpeechSynthesisUtterance(t);
                    u.lang = 'en-US'; u.rate = speechRate;
                    window.speechSynthesis.speak(u);
                };

                // 分流器：正面自動朗讀單字，背面自動朗讀例句
                useEffect(() => {
                    if (view === 'quiz' && quizList.length > 0) {
                        const curr = quizList[0];
                        if (!isFlipped) speak(curr.word || curr.w);
                        else if (curr.example || curr.e) speak(curr.example || curr.e);
                    }
                }, [quizList, isFlipped, view]);

                const startQuiz = () => {
                    let filtered = [...db];
                    if (lvlFilter !== 'all') filtered = filtered.filter(i => String(i.l) === lvlFilter);
                    if (prefixFilter) filtered = filtered.filter(i => (i.word || i.w || "").toLowerCase().startsWith(prefixFilter.toLowerCase()));
                    const shuffled = filtered.sort(() => Math.random() - 0.5).slice(0, parseInt(limit));
                    setQuizList(shuffled); setTotalInitial(shuffled.length); setStats({ again: 0, hard: 0, good: 0, easy: 0 });
                    setView('quiz'); setIsFlipped(false);
                };

                const handleSRS = (type) => {
                    let newList = [...quizList];
                    const curr = newList.shift(); // 移除目前的
                    setStats(prev => ({ ...prev, [type]: prev[type] + 1 }));

                    if (type === 'again') newList.splice(1, 0, curr); // 插到第 2 位
                    else if (type === 'hard') newList.splice(4, 0, curr); // 插到第 5 位
                    else if (type === 'good') newList.push(curr); // 丟到最後
                    // easy 則直接不放回去

                    if (newList.length === 0) { setView('result'); localStorage.removeItem('vocab_master_gold_save'); }
                    else { setQuizList(newList); setIsFlipped(false); }
                };

                const resetAll = () => {
                    localStorage.removeItem('vocab_master_gold_save');
                    window.location.reload();
                };

                const handleFileUpload = (e) => {
                    const file = e.target.files[0];
                    if (!file) return;
                    const reader = new FileReader();
                    reader.onload = (ev) => {
                        try {
                            const data = JSON.parse(ev.target.result);
                            setDb(data); alert("檔案載入成功，共 " + data.length + " 筆記錄");
                        } catch(err) { alert("JSON 格式錯誤"); }
                    };
                    reader.readAsText(file);
                };

                // 快捷鍵
                useEffect(() => {
                    const handleKey = (e) => {
                        if (view !== 'quiz') return;
                        if (e.code === 'Space') { e.preventDefault(); setIsFlipped(f => !f); }
                        else if (isFlipped && e.key === '1') handleSRS('again');
                        else if (isFlipped && e.key === '2') handleSRS('hard');
                        else if (isFlipped && e.key === '3') handleSRS('good');
                        else if (isFlipped && e.key === '4') handleSRS('easy');
                        else if (e.key === 'i') setShowInfo(v => !v);
                        else if (e.key === 'Enter') {
                            const curr = quizList[0];
                            if (!isFlipped) speak(curr.word || curr.w);
                            else speak(curr.example || curr.e);
                        }
                    };
                    window.addEventListener('keydown', handleKey);
                    return () => window.removeEventListener('keydown', handleKey);
                }, [view, isFlipped, quizList]);

                if (view === 'home') return h('div', { className: "flex flex-col items-center justify-center min-h-screen p-6" },
                    h('div', { className: "glass max-w-sm w-full rounded-[3.5rem] p-12 text-center" },
                        h('div', { className: "w-20 h-20 bg-indigo-600 rounded-3xl mx-auto mb-8 flex items-center justify-center shadow-lg" }, h('span', { className: "text-white text-4xl font-black" }, "E")),
                        h('h1', { className: "text-4xl font-black mb-8" }, "英文究極金牌"),
                        h('div', { className: "space-y-4" },
                            h('button', { onClick: () => setView('setup'), className: "w-full py-5 rounded-[2rem] bg-indigo-600 text-white font-black text-lg" }, "新練習"),
                            h('a', { href: 'entry.html', className: "block mt-4 text-slate-400 font-bold" }, "← 返回入口")
                        )
                    )
                );

                if (view === 'setup') return h('div', { className: "flex flex-col items-center justify-center min-h-screen p-6" },
                    h('div', { className: "glass max-w-sm w-full rounded-[3rem] p-10" },
                        h('h2', { className: "text-2xl font-black mb-8 text-center" }, "練習設定"),
                        h('div', { className: "mb-6" }, h('label', { className: "info-label" }, "等級"), h('select', { value: lvlFilter, onChange: e => setLvlFilter(e.target.value), className: "w-full p-4 rounded-2xl bg-white border font-bold" }, h('option', { value: 'all' }, "全部"), [1,2,3,4,5,6].map(l => h('option', { key: l, value: l }, "Level " + l)))),
                        h('div', { className: "mb-6" }, h('label', { className: "info-label" }, "字首篩選"), h('input', { value: prefixFilter, onChange: e => setPrefixFilter(e.target.value), placeholder: "例: a", className: "w-full p-4 rounded-2xl bg-white border font-bold" })),
                        h('div', { className: "mb-10" }, h('div', { className: "flex justify-between" }, h('label', { className: "info-label" }, "題數"), h('span', { className: "font-black" }, limit)), h('input', { type: 'range', min: 5, max: 200, step: 5, value: limit, onChange: e => setLimit(e.target.value), className: "w-full accent-indigo-600" })),
                        h('button', { onClick: startQuiz, className: "w-full py-5 bg-indigo-600 text-white rounded-[2rem] font-black" }, "開始"),
                        h('button', { onClick: () => setView('home'), className: "w-full mt-4 text-slate-400 font-bold" }, "取消")
                    )
                );

                if (view === 'quiz') {
                    const curr = quizList[0];
                    const progress = ((totalInitial - quizList.length) / totalInitial) * 100;
                    
                    return h('div', { className: "flex flex-col items-center min-h-screen p-4 pt-8" },
                        // 一體化資訊欄
                        h('div', { className: "w-full max-w-4xl flex items-center justify-between gap-4 mb-8" },
                            h('button', { onClick: resetAll, className: "btn-icon" }, "🏠"),
                            h('div', { className: "progress-indicator" }, h('div', { className: "progress-fill", style: { width: progress + "%" } })),
                            h('div', { className: "flex items-center gap-4 text-xs font-black text-slate-400" },
                                h('span', { className: "text-indigo-600" }, (totalInitial - quizList.length + 1) + " / " + totalInitial),
                                h('div', { className: "flex gap-2" },
                                    h('span', { className: "text-red-400" }, "A: " + stats.again),
                                    h('span', { className: "text-amber-400" }, "H: " + stats.hard),
                                    h('span', { className: "text-emerald-400" }, "G: " + stats.good),
                                    h('span', { className: "text-blue-400" }, "E: " + stats.easy)
                                )
                            ),
                            h('button', { onClick: () => setShowInfo(!showInfo), className: "btn-icon" }, "ℹ️"),
                            h('label', { className: "btn-icon cursor-pointer" }, "📁", h('input', { type: 'file', hidden: true, onChange: handleFileUpload }))
                        ),

                        showInfo && h('div', { className: "w-full max-w-md bg-slate-900 text-white p-6 rounded-3xl mb-6 text-sm" },
                            h('h4', { className: "font-black mb-4" }, "快捷鍵說明"),
                            h('p', null, "Space: 翻面"),
                            h('p', null, "1 - 4: SRS 分類"),
                            h('p', null, "Enter: 再次朗讀"),
                            h('p', null, "i: 開關此說明")
                        ),

                        // 卡片主體
                        h('div', { className: "card-container mb-2" },
                            h('div', { className: "card " + (isFlipped ? "is-flipped" : ""), onClick: () => setIsFlipped(!isFlipped) },
                                h('div', { className: "card-face card-front" },
                                    h('div', { className: "flex flex-col items-center gap-6" },
                                        h('h2', { className: "text-6xl font-black tracking-tight" }, curr.word || curr.w),
                                        h('button', { onClick: (e) => { e.stopPropagation(); speak(curr.word || curr.w); }, className: "w-16 h-16 bg-slate-50 rounded-2xl flex items-center justify-center text-3xl" }, "🔊")
                                    )
                                ),
                                h('div', { className: "card-face card-back" },
                                    h('div', { className: "flex justify-between items-start mb-4" },
                                        h('div', null, h('p', { className: "text-indigo-600 font-black text-2xl" }, curr.word || curr.w), h('p', { className: "text-slate-400 font-bold" }, curr.p || "")),
                                        h('button', { onClick: (e) => { e.stopPropagation(); speak(curr.example || curr.e); }, className: "btn-icon text-xl" }, "🔊")
                                    ),
                                    h('div', { className: "content-box box-def" }, h('label', { className: "info-label" }, "解釋 DEFINITION"), h('p', { className: "text-lg font-black" }, curr.definition || curr.d || "")),
                                    (curr.collocation || curr.c) && h('div', { className: "content-box box-col" }, h('label', { className: "info-label" }, "搭配 COLLOCATION"), h('p', { className: "text-sm font-bold" }, curr.collocation || curr.c)),
                                    (curr.example || curr.e) && h('div', { className: "content-box box-exam" }, h('label', { className: "info-label" }, "例句 SENTENCE"), h('p', { className: "text-sm font-medium leading-relaxed" }, curr.example || curr.e))
                                )
                            )
                        ),

                        // 音量與語速控制
                        h('div', { className: "w-full max-w-md flex items-center gap-4 px-6 mb-8" },
                            h('button', { onClick: () => setIsSoundOn(!isSoundOn), className: "text-2xl" }, isSoundOn ? "🔊" : "🔇"),
                            h('input', { type: 'range', min: 0.5, max: 1.5, step: 0.1, value: speechRate, onChange: e => setSpeechRate(parseFloat(e.target.value)), className: "flex-grow h-1.5 accent-indigo-600" }),
                            h('span', { className: "text-[10px] font-black text-slate-400 w-8" }, speechRate + "x")
                        ),

                        // SRS 按鈕
                        isFlipped && h('div', { className: "grid grid-cols-4 gap-3 w-full max-w-lg mb-8" },
                            ['Again', 'Hard', 'Good', 'Easy'].map((b, i) => h('button', { key: i, onClick: (e) => { e.stopPropagation(); handleSRS(b.toLowerCase()); }, className: `srs-btn btn-${b.toLowerCase()}` }, 
                                h('span', null, b), h('span', { className: "text-[10px] opacity-60" }, i + 1)
                            ))
                        )
                    );
                }

                if (view === 'result') return h('div', { className: "flex flex-col items-center justify-center min-h-screen p-6" },
                    h('div', { className: "glass max-w-sm w-full rounded-[3.5rem] p-12 text-center" }, h('h3', { className: "text-3xl font-black mb-10" }, "挑戰完成"), h('button', { onClick: resetAll, className: "w-full py-5 bg-indigo-600 text-white rounded-3xl font-black" }, "重新開始"))
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
