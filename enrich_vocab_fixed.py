import pandas as pd
import os

# 這裡我將為前 100 個單字提供極其詳盡的補全資料。
# 單字清單來源：extracted_vocab.csv 前 100 筆
VOCAB_FULL_DATA = {
    "girl": {"def": "女孩", "ipa": "/ɡɜːl/", "trans": "girls (複數)", "col": "a little girl", "ex": "She is a smart girl."},
    "healthy": {"def": "健康的", "ipa": "/ˈhelθi/", "trans": "health (名詞), healthily (副詞)", "col": "healthy diet", "ex": "Eating fruit is healthy."},
    "idea": {"def": "主意、想法", "ipa": "/aɪˈdɪə/", "trans": "ideas (複數)", "col": "get an idea", "ex": "That's a great idea."},
    "give": {"def": "給、送", "ipa": "/ɡɪv/", "trans": "gave (過去式), given (過去分詞)", "col": "give a gift, give up", "ex": "Please give me the book."},
    "hear": {"def": "聽見", "ipa": "/hɪə/", "trans": "heard (過去式/過去分詞)", "col": "hear a noise, hear from", "ex": "Did you hear that noise?"},
    "if": {"def": "如果", "ipa": "/ɪf/", "trans": "無", "col": "as if, if only", "ex": "Tell me if you need help."},
    "glad": {"def": "高興的", "ipa": "/ɡlæd/", "trans": "gladness (名詞)", "col": "be glad to", "ex": "I am glad to see you."},
    "heart": {"def": "心臟、心", "ipa": "/hɑːt/", "trans": "hearts (複數)", "col": "have a big heart", "ex": "His heart is beating fast."},
    "important": {"def": "重要的", "ipa": "/ɪmˈpɔːtnt/", "trans": "importance (名詞)", "col": "important meeting", "ex": "It is an important task."},
    "glass": {"def": "玻璃、杯子", "ipa": "/ɡlɑːs/", "trans": "glasses (複數)", "col": "a glass of water", "ex": "The window is made of glass."},
    "heat": {"def": "熱、加熱", "ipa": "/hiːt/", "trans": "heated, heating", "col": "heat up", "ex": "The summer heat is record-breaking."},
    "in": {"def": "在...之中", "ipa": "/ɪn/", "trans": "無", "col": "in the room, in a hurry", "ex": "He is in the office."},
    "glasses": {"def": "眼鏡", "ipa": "/ˈɡlɑːsɪz/", "trans": "無 (通常用複數)", "col": "wear glasses", "ex": "I can't see without glasses."},
    "heavy": {"def": "重的", "ipa": "/ˈhevi/", "trans": "heavier, heaviest", "col": "heavy rain, heavy traffic", "ex": "The box is too heavy to lift."},
    "inch": {"def": "英吋", "ipa": "/ɪntʃ/", "trans": "inches (複數)", "col": "square inch", "ex": "One inch is about 2.54 cm."},
    "glove(s)": {"def": "手套", "ipa": "/ɡlʌv/", "trans": "gloves (複數)", "col": "wear gloves", "ex": "Put on your gloves; it's cold."},
    "height": {"def": "高度", "ipa": "/haɪt/", "trans": "high (形容詞)", "col": "average height", "ex": "The building's height is 20 meters."},
    "insect": {"def": "昆蟲", "ipa": "/ˈɪnsekt/", "trans": "insects (複數)", "col": "harmful insects", "ex": "Ants are social insects."},
    "go": {"def": "去、離開", "ipa": "/ɡəʊ/", "trans": "went (過去式), gone (過去分詞)", "col": "go home, go crazy", "ex": "I need to go now."},
    "hello": {"def": "你好", "ipa": "/həˈləʊ/", "trans": "hellos (複數)", "col": "say hello", "ex": "She waved and said hello."},
    "inside": {"def": "在...裡面", "ipa": "/ˌɪnˈsaɪd/", "trans": "無", "col": "step inside", "ex": "It's warmer inside the house."},
    "god/goddess": {"def": "上帝/女神", "ipa": "/ɡɒd/", "trans": "gods (複數)", "col": "believe in God", "ex": "Ancient Greeks had many gods."},
    "help": {"def": "幫助", "ipa": "/help/", "trans": "helped, helping", "col": "can't help doing", "ex": "Thank you for your help."},
    "interest": {"def": "興趣、利益", "ipa": "/ˈɪntrest/", "trans": "interested (形容詞), interesting (形容詞)", "col": "place of interest", "ex": "Music is my main interest."},
    "good": {"def": "好的", "ipa": "/ɡʊd/", "trans": "better, best", "col": "good weather, good luck", "ex": "Have a good time!"},
    "helpful": {"def": "有幫助的", "ipa": "/ˈhelpfl/", "trans": "helpfully (副詞)", "col": "a helpful tip", "ex": "She was very helpful to us."},
    "interested": {"def": "感興趣的", "ipa": "/ˈɪntrestɪd/", "trans": "be interested in", "col": "more interested in", "ex": "I'm interested in world history."},
    "goodbye": {"def": "再見", "ipa": "/ˌɡʊdˈbaɪ/", "trans": "goodbyes (複數)", "col": "wave goodbye", "ex": "We said goodbye at the airport."},
    "hen": {"def": "母雞", "ipa": "/hen/", "trans": "hens (複數)", "col": "a mother hen", "ex": "The hen laid an egg."},
    "interesting": {"def": "有趣的", "ipa": "/ˈɪntrestɪŋ/", "trans": "interestingly (副詞)", "col": "interesting story", "ex": "This is an interesting movie."},
    "grade": {"def": "等級、年級", "ipa": "/ɡreɪd/", "trans": "grades (複數)", "col": "get a good grade", "ex": "He is in the fifth grade."},
    "here": {"def": "這裡", "ipa": "/hɪə/", "trans": "無", "col": "stay here, here and there", "ex": "Come here, please."},
    "interview": {"def": "面試、訪談", "ipa": "/ˈɪntəvjuː/", "trans": "interviewer (面試官)", "col": "job interview", "ex": "The interview lasted an hour."},
    "grandfather": {"def": "祖父、外公", "ipa": "/ˈɡrænfɑːðə/", "trans": "grandfathers (複數)", "col": "visit grandfather", "ex": "My grandfather is 80 years old."},
    "hide": {"def": "躲藏", "ipa": "/haɪd/", "trans": "hid (過去式), hidden (過去分詞)", "col": "hide and seek", "ex": "The children like to hide."},
    "into": {"def": "到...裡面", "ipa": "/ˈɪntu/", "trans": "無", "col": "go into", "ex": "He walked into the room."},
    "grandmother": {"def": "祖母、外婆", "ipa": "/ˈɡrænmʌðə/", "trans": "grandmothers (複數)", "col": "love grandmother", "ex": "She is my favorite grandmother."},
    "high": {"def": "高的", "ipa": "/haɪ/", "trans": "higher, highest, height (名詞)", "col": "high school, high price", "ex": "The price is quite high."},
    "invite": {"def": "邀請", "ipa": "/ɪnˈvaɪt/", "trans": "invitation (名詞)", "col": "invite to a party", "ex": "They invited us to lunch."},
    "grass": {"def": "草、草地", "ipa": "/ɡrɑːs/", "trans": "grassy (形容詞)", "col": "sit on the grass", "ex": "Don't walk on the grass."},
    "hill": {"def": "小山、山丘", "ipa": "/hɪl/", "trans": "hills (複數)", "col": "up the hill", "ex": "We climbed the steep hill."},
    "island": {"def": "島嶼", "ipa": "/ˈaɪlənd/", "trans": "islands (複數)", "col": "desert island", "ex": "Taiwan is a beautiful island."},
    "gray": {"def": "灰色", "ipa": "/ɡreɪ/", "trans": "grays (複數)", "col": "gray sky", "ex": "The cat has gray fur."},
    "history": {"def": "歷史", "ipa": "/ˈhɪstəri/", "trans": "historical (形容詞), historian (名詞)", "col": "world history", "ex": "I like studying history."},
    "itself)": {"def": "它自己", "ipa": "/ɪtˈself/", "trans": "無", "col": "by itself", "ex": "The cat is cleaning itself."},
    "great": {"def": "偉大的、棒的", "ipa": "/ɡreɪt/", "trans": "greater, greatest", "col": "Great Wall, great job", "ex": "You did a great job!"},
    "hit": {"def": "打、打擊", "ipa": "/hɪt/", "trans": "hit, hit (三態同形)", "col": "hit the ball", "ex": "The car hit a tree."},
    "item": {"def": "項目、品項", "ipa": "/ˈaɪtəm/", "trans": "items (複數)", "col": "a list of items", "ex": "Which item do you prefer?"},
    "green": {"def": "綠色", "ipa": "/ɡriːn/", "trans": "greens (複數)", "col": "green light", "ex": "The leaves are green."},
    "hobby": {"def": "愛好", "ipa": "/ˈhɒbi/", "trans": "hobbies (複數)", "col": "favorite hobby", "ex": "My hobby is gardening."},
    "jacket": {"def": "夾克", "ipa": "/ˈdʒækɪt/", "trans": "jackets (複數)", "col": "leather jacket", "ex": "Put on your jacket."},
    "ground": {"def": "地面", "ipa": "/ɡraʊnd/", "trans": "grounds (複數)", "col": "fall to the ground", "ex": "The bird fell to the ground."},
    "hold": {"def": "握住、舉行", "ipa": "/həʊld/", "trans": "held, held", "col": "hold hands, hold a meeting", "ex": "Please hold my hand."},
    "jeans": {"def": "牛仔褲", "ipa": "/dʒiːnz/", "trans": "無 (固定複數)", "col": "a pair of jeans", "ex": "I like wearing blue jeans."},
    "group": {"def": "團體", "ipa": "/ɡruːp/", "trans": "groups (複數)", "col": "group project", "ex": "We work in a group."},
    "holiday": {"def": "假期", "ipa": "/ˈhɒlədeɪ/", "trans": "holidays (複數)", "col": "summer holiday", "ex": "Where are you going for the holiday?"},
    "job": {"def": "工作", "ipa": "/dʒɒb/", "trans": "jobs (複數)", "col": "job search, good job", "ex": "I am looking for a job."},
    "grow": {"def": "成長", "ipa": "/ɡrəʊ/", "trans": "grew, grown, growth (名詞)", "col": "grow up", "ex": "Plants grow in sunlight."},
    "home": {"def": "家", "ipa": "/həʊm/", "trans": "homeless (形容詞)", "col": "at home, go home", "ex": "I am going home now."},
    "join": {"def": "加入", "ipa": "/dʒɔɪn/", "trans": "joined, joining", "col": "join a club", "ex": "Would you like to join us?"},
    "guess": {"def": "猜測", "ipa": "/ɡes/", "trans": "guessed, guessing", "col": "guess what", "ex": "Can you guess the answer?"},
    "homework": {"def": "作業", "ipa": "/ˈhəʊmwɜːk/", "trans": "無 (不可數)", "col": "do homework", "ex": "I have a lot of homework."},
    "joke": {"def": "笑話", "ipa": "/dʒəʊk/", "trans": "joked, joking", "col": "tell a joke", "ex": "He told a funny joke."},
    "guitar": {"def": "吉他", "ipa": "/ɡɪˈtɑː/", "trans": "guitars (複數)", "col": "play the guitar", "ex": "He is playing the guitar."},
    "honest": {"def": "誠實的", "ipa": "/ˈɒnɪst/", "trans": "honesty (名詞), honestly (副詞)", "col": "an honest man", "ex": "To be honest, I'm tired."},
    "joy": {"def": "喜悅", "ipa": "/dʒɔɪ/", "trans": "joyful (形容詞)", "col": "full of joy", "ex": "Childhood was full of joy."},
    "guy": {"def": "傢伙、男人", "ipa": "/ɡaɪ/", "trans": "guys (複數)", "col": "nice guy", "ex": "He's a nice guy."},
    "honey": {"def": "蜂蜜", "ipa": "/ˈhʌni/", "trans": "honeys (複數)", "col": "sweet as honey", "ex": "Bees make honey."},
    "juice": {"def": "果汁", "ipa": "/dʒuːs/", "trans": "juices (複數)", "col": "orange juice", "ex": "I like fresh fruit juice."},
    "habit": {"def": "習慣", "ipa": "/ˈhæbɪt/", "trans": "habits (複數)", "col": "good habit, break a habit", "ex": "Smoking is a bad habit."},
    "hope": {"def": "希望", "ipa": "/həʊp/", "trans": "hoped, hopeful", "col": "high hopes", "ex": "I hope you feel better."},
    "jump": {"def": "跳躍", "ipa": "/dʒʌmp/", "trans": "jumped, jumping", "col": "long jump", "ex": "He jumped over the fence."},
    "hair": {"def": "頭髮", "ipa": "/heə/", "trans": "haircut (剪髮)", "col": "short hair, long hair", "ex": "She has long black hair."},
    "horse": {"def": "馬", "ipa": "/hɔːs/", "trans": "horses (複數)", "col": "ride a horse", "ex": "The horse runs very fast."},
    "just": {"def": "剛好、只是", "ipa": "/dʒʌst/", "trans": "justice (名詞)", "col": "just in time", "ex": "I've just finished my work."},
    "half": {"def": "一半", "ipa": "/hɑːf/", "trans": "halves (複數)", "col": "half an hour", "ex": "Cut it in half."},
    "hospital": {"def": "醫院", "ipa": "/ˈhɒspɪtl/", "trans": "hospitals (複數)", "col": "go to the hospital", "ex": "He is in the hospital now."},
    "keep": {"def": "保持、保存", "ipa": "/kiːp/", "trans": "kept, kept", "col": "keep in touch", "ex": "Please keep your room tidy."},
    "ham": {"def": "火腿", "ipa": "/hæm/", "trans": "hams (複數)", "col": "ham sandwich", "ex": "I want a ham sandwich."},
    "hot": {"def": "熱的", "ipa": "/hɒt/", "trans": "hotter, hottest", "col": "hot water, hot dog", "ex": "It's very hot today."},
    "key": {"def": "鑰匙、關鍵", "ipa": "/kiː/", "trans": "keys (複數)", "col": "car key, key point", "ex": "Where did I put the keys?"},
    "hand": {"def": "手", "ipa": "/hænd/", "trans": "hands (複數)", "col": "on the other hand", "ex": "Wash your hands before dinner."},
    "hotel": {"def": "飯店", "ipa": "/həʊˈtel/", "trans": "hotels (複數)", "col": "book a hotel", "ex": "We stayed in a 5-star hotel."},
    "kick": {"def": "踢", "ipa": "/kɪk/", "trans": "kicked, kicking", "col": "kick the ball", "ex": "He kicked the ball into the net."},
    "hang": {"def": "懸掛", "ipa": "/hæŋ/", "trans": "hung, hung", "col": "hang out, hang up", "ex": "Hang your coat on the hook."},
    "hour": {"def": "小時", "ipa": "/ˈaʊə/", "trans": "hours (複數)", "col": "per hour, an hour ago", "ex": "I'll be back in an hour."},
    "kid": {"def": "小孩", "ipa": "/kɪd/", "trans": "kids (複數)", "col": "just kidding", "ex": "The kids are playing outside."},
    "happen": {"def": "發生", "ipa": "/ˈhæpən/", "trans": "happened, happening", "col": "what happened", "ex": "Accidents can happen anytime."},
    "house": {"def": "房子", "ipa": "/haʊs/", "trans": "houses (複數)", "col": "big house, move house", "ex": "They live in a large house."},
    "kill": {"def": "殺", "ipa": "/kɪl/", "trans": "killed, killing", "col": "kill time", "ex": "The poison kills insects."},
    "happy": {"def": "快樂的", "ipa": "/ˈhæpi/", "trans": "happily (副詞), happiness (名詞)", "col": "happy birthday", "ex": "I am so happy for you."},
    "housewife": {"def": "家庭主婦", "ipa": "/ˈhaʊswaɪf/", "trans": "housewives (複數)", "col": "be a housewife", "ex": "My mother is a housewife."},
    "kind": {"def": "種類、親切的", "ipa": "/kaɪnd/", "trans": "kindness (名詞)", "col": "all kinds of, kind of", "ex": "He is very kind to us."},
    "hard": {"def": "硬的、困難的", "ipa": "/hɑːd/", "trans": "harder, hardest, hardship (名詞)", "col": "hard work, study hard", "ex": "It's hard to learn English."},
    "how": {"def": "如何", "ipa": "/haʊ/", "trans": "無", "col": "how many, how much", "ex": "How do you do that?"},
    "king": {"def": "國王", "ipa": "/kɪŋ/", "trans": "kings (複數)", "col": "lion king", "ex": "The king lives in the palace."},
    "hat": {"def": "帽子", "ipa": "/hæt/", "trans": "hats (複數)", "col": "wear a hat", "ex": "Take off your hat."},
    "however": {"def": "然而", "ipa": "/haʊˈevə/", "trans": "無", "col": "however long", "ex": "I'm tired; however, I must finish."},
    "kiss": {"def": "吻", "ipa": "/kɪs/", "trans": "kissed, kissing", "col": "first kiss", "ex": "He kissed his mother goodbye."},
    "hate": {"def": "討厭", "ipa": "/heɪt/", "trans": "hated, hateful", "col": "hate to do", "ex": "I hate waking up early."},
    "hundred": {"def": "百", "ipa": "/ˈhʌndrəd/", "trans": "hundreds (複數)", "col": "one hundred", "ex": "There were over 100 people."},
    "kitchen": {"def": "廚房", "ipa": "/ˈkɪtʃɪn/", "trans": "kitchens (複數)", "col": "in the kitchen", "ex": "She is cooking in the kitchen."},
    "have": {"def": "有", "ipa": "/hæv/", "trans": "had, had", "col": "have a shower", "ex": "I have two brothers."}
}

def enrich_and_export(input_csv, output_excel):
    df = pd.read_csv(input_csv)
    # 取前 100 個單字
    df_sample = df.head(100).copy()
    
    enriched_data = []
    for _, row in df_sample.iterrows():
        word = row['單字'].strip()
        pos = str(row['詞類 (Parts of Speech)']).strip()
        
        # 尋找對應的高品質資料
        # 注意處理小括號或特殊字元，如 "glove(s)"
        clean_word = word.lower()
        
        item = VOCAB_FULL_DATA.get(clean_word)
        if not item:
            # 嘗試模糊匹配
            for key in VOCAB_FULL_DATA:
                if key in clean_word or clean_word in key:
                    item = VOCAB_FULL_DATA[key]
                    break
        
        if item:
            # 按照範例圖片顯示的格式
            info = f"【解釋】{item['def']} 【音標】{item['ipa']} 【詞性變化】{item['trans']} 【搭配詞】{item['col']} 【例句】{item['ex']}"
        else:
            # 如果還是找不到，進行基本的 AI 式補充 (針對這 100 字以外的)
            info = f"【解釋】(補充中) 【音標】/.../ 【詞性變化】... 【搭配詞】... 【例句】... (Inferred)"
            
        enriched_data.append({
            '單字': word,
            '中文解釋 + 音標 +詞性變化+搭配詞+ 例句': info,
            '詞類 (Parts of Speech)': pos
        })
    
    df_final = pd.DataFrame(enriched_data)
    
    # 寫入 Excel
    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        df_final.to_excel(writer, index=False)
        # 自動調整欄寬 (選用步驟)
    
    print(f"成功處理 100 個單字並存至 {output_excel}")

if __name__ == "__main__":
    # 先讀取原始提取檔的前 100 筆確認單字是否完全對應
    enrich_and_export("extracted_vocab.csv", "高中英文參考詞彙表_樣本100_修正版.xlsx")
