import json
import random
import os

def load_vocab(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_text_quiz(data, output_dir='quizzes'):
    os.makedirs(output_dir, exist_ok=True)
    
    for level_info in data.get('levels', []):
        level_num = level_info['level']
        level_name = level_info['name']
        words = level_info['words']
        
        # 計算頁碼：從第三頁開始，一關兩頁 (Level 1: P.3-P.4, Level 2: P.5-P.6 ...)
        start_page = level_info.get('start_page', 3 + (level_num - 1) * 2)
        end_page = level_info.get('end_page', start_page + 1)
        page_str = f"P.{start_page} - P.{end_page}"
        
        # 題目卷與解答卷
        quiz_file = os.path.join(output_dir, f"Level_{level_num:02d}_P{start_page:02d}-P{end_page:02d}_Quiz.txt")
        answer_file = os.path.join(output_dir, f"Level_{level_num:02d}_P{start_page:02d}-P{end_page:02d}_AnswerKey.txt")
        
        shuffled_words = list(words)
        random.seed(level_num + 100)
        random.shuffle(shuffled_words)
        
        with open(quiz_file, 'w', encoding='utf-8') as qf:
            qf.write(f"=============== 專二餐服單字小考卷 (關卡 {level_num} | 課本頁碼: {page_str}) ===============\n")
            qf.write(f"單字主題：{level_name}\n")
            qf.write("班級：___________ 年級___________ 座號：_____ 姓名：__________  得分：_______\n\n")
            qf.write("一、 單字中譯測驗 (請寫出正確中文意思)\n")
            qf.write("-" * 68 + "\n")
            for idx, item in enumerate(shuffled_words, 1):
                qf.write(f"{idx:02d}. {item['en']:<22} [ {item.get('pron','')} ] : __________________\n")
            qf.write("-" * 68 + "\n")
            
        with open(answer_file, 'w', encoding='utf-8') as af:
            af.write(f"=============== 教師解答卷 (關卡 {level_num} | 課本頁碼: {page_str}) ===============\n")
            af.write(f"單字主題：{level_name}\n\n")
            for idx, item in enumerate(shuffled_words, 1):
                af.write(f"{idx:02d}. {item['en']:<22} -> {item['zh']}\n")

    print(f"成功依據「從第3頁開始、一關兩頁」規則，生成 {len(data.get('levels', []))} 個關卡考卷與解答至 '{output_dir}' 資料夾！")

if __name__ == '__main__':
    json_file = os.path.join(os.path.dirname(__file__), 'vocab.json')
    if os.path.exists(json_file):
        data = load_vocab(json_file)
        generate_text_quiz(data)
    else:
        print("未找到 vocab.json 檔案！")
