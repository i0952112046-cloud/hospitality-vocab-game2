import json
import random
import os

def load_vocab(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_quizzes(data, output_dir='quizzes'):
    os.makedirs(output_dir, exist_ok=True)
    levels = data.get('levels', [])
    
    # 1. 生成各常規關卡小考卷
    for level_info in levels:
        level_num = level_info['level']
        level_name = level_info['name']
        words = level_info['words']
        
        start_page = level_info.get('start_page', 3 + (level_num - 1) * 2)
        end_page = level_info.get('end_page', start_page + 1)
        page_str = f"P.{start_page} - P.{end_page}"
        
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

    # 2. 生成 15+1 (共16個) 階段總測驗考卷
    # 前 15 個：每 3 關一次 (Level 1~3, 4~6 ... 43~45)
    # 第 16 個：最後 4 關 (Level 46~49)
    review_configs = []
    for i in range(1, 16):
        lvl_start = (i - 1) * 3 + 1
        lvl_end = i * 3
        p_start = 3 + (lvl_start - 1) * 2
        p_end = 4 + (lvl_end - 1) * 2
        review_configs.append({
            'id': i,
            'title': f"階段總測驗 {i} (涵蓋 Level {lvl_start}~{lvl_end} | P.{p_start}~P.{p_end})",
            'filename': f"Review_Test_{i:02d}_Lvl{lvl_start:02d}-{lvl_end:02d}",
            'lvl_range': list(range(lvl_start, lvl_end + 1))
        })
        
    # 第 16 個：最後 4 關
    review_configs.append({
        'id': 16,
        'title': "階段總測驗 16 [期末總複習/最終大會考] (涵蓋 Level 46~49 | P.93~P.100)",
        'filename': "Review_Test_16_Lvl46-49_Final",
        'lvl_range': [46, 47, 48, 49]
    })

    # 生成 16 份總測驗 txt 檔
    for r_cfg in review_configs:
        combined_words = []
        for lvl_num in r_cfg['lvl_range']:
            target_lvl = next((l for l in levels if l['level'] == lvl_num), None)
            if target_lvl:
                combined_words.extend(target_lvl['words'])
            else:
                # 示範數據保護
                combined_words.extend(levels[0]['words'])
                
        random.seed(r_cfg['id'] + 5000)
        random.shuffle(combined_words)
        
        # 總測驗挑選 25 題
        sample_words = combined_words[:25]
        
        r_quiz_file = os.path.join(output_dir, f"{r_cfg['filename']}_Quiz.txt")
        r_ans_file = os.path.join(output_dir, f"{r_cfg['filename']}_AnswerKey.txt")
        
        with open(r_quiz_file, 'w', encoding='utf-8') as qf:
            qf.write(f"⚔️ =============== 專二餐服 {r_cfg['title']} =============== ⚔️\n")
            qf.write("班級：___________ 年級___________ 座號：_____ 姓名：__________  得分：_______\n\n")
            qf.write("一、 綜合單字中譯測驗 (每題4分，共100分)\n")
            qf.write("=" * 72 + "\n")
            for idx, item in enumerate(sample_words, 1):
                qf.write(f"{idx:02d}. {item['en']:<22} [ {item.get('pron','')} ] : __________________\n")
            qf.write("=" * 72 + "\n")

        with open(r_ans_file, 'w', encoding='utf-8') as af:
            af.write(f"⚔️ =============== 教師解答卷：{r_cfg['title']} =============== ⚔️\n\n")
            for idx, item in enumerate(sample_words, 1):
                af.write(f"{idx:02d}. {item['en']:<22} -> {item['zh']}\n")

    print(f"成功生成 49 關常規考卷 + 16 份階段總測驗考卷與解答至 '{output_dir}' 資料夾！")

if __name__ == '__main__':
    json_file = os.path.join(os.path.dirname(__file__), 'vocab.json')
    if os.path.exists(json_file):
        data = load_vocab(json_file)
        generate_quizzes(data)
    else:
        print("未找到 vocab.json 檔案！")
