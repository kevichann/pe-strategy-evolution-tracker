# pe-strategy-evolution-tracker

pip install -r requirements.txt

# Private Equity Strategy Evolution Tracker

**Computational Research Project | The Wharton School, University of Pennsylvania**

**Student Researcher:** Kevin Chan  
**Research Mentors:** Dr. Claudine Gartenberg and Elaine Pak  
**Research Period:** October 2025 – February 2026

---

## 1. Project Overview

**How do private equity firms describe their investment strategies, and how do those descriptions evolve over time?**

Private equity (PE) firms pursue different approaches to creating value, including financial restructuring, operational improvement, and strategic transformation. Yet studying how their investment philosophies evolve is challenging because firms update their websites, replace older strategy descriptions, and use inconsistent terminology.

I developed a Python-based computational workflow to identify active private equity firms, extract publicly stated investment strategies, and examine historical website information using the Internet Archive's Wayback Machine.

The objective was to transform unstructured website content into structured data that could support systematic comparisons of PE firms' strategic emphasis across different periods.

This project was conducted with guidance from researchers at the Wharton School, University of Pennsylvania.

---

## 2. Research Context and Mentorship

My primary research mentor was **Dr. Claudine Gartenberg**, Associate Professor of Management at Wharton. Her research examines corporate strategy, ownership structures, organizational purpose, and firm performance.

After working with Professor Gartenberg on an earlier research project examining collaboration in job descriptions, she introduced me to **Elaine Pak**, a Wharton Management PhD candidate researching private equity ownership and corporate strategy.

Elaine's research investigates how private equity owners implement distinct strategic approaches across portfolio companies.

Her job market paper, *Owning With Style: How Corporate Owners Shape Firm Strategy*, examines how private equity owners redeploy employees across portfolio firms to implement their investment strategies, or strategic "playbooks."

A component of her research involves measuring PE owners' strategic emphasis using historical website information. This is closely related to the data collection and analysis challenges addressed in my project.

My work supported this broader research effort through computational data collection, screening, and historical comparison. I worked independently on assigned technical tasks while receiving research direction and feedback from my mentors.

---

## 3. Research Objectives

My project focused on four questions:

1. How can active private equity firms with accessible websites be identified systematically?
2. How can publicly stated investment strategies be extracted from unstructured website content?
3. How can historical website snapshots be used to compare strategy descriptions over time?
4. What limitations arise when using public-facing investment language as a measure of strategic emphasis?

The broader goal was to investigate how computational methods can help researchers construct quantitative measures from qualitative business information.

---

## 4. Computational Methodology

### Step 1: Algorithmic Firm Screening

The first challenge was identifying private equity firms suitable for historical analysis.

I developed an algorithmic screening workflow to identify active firms with accessible websites.

This initial screening helped distinguish usable firm records from those lacking the website information required for further investigation.

**Technical focus:** Algorithmic filtering, firm identification, and data preparation.

### Step 2: Automated Web Scraping

Private equity firms typically publish investment philosophies and strategic priorities through website pages describing their investment approach.

I used Python web scraping techniques to retrieve publicly stated investment strategies.

The workflow involved collecting website content, parsing HTML, and extracting relevant strategy descriptions.

The resulting text could then be organized into a more structured format for analysis.

**Technical focus:** HTTP requests, HTML parsing, text extraction, and structured data processing.

### Step 3: Historical Website Retrieval

A company's present-day website does not necessarily preserve how its investment approach was described in previous years.

To investigate historical changes, I used the Internet Archive's Wayback Machine to retrieve earlier website snapshots.

This enabled comparisons between strategy descriptions from different periods.

Historical website retrieval introduced additional challenges because archived pages are not uniformly available across firms or years.

**Technical focus:** Historical data retrieval, longitudinal data collection, and temporal comparison.

### Step 4: Longitudinal Content Analysis

I examined how investment strategy descriptions changed across historical periods.

This included comparing changes in strategic language and the prevalence of selected investment strategy terms.

The goal was to structure qualitative website information so that strategic emphasis could be compared more systematically over time.

This approach illustrates how computational tools can help researchers investigate questions that would otherwise require extensive manual review of historical documents.

**Technical focus:** Text preprocessing, keyword-based comparison, and longitudinal content analysis.

---

## 5. My Specific Contributions

My primary responsibility was developing and implementing the computational workflow supporting the historical private equity strategy investigation.

I independently worked on:

- Designing an algorithmic screening process to identify active PE firms with accessible websites.
- Writing Python code to retrieve and extract investment strategy descriptions.
- Using the Wayback Machine to examine historical website information.
- Organizing collected text into structured data for comparison.
- Comparing changes in strategic language across time periods.

My mentors established the broader research direction and provided feedback during regular meetings.

My contribution focused on computational implementation and data preparation rather than developing the paper's hypotheses, conducting its broader econometric analysis, or claiming authorship of its findings.

---

## 6. Technical Stack

| Technology | Role in the Research Workflow |
|---|---|
| Python | Algorithm development and data processing |
| Requests | HTTP requests and website retrieval |
| Beautiful Soup | HTML parsing and text extraction |
| lxml | HTML and XML parsing support |
| Pandas | Data organization and manipulation |
| NumPy | Numerical data processing |
| OpenPyXL | Spreadsheet input and output |
| tqdm | Progress tracking |
| Internet Archive Wayback Machine | Historical website information |
| GitHub | Version control and code documentation |

The Python dependencies are listed in `requirements.txt`.

---

## 7. Repository Structure

```text
pe-strategy-evolution-tracker/
├── data/
├── scripts/
├── requirements.txt
└── README.md
```

**`scripts/`**

Python scripts associated with the research workflow.

**`data/`**

Data files associated with the project.

**`requirements.txt`**

Python dependencies required by the project.

**`README.md`**

Research background, methodology, contribution summary, and technical documentation.

---

## 8. Installation

Clone the repository:

```bash
git clone https://github.com/kevichann/pe-strategy-evolution-tracker.git
cd pe-strategy-evolution-tracker
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

### Running the Research Code

The repository contains Python scripts in the `scripts/` directory.

Execution depends on the inputs and configuration expected by each script. The scripts should be reviewed individually to determine their execution order and required input files.

The repository documents the research code and methodology rather than providing a packaged software application.

---

## 9. Research Challenges and Methodological Limitations

### Unstructured Website Information

Unlike standardized financial databases, corporate websites are designed primarily to communicate information to investors and other audiences.

Different firms use different terminology, website layouts, and levels of detail when describing investment strategies.

This makes automated collection and comparison challenging.

### Historical Data Availability

The Wayback Machine does not preserve every version of every website.

Archived pages may be missing for some periods, while other firms have more extensive historical records.

Consequently, the availability of historical data may vary substantially across companies.

### Selection and Survivorship Bias

Firms with accessible websites and extensive archived histories may not be representative of all private equity firms.

This creates a potential source of selection bias when comparing investment strategies over time.

### Measurement Validity

A firm's published investment strategy is not necessarily identical to its actual investment behavior.

Changes in website language may reflect marketing decisions, branding, or communication priorities rather than fundamental changes in investment activities.

For this reason, website-based strategy measures require careful interpretation.

### Descriptive Versus Causal Analysis

This project focuses on collecting and comparing historical descriptions.

Observed differences in strategic language do not establish causal relationships between private equity ownership, investment strategies, or company outcomes.

---

## 10. What I Learned

The most important lesson from this project was that collecting data and producing meaningful research findings are different challenges.

Initially, the technical problem seemed straightforward: identify firms, retrieve their websites, and collect investment strategy descriptions.

However, historical and unstructured data introduce questions that are not solved merely by writing working code.

How should incomplete records be handled? Can descriptions written in different years be compared reliably? Does a change in terminology represent a meaningful change in strategy?

I learned that computational research requires both technical implementation and careful consideration of what the data actually measure.

Working with Elaine also helped me understand how private equity owners' strategic approaches can affect organizational decisions, including how employees are deployed across portfolio companies.

This experience strengthened my interest in applied mathematics, computational modeling, and using quantitative methods to investigate real-world economic and organizational questions.

---

## 11. Related Academic Research

**Elaine Pak**

*Owning With Style: How Corporate Owners Shape Firm Strategy*

[Read Elaine Pak's Job Market Paper](https://faculty.wharton.upenn.edu/wp-content/uploads/2026/05/ElainePak_JMP.pdf)

Elaine's research examines how private equity owners implement distinct strategies, including through talent redeployment across portfolio companies.

Her paper uses historical private equity website information to help characterize owners' strategic approaches.

My project addresses closely related computational challenges involving historical website retrieval, strategy extraction, and the preparation of investment strategy data.

The paper provides the broader academic context for my research experience. I do not claim authorship of the paper or its empirical findings.

---

## 12. Project Scope and Attribution

This repository documents my work on computational methods for investigating the evolution of private equity investment strategy descriptions.

The broader academic research was conducted under the direction of my Wharton mentors.

The code and documentation presented here should be understood as a record of my individual research contributions, not as a complete reproduction of Elaine Pak's empirical analysis.

The project was an educational research experience and was not intended to be a commercial investment tool.

---

**Kevin Chan**  
The Haverford School | Class of 2027  
Student Researcher

**Research Area:** Computational Analysis, Private Equity Strategy, Applied Data Science
