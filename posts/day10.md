# Day 10 — 建立 first-policy skill 的四大子命令骨架

> **前情提要**：前幾天我們搞定了開發環境、Ollama 引擎與 API 快取機制。
> **本日目標**：為我們的 `first-policy` 建立四大核心指令（Subcommands）的實體檔案，讓 AI 正式學會這四招。

---

## 1. 拆解大腦：為何要有子命令？ (The Meat)

在 Day 8 建立的 `SKILL.md` 是 AI 的主控台，決定了 AI 的人格與底線（免責聲明）。但是，如果我們把「財務健檢的數學公式」、「保單健檢的判斷邏輯」、「人生模擬的遊戲規則」全部塞進同一個檔案裡，AI 處理起來會非常沒有效率，甚至會混淆指令。

這就是 OpenCode 的 `commands/` 資料夾發揮威力的地方。我們透過建立 4 個獨立的 Markdown 檔案，將這 4 種截然不同的任務徹底切開：

1.  **`/financial-check` (財務健檢)**：計算 6-3-1 比例，找出防禦缺口。
2.  **`/insurance-review` (保單健檢)**：讀取 PDF 條款，尋找保障漏洞。
3.  **`/life-simulate` (人生模擬)**：推演 30 年後的結果。
4.  **`/future-self` (60歲回顧)**：跨越時空的感性總結。

當你在對話框輸入 `/financial-check` 時，AI **只會讀取** `financial-check.md` 裡的專業指示，完全不會被遊戲規則干擾。

## 2. 實作核心：建立子命令檔案 (Code Snippet)

請在你的終端機輸入以下指令，我們一口氣把這 4 個空殼建立起來：

```bash
# 確保你在 first-policy-ai 專案目錄下
# 進入 commands 資料夾
cd commands

# 建立 4 個子命令的 Markdown 檔案
echo "# 財務與防線檢測" > financial-check.md
echo "# 保單條款與缺口健檢" > insurance-review.md
echo "# 30 年平行時空財務模擬" > life-simulate.md
echo "# 來自 60 歲未來的復盤信" > future-self.md

# 回到上一層目錄
cd ..
```

接著，我們要驗證 OpenCode 是否有成功認得這個 Skill。請在終端機輸入：

```bash
opencode debug skill
```

如果你在終端機輸出的列表中，看到了 `first-policy`，並且裡面列出了這 4 個 commands，那麼恭喜你，你的 AI 骨架已經完美組裝成功了！

## 3. GitHub 專案公開：今日進度同步

為了讓你可以對照進度，我今天正式公開了本專案的 GitHub Repo！
👉 [GitHub: first-policy-ai](https://github.com/1daniel3333/first-policy-ai)

你可以直接在 Repo 裡的 `stages/` 資料夾找到今天以前的進度代碼。如果你在照著文章操作時有卡關，隨時可以 clone 對應天數的資料夾來進行比對！

---

## 4. 今日總結與明日預告 (階段二完結！)

今天我們完成了**第二階段 (OpenCode Skill 基礎)**。至此，開發環境、地端引擎、API 金鑰、Skill 骨架以及雙軌 GitHub Repo 全都架設完畢，基礎工程大功告成。

**思考題**：如果你想擴充這個 AI 顧問的功能，除了這 4 個指令，你還想加什麼？（例如 `/tax-calculate` 算所得稅？）

**明日預告**：明天（Day 11），我們將進入**第三階段 (財務健檢)** 的深水區！我們要先定義出 `/financial-check` 所需要的 `user_profile.json` Schema，看看 AI 怎麼精準算出你的財務缺口！

---
* 🔗 專案 GitHub 倉庫：[first-policy-ai](https://github.com/1daniel3333/first-policy-ai)
