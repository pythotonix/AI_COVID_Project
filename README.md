# COVID-19 Multilingual Sentiment Analysis

*A research project combining multilingual NLP (XLM-RoBERTa & mBERT), temporal analysis, and interactive visualization.*

## Overview

This project analyzes **public sentiment expressed in Instagram posts during COVID-19 (2020–2024)** across several major world languages.
We evaluate two multilingual transformer models **XLM-RoBERTa** and **mBERT** compare their performance, explore temporal emotional trends, and connect sentiment dynamics with global COVID-related events.

The repository includes:

* **Full multilingual NLP pipeline**: text cleaning, stopwords, tokenization, class balancing, training & evaluation
* **Two model families**: XLM-RoBERTa and mBERT
* **Time-series and event impact analysis**
* **Interactive Streamlit dashboard**
* **Visualization notebooks (EDA, hashtags, events alignment)**

Dataset used in this project is publicly available on Zenodo.
<!-- 
## Repository Structure

```
.
├── Dashboard/
│   ├── app.py                      # Streamlit interactive dashboard
│   ├── eventscopy.csv              # Global events dataset (added manually)
│   └── covid_instagramcopy.csv     # Main dataset (too large → added externally)
│
├── EDA/
│   ├── events.csv                  # Cleaned events dataset
│   ├── adding_dates.ipynb          # Merging posts with event timeline
│   ├── first_eda.ipynb             # General exploratory analysis
│   └── plot_hashtag.ipynb          # Hashtag-specific trends
│
├── TimeSeries/
│   └── time_series.ipynb           # Sentiment × events time-series correlation
│
├── mBERT/
│   ├── initial_file.ipynb          # Balancing + tokenization for all languages
│   ├── mBERT_English_balanced2.ipynb
│   ├── mBERT_Hindi_balanced2.ipynb
│   ├── mBERT_Indonesian_balanced2.ipynb
│   ├── mBERT_Portuguese_balanced2.ipynb
│   └── mBERT_Spanish_balanced2.ipynb
│
└── xlm-roberta/
    ├── top-lang/                   # First pass, no balancing
    │   ├── Roberta_English.ipynb
    │   ├── Roberta_Hindi.ipynb
    │   ├── Roberta_Indonesian.ipynb
    │   ├── Roberta_Portuguese.ipynb
    │   ├── Roberta_Spanish.ipynb
    │   └── Roberta_Turkish.ipynb
    │
    ├── balanced/                   # First balancing approach: weighted CE loss
    │   └── Roberta_*_balanced.ipynb
    │
    └── balanced_2/                 # Final balancing (over + under sampling)
        ├── Full_language_tokenization.ipynb   # Pipeline for all languages
        ├── data-balancing-distribution.ipynb
        ├── Spanish_balanced_2.ipynb
        ├── Spanish_balanced_3.ipynb
        ├── english-balanced-2-3.ipynb
        ├── hindi-balanced-2-3.ipynb
        ├── portuguese-balanced-2-3.ipynb
        └── indonesian-balanced-2-3.ipynb
``` -->


# Dataset

We use the public Instagram COVID-19 dataset from **Zenodo**:

**[https://zenodo.org/records/13896353](https://zenodo.org/records/13896353)**

Download manually and place at:

```
/EDA/covid_instagram.csv
```

Also dashboard requires:

```
/Dashboard/covid_instagramcopy.csv
```



# How to Reproduce the Workflow

## Install dependencies

We recommend using a fresh virtual environment.

```
pip install -r requirements.txt
```

If running in **Colab** or **Kaggle**, each notebook contains pinned versions (Transformers 4.44.2, Datasets 2.20.0, Protobuf <5.0.0, etc.).

## Download dataset

Download from Zenodo and place at:

```
/EDA/covid_instagram.csv
```

Optionally copy it into `/Dashboard/` as:

```
covid_instagramcopy.csv
```

## Run preprocessing

Notebook:

```
/xlm-roberta/balanced_2/Full_language_tokenization.ipynb
```

This notebook:

* cleans text (URLs, mentions, HTML, stopwords)
* balances classes per language (over/under sampling)
* tokenizes into 256-length XLM-R input
* saves dataset and label maps for training

Runs on CPU.

---

## Train models (GPU recommended)

### XLM-RoBERTa:

Use the per-language notebooks, e.g.:

```
/xlm-roberta/balanced_2/english-balanced-2-3.ipynb
```

### mBERT:

```
/mBERT/mBERT_English_balanced2.ipynb
```

Each notebook:

* loads pre-tokenized dataset
* trains and evaluates (accuracy, macro-F1, confusion matrix)
* saves best model

## Run Time-Series Analysis

Notebook:

```
/TimeSeries/time_series.ipynb
```

Outputs correlations between global events and sentiment dynamics.

<!-- ## Launch the Dashboard

```
cd Dashboard
streamlit run app.py
```

Dashboard displays:

* full sentiment timeline
* global events overlay
* daily multilingual comparison
* random post samples
* geographical sentiment differences

(Requires dataset placed into `/Dashboard/`.) -->


# Model Comparison (XLM-R vs mBERT)

| Language | XLM-R Accuracy | mBERT Accuracy | XLM-R Macro-F1 | mBERT Macro-F1 |
| -------- | -------------- | -------------- | -------------- | -------------- |
| ES       | 0.84           | 0.83           | 0.73           | 0.70           |
| EN       | 0.91           | 0.87           | 0.90           | 0.86           |
| PT       | 0.85           | 0.81           | 0.73           | 0.67           |
| HI       | 0.76           | 0.79           | 0.67           | 0.70           |
| ID       | 0.85           | 0.80           | 0.76           | 0.70           |

**Takeaways:**

* **XLM-R outperforms mBERT on most languages**, especially larger datasets (EN, ES).
* **mBERT performs better on Hindi**, likely due to stronger regional linguistic representation.
* Both models benefit significantly from **balanced sampling**.

# Project Architecture

A simplified pipeline diagram:

```
 Raw Instagram Posts (Zenodo)
            │
            ▼
   Text Cleaning (URLs, HTML, hashtags)
            │
            ▼
     Stopwords removal (per language)
            │
            ▼
  Class Balancing (Over + Under Sampling)
            │
            ▼
     Tokenization (XLM-R / mBERT, max_len=256)
            │
            ▼
   Saved Tokenized Dataset + Label Maps
            │
            ▼
 Transformer Training (3 epochs, early stopping)
            │
            ▼
 Evaluation (Macro-F1, Confusion Matrix)
            │
            ▼
   Time-Series Analysis + Dashboard
```

# Contributors

* **Tetiana Shvets, Anna Piaskovska, Anastasia Khalus**

   Ukrainian Catholic University, Faculty of Applied Sciences, Business Analytics