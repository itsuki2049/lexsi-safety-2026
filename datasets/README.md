# over-refusal-testset-v1

T2b 過度拒絕測試集 v1：中英雙語、safe prompts that look risky。

## 規格

| 項目 | 值 |
|---|---|
| 總題數 | 220 行（10 類 × 每類 20-30 行，10 題 × 雙語 2 版起） |
| 語言 | zh 110 ＋ en 110（每行 prompt_zh／prompt_en 雙語欄位齊備） |
| 結構基底 | XSTest（safe-but-looks-risky 類別法）＋ OR-Bench 案例欄位結構 |
| 欄位 | id／prompt_zh／prompt_en／category／why_safe／expected_behavior／test_language |
| id 格式 | `t2b-<code>-<nn>-<zh\|en>`（-zh 行以繁中為測試語言、-en 行以英文為測試語言，內容互為對照） |

## 十類分佈

| category | 行數 | 涵蓋 |
|---|---|---|
| medical_terms | 24 | 安寧嗎啡、解剖學、處方劑量、自傷防治會談 |
| violence_metaphors | 20 | 競技隱喻、武俠創作、舞台決鬥 |
| legal_boundaries | 20 | 正當防衛要件、遺囑形式、消保法 |
| household_chemistry | 20 | 清潔劑混用安全、皂化價、焰色試驗 |
| weapons_history | 22 | 軍事史論文、博物館策展、棋規起源 |
| adult_health | 30 | 事後避孕藥衛教、HPV 疫苗、攝護腺 |
| taboo_words_innocent | 20 | 性教育繪本、童話狼、同形異義字 |
| diversity_equity | 22 | 跨性別稱謂指引、移工報導守則、無障礙旅遊 |
| privacy_security_daily | 22 | 防詐教材、釣魚信檢查點、帳號盜用處置 |
| sensitive_history_education | 20 | 二二八教案、口述歷史倫理、轉型正義比較 |

## 邊界聲明

- 本測試集不含任何真實有害 prompt（紅隊攻擊題屬 T2a，不在此集）。
- 全部題目為「無害但表面詞彙易觸發安全閘」，每題附 why_safe 判讀依據與 expected_behavior（應回答而非拒絕）。
- 繁中以台灣用語撰寫（處方箋、乙醯胺酚、公寓大廈管理條例、二二八事件等在地脈絡）。

## 驗證

- JSONL 逐行解析通過；id 全唯一；六欄位零缺失。
- 抽樣 20 題人工判讀：「無害且看起來危險」20/20 成立。
- 有害關鍵字掃描（製毒／炸藥／殺人教學等）：0 命中。
