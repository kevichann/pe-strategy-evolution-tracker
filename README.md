# Wharton Computational Research: Private Equity Strategies and O*NET Occupational Data

**Student Researcher:** Kevin Chan  
**School:** The Haverford School | Class of 2027  
**Research Institution:** The Wharton School, University of Pennsylvania  
**Research Mentors:** Professor Claudine Gartenberg and Elaine Pak  
**Research Areas:** Applied Mathematics, Computational Analysis, Organizational Strategy, and Data Science

---

## 1. Research Overview

My research at Wharton involved two related computational projects:

1. **Occupational data analysis:** Developing an O*NET-based scoring approach for research on collaboration and skills in job descriptions.
2. **Private equity strategy evolution:** Building Python tools to collect investment strategy descriptions from private equity firm websites and investigate changes in their language over time.

Although the projects addressed different research questions, both involved a challenge I became increasingly interested in: **How can messy, real-world information be turned into meaningful quantitative measurements?**

I first worked with Professor Claudine Gartenberg on job-description research. She later introduced me to Elaine Pak, whose research examines how private equity ownership and investment strategies influence organizational decisions.

My contributions focused on computational implementation, data preparation, and building tools for empirical research.

The primary focus of this repository is the private equity strategy project. It also includes code from my earlier O*NET work.

---

## 2. Project A: O*NET Occupational Data and Job-Description Research

**Mentor:** Professor Claudine Gartenberg  
**Research period:** Summer 2025

### Research Question

How can information about occupational skills and requirements be organized into comparable quantitative measures for studying collaboration in job descriptions?

Job descriptions use different terminology to describe responsibilities, capabilities, and workplace activities. Even when two positions involve similar work, their descriptions may be difficult to compare directly.

O*NET provides standardized occupational classifications and measurements that can help researchers investigate these differences.

### My Contribution

I worked on an O*NET-based occupational scoring task and developed Python code to process occupational data.

The published data-processing module, `src/data_processor.py`, performs several operations:

- Reads occupation titles and standardized O*NET-SOC occupation codes.
- Imports occupational datasets containing skills, abilities, and work activities.
- Groups occupational attributes using their O*NET element identifiers.
- Extracts Importance (IM) and Level (LV) ratings.
- Preserves information about the number of observations (`N`).
- Combines occupational attributes into a structured dataset.
- Exports the resulting data for further analysis.

The objective was to make occupational measurements easier to use when comparing job requirements.

### Technical Approach

The algorithm uses O*NET-SOC codes to connect occupational information across datasets.

For each occupation, the program identifies relevant elements, collects their ratings, and organizes the results into columns containing:

- Element ID
- Element name
- Importance rating
- Level rating
- Number of observations

Pandas is used for data manipulation, grouping, and merging.

The code preserves occupations even when some attributes are unavailable, allowing missing measurements to be represented explicitly.

### Scope of the Published Code

The file `src/data_processor.py` documents the occupational data-processing component of my O*NET work.

The currently published module organizes source ratings but does not include a separate complete job-description-to-occupation matching workflow, composite-scoring formula, or statistical correlation analysis.

These distinctions matter because preparing occupational measurements and validating a research measure are separate tasks.

---

## 3. Project B: Private Equity Strategy Evolution

**Research mentors:** Professor Claudine Gartenberg and Elaine Pak  
**Research period:** October 2025 – February 2026

### Research Question

**How do private equity firms describe their investment strategies, and how might those descriptions change over time?**

Private equity firms pursue different investment approaches, including:

- Operational improvements
- Growth investments
- Acquisition and consolidation strategies
- Platform investments
- Financial and organizational restructuring
- Strategic transformation

However, firms do not describe these approaches using consistent terminology.

Some emphasize operational expertise, while others focus on sector specialization, growth, or financial structuring.

These differences create a challenge for researchers seeking to compare investment strategies systematically.

Historical comparisons are particularly difficult because corporate websites change, older pages disappear, and archived versions may be incomplete.

### Research Objective

My objective was to build a computational workflow that could:

1. Identify candidate private equity firms with website information.
2. Locate pages describing their investment approaches.
3. Extract and organize strategy-related website text.
4. Retrieve archived website information across historical periods.
5. Identify strategy-related terminology for comparison.

The goal was not to prove that website descriptions accurately represent investment behavior, but to investigate how this information could be structured for further empirical research.

---

## 4. Python Implementation

I developed five scripts covering successive stages of the private equity research workflow.

### Stage 1: Investor Screening

**File:** `scripts/01_filter_investors.py`

The first script screens investor records using three criteria:

- The investor is not marked "Out of Business."
- The primary investor classification is `PE/Buyout`.
- A nonempty website field is available.

The results are exported to a filtered CSV dataset.

This is a rule-based screening process rather than independent verification that every retained firm is currently operating.

**Technical methods:** Pandas filtering, missing-value handling, and CSV processing.

### Stage 2: Website Discovery and Text Extraction

**File:** `scripts/02_scrape_pe_strategies.py`

This script retrieves firm websites and searches for descriptions of investment strategies.

It performs the following operations:

1. Reads website addresses from the filtered investor dataset.
2. Sends HTTP requests and parses website HTML.
3. Identifies internal links with relevant terms such as `strategy`, `approach`, `investment`, and `value-creation`.
4. Examines the homepage and up to two selected internal pages.
5. Extracts descriptive text from HTML elements.
6. Scores text blocks using strategy-related keyword matches.
7. Ranks the passages and retains selected text.
8. Records source URLs alongside the extracted information.

The scoring process looks for terms associated with investment strategies, including:

- Operational improvement
- Management
- Value creation
- Growth
- Platform investments
- Acquisition
- Transformation
- Governance
- Efficiency

The code selects up to five of the highest-scoring text blocks. When no blocks match the strategy keywords, it can fall back to other descriptive page content.

This fallback improves text coverage but also creates a risk of collecting irrelevant information.

**Technical methods:** Python, Requests, lxml, URL parsing, keyword scoring, and text ranking.

### Stage 3: Historical Website Retrieval

**File:** `scripts/03_wayback_scraper.py`

A present-day website may not reflect how a firm described its strategy in earlier years.

I developed a script that queries the Internet Archive's Wayback Machine CDX API for historical website snapshots.

The code targets six years:

**2015, 2017, 2019, 2021, 2023, and 2025.**

For each firm and target year, it attempts to:

1. Locate an archived webpage.
2. Retrieve the archived HTML.
3. Extract text from the webpage.
4. Identify selected strategy-related keywords.
5. Record the results in a structured dataset.

The script distinguishes between periods where no snapshot is available and snapshots where no selected keywords are found.

Historical availability depends on the Internet Archive and may differ across websites and periods.

### Stage 4: Strategy-Term Aggregation

**File:** `scripts/04_analyze_strategy_evolution.py`

I also wrote code to organize keyword results across historical periods.

The script reads the historical keyword dataset and produces aggregated counts for individual terms by year.

This supports descriptive comparisons of strategy-related language.

The current code requires additional missing-data handling to avoid counting certain missing-snapshot labels as if they were strategy keywords.

Consequently, these aggregated counts should not be interpreted as validated historical findings without further checking.

### Stage 5: Data Visualization

**File:** `scripts/05_visualize_trends.py`

The final script uses Pandas, Matplotlib, and Seaborn to create line charts showing strategy-term counts across periods.

Selected terms include:

- Leveraged buyout
- Value creation
- Digital transformation
- Platform
- Operational improvement

The script is intended to make changes in selected terminology easier to inspect.

The presence of the visualization code does not, by itself, establish that the full historical workflow produced complete or validated results.

---

## 5. Pilot Results

I tested the live website extraction workflow on a sample of 100 firm websites.

| Measure | Pilot Result |
|---|---:|
| Target websites | 100 |
| Websites with nonempty extracted text | 82 |
| Websites without nonempty extracted text | 18 |
| Nonempty extraction coverage | 82% |

The corresponding output is available in:

`data/processed/PE_Strategy_Implementation.csv`

The output records firm website addresses, extracted text, and source pages.

### Interpretation

The 82% figure measures **nonempty text extraction**, not verified accuracy in identifying investment strategies.

Some extracted passages contain material such as announcements, company news, or other website content rather than direct descriptions of investment philosophy.

This pilot demonstrated that the workflow could retrieve text from many of the selected websites, but also highlighted the need for additional validation.

The pilot was not designed to be a representative sample of all private equity firms.

---

## 6. Research Challenges and Limitations

### Challenge 1: Finding Relevant Information

Private equity websites are organized differently.

Some firms maintain dedicated strategy pages. Others describe their investment approach through portfolio information, news releases, or general company descriptions.

Keyword-based page discovery helped automate the search, but relevant information was not always located in predictable places.

### Challenge 2: Keyword Matches Are Not Strategy Measurements

A passage containing "growth," "platform," or "operational improvement" may appear relevant without actually describing a firm's investment approach.

A keyword match is therefore not equivalent to an accurate strategy classification.

This makes measurement validity an important limitation of the approach.

### Challenge 3: Missing Historical Data

The Wayback Machine does not preserve every website in every year.

Missing snapshots can reflect incomplete archival coverage rather than a firm's actual absence or a change in its strategy.

Historical comparisons must therefore account for uneven data availability.

### Challenge 4: Changes in Language Versus Changes in Behavior

A firm might change the language on its website because of branding, marketing, or communication priorities.

Such changes do not necessarily indicate changes in its actual investment behavior.

Website text may be a useful source of research data, but it requires careful interpretation and, where possible, independent validation.

### Challenge 5: Reproducibility

The code represents research-stage computational work rather than a fully packaged software application.

The historical analysis scripts need additional validation and cleanup of missing-data labels.

Some input files and dependencies also require configuration before the complete workflow can be reproduced.

---

## 7. What I Learned

Both projects changed how I think about computational research.

During the O*NET project, I worked on converting occupational information into comparable measurements.

The challenge was not simply retrieving numerical ratings. It was understanding how those measurements related to what researchers actually wanted to study.

I encountered a similar issue with private equity websites.

At first, I focused on getting the scraper to retrieve information successfully. But finding text containing relevant keywords did not necessarily mean I had measured a firm's strategy correctly.

I learned that **making code run and measuring something accurately are two different accomplishments.**

Working with Elaine also helped me understand how investment strategies connect to organizational decisions, including the redeployment of talent across portfolio companies.

These experiences strengthened my interest in applied mathematics, computational methods, and using quantitative analysis to study real-world problems.

---

## 8. Research Mentorship and Attribution

My first research experience was under the guidance of **Professor Claudine Gartenberg** at Wharton.

She helped frame the broader questions behind the job-description research and guided my work on occupational measurement.

After that project, she introduced me to **Elaine Pak**, whose research investigates private equity ownership and firm strategy.

Elaine explained the objectives of the private equity project and helped identify the information needed for comparing investment strategies.

We met regularly to review progress, discuss data-quality problems, troubleshoot obstacles, and identify next steps.

I independently developed the Python scripts documented in this repository.

My contributions were focused on assessing practicality and feasibility for further research. 

The broader research questions and academic interpretation were guided by my mentors.

My work is simply a preliminary proof of concept for Elaine's work. I did not author her paper itself.

---

## 9. Related Academic Research

**Elaine Pak**

*Owning With Style: How Corporate Owners Shape Firm Strategy*

[Read the research paper](https://faculty.wharton.upenn.edu/wp-content/uploads/2026/05/ElainePak_JMP.pdf)

Elaine's research investigates how private equity owners implement different strategic approaches, including through talent redeployment across portfolio companies.

The paper provides the subsequent academic work associated with my project.

My GitHub repository documents my computational work, not the complete research methods or results of Elaine's paper.

---

## 10. Repository Structure

```text
pe-strategy-evolution-tracker/
|
|-- README.md
|-- requirements.txt
|
|-- scripts/
|   |-- 01_filter_investors.py
|   |-- 02_scrape_pe_strategies.py
|   |-- 03_wayback_scraper.py
|   |-- 04_analyze_strategy_evolution.py
|   `-- 05_visualize_trends.py
|
|-- src/
|   |-- __init__.py
|   `-- data_processor.py
|
`-- data/
    |-- Occupation Data.txt
    |-- Skills.txt
    |-- Abilities.txt
    |-- Work Activities.txt
    |-- Work Context.txt
    |
    |-- raw/
    |   |-- investorAll.csv
    |   `-- filtered_investors.csv
    |
    `-- processed/
        |-- filtered_investors.csv
        `-- PE_Strategy_Implementation.csv
```

### Key Files

| File | Purpose |
|---|---|
| `src/data_processor.py` | Processes and combines O*NET occupational ratings |
| `scripts/01_filter_investors.py` | Screens PE/Buyout investor records |
| `scripts/02_scrape_pe_strategies.py` | Discovers and extracts website strategy-related content |
| `scripts/03_wayback_scraper.py` | Queries historical website snapshots |
| `scripts/04_analyze_strategy_evolution.py` | Aggregates historical strategy keywords |
| `scripts/05_visualize_trends.py` | Creates strategy-term visualizations |
| `data/processed/PE_Strategy_Implementation.csv` | Existing live website extraction pilot output |

The repository contains both research scripts and associated data files. Not all datasets shown in the directory are complete research outputs.

---

## 11. Installation and Usage

### Clone the Repository

```bash
git clone https://github.com/kevichann/pe-strategy-evolution-tracker.git
cd pe-strategy-evolution-tracker
```

### Create a Virtual Environment

```bash
python -m venv .venv
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

### Install Dependencies

The current `requirements.txt` includes dependencies associated with the occupational-data work but does not yet list every library imported by the private equity scripts.

For the published code, install the listed requirements and additional PE dependencies:

```bash
python -m pip install -r requirements.txt requests lxml matplotlib seaborn
```

### O*NET Data Processing

The O*NET processor currently expects its input files in the working directory.

From the repository root on macOS or Linux:

```bash
cd data
python ../src/data_processor.py
```

The script reads the available occupational data files and writes `processed_onet_data.csv` into the working directory.

The code also references `Knowledge.txt`, which is not currently included in the repository. It handles missing input files by issuing a warning and continuing.

### Private Equity Website Scraping

The private equity scripts expect `filtered_investors.csv` in the current working directory.

A populated version is stored in `data/raw/`.

From the repository root on macOS or Linux:

```bash
cp data/raw/filtered_investors.csv filtered_investors.csv
python scripts/02_scrape_pe_strategies.py
```

The scraper processes up to 100 website addresses and writes:

`PE_Strategy_Implementation.csv`

The original full investor input, `investorAll.csv`, is not available as a usable dataset in the current repository; its committed version is an empty placeholder.

Therefore, reproducing the initial investor filtering requires a valid source dataset.

### Historical Analysis

The historical pipeline consists of:

```bash
python scripts/03_wayback_scraper.py
python scripts/04_analyze_strategy_evolution.py
python scripts/05_visualize_trends.py
```

These commands represent the intended processing order, not a guarantee that the complete workflow runs successfully without additional corrections.

Historical retrieval depends on external archive availability and may take substantial time when processing a large firm list.

The analysis script's missing-data handling also requires correction before its counts should be relied upon.

---

## 12. Project Scope

This repository records computational work from two Wharton research experiences.

It is intended to show my individual approach to data collection, processing, and measurement challenges.

It is not a publication, a complete reproduction of my mentors' empirical research, or a validated commercial research system.

The most important lesson across both projects was that **the usefulness of quantitative analysis depends not only on the code, but also on whether the underlying data represent what we intend to measure.**

---

**Kevin Chan**  
The Haverford School | Class of 2027  
Student Researcher  
Applied Mathematics and Computational Research
