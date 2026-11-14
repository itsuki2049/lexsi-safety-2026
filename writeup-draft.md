# Over-Refusal Evaluation of Aya-Expanse-8B: A Traditional Chinese-First Safety Test Set
**T2b｜Team: Yongle (solo)｜Draft v1 (2026-11-14)**

## Title + one-line claim
Over-refusal evaluation of Aya-Expanse-8B with a 220-prompt bilingual (Traditional Chinese/English) safe-but-risky-looking test set: quantifying how often harmless daily requests are wrongly refused.

## Tracks + problem statements
- **[T2b] Over-refusal test set**: safe prompts that look risky, used to check the model does not refuse harmless requests

## Abstract (under 500 words — draft, pending final results)
AI assistants increasingly serve multilingual households, yet safety alignment research remains English-centric. We present a 220-prompt over-refusal test set in Traditional Chinese (Taiwan usage) and English, covering ten everyday categories where helpfulness matters most: palliative-care dosage teaching, household chemistry safety confirmation, sexual-health education materials, fraud-pattern recognition, and historically sensitive education among them. We evaluate Aya-Expanse-8B (the hackathon base model) and quantify the over-refusal rate — the share of harmless requests wrongly refused — overall and per category, with per-item bilingual analysis.

*(結果數據待評測後填入)*

## Headline before → after number
(待評測：Aya-expanse-8b 於 220 題雙語安全測試集的誤拒率 — baseline 量測)

## Base model + method
Aya-Expanse-8B (Cohere Labs, Apache-2.0) via local inference (Ollama, 8B Q4) — zero-shot evaluation, no fine-tuning (T2b scope: test set construction + evaluation).

## Problem statement and approach
**Why this problem**: Safety tuning over-corrects. Nurses ask about morphine dosing for palliative education; homeowners confirm bleach-mixing safety; educators select sex-ed picture books. When models refuse these harmless requests, the harm lands on exactly the users who need help most — and non-English users face a double penalty: the safety training was English-centric, and their language's harmlessness signals were never learned.

**Approach**: (1) Curate 220 prompts (110 zh-TW / 110 en) across ten XSTest-style categories with per-item `why_safe` rationale and `expected_behavior`. (2) Evaluate zero-shot with bilingual refusal-pattern detection (v1 heuristics; v2 adds LLM-as-judge cross-validation). (3) Quantify over-refusal rate overall and per category.

## Hackathon repos used
- **SafeTune**: Not used — this sprint is evaluation-only scope; original curation meets T2b core requirement
- **CuratorKIT**: Not used — original test-set curation (XSTest-style structure, bilingual extension); KIT-based distillation belongs to T1 scope

## Datasets, benchmarks and licenses
- Over-refusal test set v1: 220 prompts (110 zh-TW / 110 en), ten categories (20-30 each), original curation referencing XSTest structure. License: (確定中，擬 Apache-2.0 或 CC-BY-4.0)
- Safety retention check: (optional per template — T2b focus 為主)

## Metrics, and why these
- **Over-refusal rate (lower is better)**: share of harmless prompts met with refusal-pattern-matching responses. Per-category breakdown identifies which everyday domains suffer most.
- v2 規劃：LLM-as-judge 與人工標註一致率（Cohen's κ）交叉驗證

## Limitations
- Heuristic refusal detection may miss subtle refusals (v1; v2 judge 交叉驗證中)
- Single-model baseline in this sprint; multi-model comparison planned with more credits
- 220 prompts is a pilot scale

## With more credits
- Fine-tune Aya-Expanse-8B on balanced refusal/refusal-free pairs to reduce over-refusal without degrading true safety
- Extend to Japanese/Korean (Aya multilingual reach)

## Artifacts
- HF Dataset Collection: (建置中，token 就緒後上傳)
- This repo: eval pipeline + test set + write-up

## Documentation and reproduction
- Repo layout: datasets/（測試集）experiments/（評測管線與結果）writeup-draft.md
- Run: `python3 experiments/eval_over_refusal.py --model aya-expanse:8b --backend local --testset datasets/over-refusal-testset-v1.jsonl`
