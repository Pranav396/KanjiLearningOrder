# Optimizing Kanji Learning Order

A data-driven approach to Japanese character acquisition. This project clusters the 2,136 jōyō kanji by simplicity (stroke count) and utility (corpus frequency) to propose a more efficient learning order than the traditional JLPT sequence.

## 🌐 Live Demo
[kanjilearningorder.streamlit.app](https://kanjilearningorder.streamlit.app)

## 📓 Notebook
The full analysis is documented in `project.ipynb`, covering data collection, cleaning, feature engineering, clustering, and results.

## 📁 Repository Structure
```
├── project.ipynb         # Main analysis notebook
├── app.py                # Streamlit dashboard
├── kanji.db              # SQLite database
├── requirements.txt      # Python dependencies
├── Data/                 # Raw data files
├── Data/                 # Raw data files
│   ├── jouyou.json       # Jōyō kanji data (davidluzgouveia)
│   ├── kyouiku.json      # Kyōiku kanji data (davidluzgouveia) - Unused
│   ├── wk_kanji.json     # WaniKani kanji data (via API)
│   ├── aozora.csv        # Aozora Bunko frequency (scriptin)
│   ├── wikipedia.csv     # Wikipedia frequency (scriptin)
│   ├── news.csv          # News frequency (scriptin)
│   └── kanjidic2.xml     # KANJIDIC2 (EDRDG) — Unused
└── wanikani.py           # WaniKani API fetch script
```

## 📊 Data Sources
- **WaniKani API** — Kanji levels and radical names. © Tofugu LLC
- **[kanji-data](https://github.com/davidluzgouveia/kanji-data)** by davidluzgouveia — JLPT levels, stroke counts, grade. (MIT License)
- **[kanji-frequency](https://github.com/scriptin/kanji-frequency)** by Dmitry Shpika — Corpus frequency ranks. (CC BY 4.0)
- **KANJIDIC2** by EDRDG — Explored but unused. (CC BY-SA 4.0)

## 🛠️ Setup
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📄 References
- Paxton, S. & Svetenant, C. (2014). [Tackling the Kanji Hurdle](https://www.researchgate.net/publication/271258201_Tackling_the_Kanji_hurdle_Investigation_of_Kanji_learning_in_Non-Kanji_background_learners). *International Journal of Research Studies in Language Learning*, 3(3), 89–104.
- Agency for Japanese Cultural Affairs. ["常用漢字表" [Jōyō Kanji Table]](www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/pdf/joyokanjihyo_20101130.pdf). Ministry of Education, Culture, Sports, Science and Technology, 30 Nov. 2010.
