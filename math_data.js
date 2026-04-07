const MATH_DB = [
    // === 七年級上學期 ===
    // 第一章：數與量
    {"w": "整數的加減法：同號數相加？", "d": "取其共同性質符號，再將其絕對值相加。", "l": "7上", "v": "https://www.youtube.com/watch?v=4BhVJ0uKW58", "c": "1"},
    {"w": "整數的乘除法：異號數相乘？", "d": "結果必為負數 (負號)。", "l": "7上", "v": "https://www.youtube.com/watch?v=dgcP3P6pdRQ", "c": "1"},
    {"w": "$a$ 的絕對值 $|a|$ 的幾何意義？", "d": "點 $a$ 到原點的「距離」。", "l": "7上", "v": "https://www.youtube.com/watch?v=cpqjUlP9YPo", "c": "1"},
    {"w": "數線上 $A(a)$ 與 $B(b)$ 兩點間的距離公式？", "d": "$\\overline{AB} = |a - b|$", "l": "7上", "v": "https://www.youtube.com/watch?v=cpqjUlP9YPo", "c": "1"},
    {"w": "指數律：底數相同相乘時，指數該如何運算？", "d": "指數相加（即 $a^m \\times a^n = a^{m+n}$）。", "l": "7上", "v": "https://www.youtube.com/watch?v=UdROW9PkWnY", "c": "1"},
    {"w": "科學記號 (Scientific Notation) 的格式？", "d": "$a \\times 10^n$ (其中 $1 \\le |a| < 10$，$n$ 為整數)", "l": "7上", "v": "https://www.youtube.com/watch?v=QJ_ir5UPgwc", "c": "1"},
    
    // 第二章：因數與倍數、分數的運算
    {"w": "因數 (Factor) 的定義？", "d": "若整數 $a$ 能被整數 $b$ 整除，則 $b$ 為 $a$ 的因數。", "l": "7上", "v": "https://www.youtube.com/watch?v=caWwZMiy098", "c": "2"},
    {"w": "質數 (Prime Number) 的定義？", "d": "大於 1 的整數中，除了 1 和本身以外沒有其他因數的數。", "l": "7上", "v": "https://www.youtube.com/watch?v=iRxc1BFg8_c", "c": "2"},
    {"w": "標準分解式 (Prime Factorization)？", "d": "將一個合數表示成其質因數乘積的形式，且從小排到大。", "l": "7上", "v": "https://www.youtube.com/watch?v=iRxc1BFg8_c", "c": "2"},
    {"w": "最大公因數 (GCD) 的符號標示？", "d": "$(a, b)$", "l": "7上", "v": "https://www.youtube.com/watch?v=Pr-kEa9mOdI", "c": "2"},
    {"w": "最小公倍數 (LCM) 的符號標示？", "d": "$[a, b]$", "l": "7上", "v": "https://www.youtube.com/watch?v=b-bAM4FRz9k", "c": "2"},
    {"w": "分數的加減：分母不同時該如何處理？", "d": "先找到分母的最小公倍數進行通分，再相加減。", "l": "7上", "v": "https://www.youtube.com/watch?v=vajHikZXuH0", "c": "2"},
    {"w": "分數的乘法：$\\frac{a}{b} \\times \\frac{c}{d} = ?$", "d": "$\\frac{a \\times c}{b \\times d}$", "l": "7上", "v": "https://www.youtube.com/watch?v=wx4ia3YovX8", "c": "2"},
    {"w": "分數的除法：$\\frac{a}{b} \\div \\frac{c}{d} = ?$", "d": "$\\frac{a}{b} \\times \\frac{d}{c}$ (乘以倒數)", "l": "7上", "v": "https://www.youtube.com/watch?v=VHqFlPCaQL4", "c": "2"},

    // 第三章：一元一次方程式
    {"w": "一元一次方程式的定義？", "d": "只有一個未知數，且該未知數的最高次數為 1 的等式。", "l": "7上", "v": "https://www.youtube.com/watch?v=iBedXmNFnSk", "c": "3"},
    {"w": "等量公理 (Addition/Multiplication Property)？", "d": "等式兩邊同時加、減、乘、除同一個數（除數不為0），等式仍成立。", "l": "7上", "v": "https://www.youtube.com/watch?v=PIfRMUzEM0k", "c": "3"},
    {"w": "解方程式的「移項法則」？", "d": "加變減、減變加、乘變除、除變乘。", "l": "7上", "v": "https://www.youtube.com/watch?v=tG4El1Fkvkg", "c": "3"},

    // 第四章：線對稱圖形與三視圖
    {"w": "線對稱圖形的特性？", "d": "沿著對稱軸摺疊，兩側的圖形能夠完全重合。", "l": "7上", "v": "https://www.youtube.com/watch?v=qtrmfjU1zgU", "c": "4"},
    {"w": "幾何三視圖 (Three-view drawing) 包含哪三個面向？", "d": "前視圖、上視圖、右視圖(側視)。", "l": "7上", "v": "https://www.youtube.com/watch?v=JO69mU3d5CM", "c": "4"},

    // === 七年級下學期 ===
    // 第一章：二元一次聯立方程式
    {"w": "二元一次聯立方程式的解法？", "d": "代入消去法、加減消去法。", "l": "7下", "v": "https://www.youtube.com/watch?v=XuV2OO7ppfQ", "c": "1"},
    {"w": "找出聯立方程式唯一解的幾何意義？", "d": "兩條直線在座標平面上的交點。", "l": "7下", "v": "https://www.youtube.com/watch?v=XuV2OO7ppfQ", "c": "1"},

    // 第二章：坐標幾何
    {"w": "直角坐標平面的四個象限？", "d": "右上(I), 左上(II), 左下(III), 右下(IV)。", "l": "7下", "v": "https://www.youtube.com/watch?v=HX8qfjpWSak", "c": "2"},
    {"w": "二元一次方程式的圖形 $ax + by = c$？", "d": "在一平面的直角座標系中，其圖形為一條「直線」。", "l": "7下", "v": "https://www.youtube.com/watch?v=VjV8suevpkk", "c": "2"},
    {"w": "線型函數 (Linear Function) 的一般式？", "d": "$y = ax + b$ (a為斜率, b為y軸截距)", "l": "7下", "v": "https://www.youtube.com/watch?v=dS3zCJ_7oyo", "c": "2"},

    // 第三章：比與比例式
    {"w": "比 (Ratio) 與比值？", "d": "$a:b$ 的比值為 $\\frac{a}{b}$ ($b \\neq 0$ )。", "l": "7下", "v": "https://www.youtube.com/watch?v=bm8fKqgC5yo", "c": "3"},
    {"w": "連比例式？", "d": "若 $x:y:z = a:b:c$，則可設 $x=ak, y=bk, z=ck$ ($k$ 為常數)。", "l": "7下", "v": "https://www.youtube.com/watch?v=kGOMzzQ92TQ", "c": "3"},
    {"w": "正比與反比的區別？", "d": "正比為 $y=kx$，反比為 $xy=k$ ($k$ 不為0)。", "l": "7下", "v": "https://www.youtube.com/watch?v=sup0FFNP6cQ", "c": "3"},

    // 第四章：一元一次不等式
    {"w": "一元一次不等式的解在數線上的表示？", "d": "大於(>)向右畫圓圈排除，小於(<)向左畫圓圈排除；包含等號為實心點。", "l": "7下", "v": "https://www.youtube.com/watch?v=lTkf6toho9k", "c": "4"},
    {"w": "不等式的性質：同乘除負數？", "d": "不等號的方向必須「改變」(反向)。", "l": "7下", "v": "https://www.youtube.com/watch?v=lTkf6toho9k", "c": "4"},

    // 第五、六章：資料與不確定性
    {"w": "統計圖表的平均數、中位數、眾數？", "d": "平均為總和除以個數；中位數為排序後中間數；眾數為出現次數最多者。", "l": "7下", "v": "https://www.youtube.com/watch?v=jWJoLALDMSE", "c": "4"},

    // === 八年級上學期 ===
    // 第一章：乘法公式與多項式
    {"w": "和平方公式 $(a+b)^2 = ?$", "d": "$a^2 + 2ab + b^2$", "l": "8上", "v": "https://www.youtube.com/watch?v=i9T-sAozHdE", "c": "1"},
    {"w": "差平方公式 $(a-b)^2 = ?$", "d": "$a^2 - 2ab + b^2$", "l": "8上", "v": "https://www.youtube.com/watch?v=BZ2IkxJ2hHE", "c": "1"},
    {"w": "平方差公式 $(a+b)(a-b) = ?$", "d": "$a^2 - b^2$", "l": "8上", "v": "https://www.youtube.com/watch?v=i9T-sAozHdE", "c": "1"},
    {"w": "多項式相加減時，必須針對什麼進行合併？", "d": "同類項（即變數及其次方相同的項）。", "l": "8上", "v": "https://www.youtube.com/watch?v=9QQs-YPbNTw", "c": "1"},

    // 第二章：平方根與畢氏定理
    {"w": "若 $x^2 = a$ ($a \\ge 0$)，則 $x$ 稱為 $a$ 的？", "d": "平方根 ($\\pm\\sqrt{a}$)", "l": "8上", "v": "https://www.youtube.com/watch?v=3ifyPKtfEFE", "c": "2"},
    {"w": "根式的最簡式定義為何？", "d": "根號內的數不能有完全平方數的因數，且分母不能有根號。", "l": "8上", "v": "https://www.youtube.com/watch?v=XzrJDW-u1r4", "c": "2"},
    {"w": "勾股定理 (畢氏定理) 公式？", "d": "$a^2 + b^2 = c^2$ ($c$ 為斜邊)", "l": "8上", "v": "https://www.youtube.com/watch?v=C3N4EuSMlRg", "c": "2"},

    // 第三章：因式分解
    {"w": "因式分解 (Factorization) 的定義？", "d": "將一個多項式寫成多個多項式乘積的過程。", "l": "8上", "v": "https://www.youtube.com/watch?v=qlanMNYt7-0", "c": "3"},
    {"w": "提公因式法？", "d": "利用分配律的逆運算，將各項公有的因式提到括號外。", "l": "8上", "v": "https://www.youtube.com/watch?v=qlanMNYt7-0", "c": "3"},
    {"w": "十字交乘法 (Cross Multiplication)？", "d": "利用係數配對來分解二次三項式的方法。", "l": "8上", "v": "https://www.youtube.com/watch?v=ND1AasNJeb0", "c": "3"},

    // 第四章：一元二次方程式
    {"w": "一元二次方程式 $ax^2 + bx + c = 0$ 的求根公式 (公式解)？", "d": "$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$", "l": "8上", "v": "https://www.youtube.com/watch?v=htFRiHE_T4k", "c": "4"},
    {"w": "一元二次方程式的判別式 $D = ?$", "d": "$b^2 - 4ac$ (D>0 兩相異實根, D=0 重根, D<0 無實根)", "l": "8上", "v": "https://www.youtube.com/watch?v=74F92Yv3VG4", "c": "4"},
    {"w": "解一元二次方程式的配方法？", "d": "將式子配成 $(x+p)^2 = q$ 的形式，再開平方求解。", "l": "8上", "v": "https://www.youtube.com/watch?v=opZx_8_9l7g", "c": "4"},

    // === 八年級下學期 ===
    // 第一章：數列與等差級數
    {"w": "等差數列第 $n$ 項公式 $a_n = ?$", "d": "$a_1 + (n-1)d$", "l": "8下", "v": "https://www.youtube.com/watch?v=lfJWT8fQ524", "c": "1"},
    {"w": "等比數列 (Geometric Progression)？", "d": "後項除以前項的比值 (公比 $r$) 為定值的數列。", "l": "8下", "v": "https://www.youtube.com/watch?v=OYguKswWamM", "c": "1"},
    {"w": "等差級數前 $n$ 項和公式 $S_n = ?$", "d": "$S_n = \\frac{n(a_1 + a_n)}{2}$ 或 $\\frac{n[2a_1 + (n-1)d]}{2}$", "l": "8下", "v": "https://www.youtube.com/watch?v=0q2fKebbvPc", "c": "1"},

    // 第二章：函數及其圖形
    {"w": "函數 (Function) 的基礎判斷法則？", "d": "每一個 x 值只能對應到唯一的 y 值 (一對一或多對一，不能一對多)。", "l": "8下", "v": "https://www.youtube.com/watch?v=OphdL0gixWM", "c": "2"},
    {"w": "常數函數 (Constant Function)？", "d": "$y = k$ (其圖形為一條水平線)。", "l": "8下", "v": "https://www.youtube.com/watch?v=57UeKsNc-ew", "c": "2"},

    // 第三章：三角形的性質
    { "w": "三角形的內角和與外角和？", "d": "內角和 $180^\circ$，外角和 $360^\circ$。", "l": "8下", "c": "3", "v": "https://www.youtube.com/watch?v=wS5las4myVg", "v_chap": "3-1" },
    {"w": "尺規作圖 (Straightedge and Compass Construction) 限定工具？", "d": "沒有刻度的直尺、圓規。", "l": "8下", "v": "https://www.youtube.com/watch?v=Bh7NZrc_aBY", "c": "3"},
    {"w": "何謂樞紐定理（夾角與對邊的關係）？", "d": "兩三角形若有兩邊對應相等，則夾角越大者，其對邊越長。", "l": "8下", "v": "https://www.youtube.com/watch?v=K3cmCVmPjEI", "c": "3"},
    {"w": "三角形全等性質有哪幾種？", "d": "SSS、SAS、ASA、AAS、RHS。", "l": "8下", "v": "https://www.youtube.com/watch?v=A0IH4ICiMlo", "c": "3"},

    // 第四章：平行與四邊形
    {"w": "平行線的性質：內錯角？", "d": "若兩平行線被一直線所截，則其「內錯角相等」。", "l": "8下", "v": "https://www.youtube.com/watch?v=dbdpJSvzimI", "c": "4"},
    {"w": "平行四邊形的判定條件？", "d": "對邊互相平行、對角相等、對角線互相平分（任一成立即可）。", "l": "8下", "v": "https://www.youtube.com/watch?v=8nMUDggdH1Q", "c": "4"},
    {"w": "梯形、菱形、箏形等特殊四邊形的對角線特性？", "d": "菱形與箏形對角線互相垂直，矩形對角線等長且互相平分。", "l": "8下", "v": "https://www.youtube.com/watch?v=VDyhBxM_wq0", "c": "4"},

    // === 九年級上學期 === (由於該頻道未列專屬影片，保留原題庫觀念，無YT連結)
    // 第一章：幾何
    {"w": "相似三角形對應邊與面積比的關係？", "d": "面積比等於「對應邊長的平方比」。", "l": "9上", "c": "1"},
    {"w": "相似三角形的判定性質？", "d": "$AA/SAS/SSS$ 相似性質。", "l": "9上", "c": "1"},
    {"w": "比例線段性質？", "d": "平行三角形一邊的直線，截其餘兩邊成「比例線段」。", "l": "9上", "c": "1"},
    {"w": "直角三角形中 $\\sin \\theta$ 的定義？", "d": "$\\frac{\\text{對邊}}{\\text{斜邊}}$", "l": "9上", "c": "1"},

    // 第二章：幾何
    {"w": "圓心角與其所對弧的度數關係？", "d": "圓心角度數 = 所對弧的度數。", "l": "9上", "c": "2"},
    {"w": "圓與切線的性質？", "d": "圓心到切線的距離等於半徑，且半徑垂直於切點的切線。", "l": "9上", "c": "2"},
    {"w": "圓周角、弦切角性質？", "d": "圓周角 = 弦切角 = $\\frac{1}{2}$ 所對弧的度數。", "l": "9上", "c": "2"},

    // 第三章：幾何
    {"w": "三角形的「外心」 (O) 是哪三條線的交點？", "d": "三邊的「中垂線」交點 (到三頂點等距)。", "l": "9上", "c": "3"},
    {"w": "三角形的「內心」 (I) 是哪三條線的交點？", "d": "三個「內角平分線」交點 (到三邊等距)。", "l": "9上", "c": "3"},
    {"w": "三角形的「重心」 (G) 是哪三條線的交點？", "d": "三條「中線」的交點 (比例 $2:1$)。", "l": "9上", "c": "3"},

    // === 九年級下學期 ===
    // 第一章：二次函數
    {"w": "二次函數 $y = ax^2 + bx + c$ 的圖形為何？", "d": "一條「拋物線」 (a>0 向下凹/開口向上, a<0 向上凹/開口向下)。", "l": "9下", "v": "https://www.youtube.com/watch?v=eaiDyDX7MyI", "c": "1"},
    {"w": "二次函數 $y = ax^2+bx+c$ 中，當 $a > 0$ 時，圖形有極大值還是極小值？", "d": "有最低點（極小值），因為圖形開口向上。", "l": "9下", "v": "https://www.youtube.com/watch?v=q1xt_j8KghI", "c": "1"},
    
    // 第二章：統計與機率
    {"w": "中位數 (Median) 的定義？", "d": "將資料從小到大排列，處於中間位置的數組。", "l": "9下", "v": "https://www.youtube.com/watch?v=Rt7cdsSWQgM", "c": "2"},
    {"w": "一個標準的盒狀圖由哪五個重要的數值畫出？", "d": "最小值、第一四分位數(Q1)、中位數(Q2)、第三四分位數(Q3)、最大值。", "l": "9下", "v": "https://www.youtube.com/watch?v=Rt7cdsSWQgM", "c": "2"},
    {"w": "古典機率的公式 $P(A) = ?$", "d": "$\\frac{\\text{事件A的結果數}}{\\text{所有可能的結果總數}}$", "l": "9下", "v": "https://www.youtube.com/watch?v=hBVFyCgHbeY", "c": "2"},

    // 第三章：立體圖形
    {"w": "立體幾何圖形：角柱體積公式？", "d": "底面積 $\\times$ 高", "l": "9下", "v": "https://www.youtube.com/watch?v=2bhJXM1cqek", "c": "3"},
    {"w": "立體幾何圖形：圓/角錐體積公式？", "d": "$\\frac{1}{3} \\times \\text{底面積} \\times \\text{高}$", "l": "9下", "v": "https://www.youtube.com/watch?v=rbkZT0oILQY", "c": "3"}
];
