---

# ✅ **1. GitHub Folder Structure**

```
excel-to-powerpoint-automation/
│
├── data/
│   └── data.xlsx
│
├── template/
│   └── template.pptx
│
├── output/
│   └── (generated files appear here)
│
├── src/
│   └── excel_to_ppt.py
│
├── README.md
└── .gitignore
```

### Add to `.gitignore`:

```
output/
*.pptx
*.xlsx
__pycache__/
```

---

# ✅ **2. Your GitHub-ready README (Markdown)**

**Copy & paste directly into your repo.**

---

# **Excel → PowerPoint Automation**

Automated PowerPoint generation from Excel data using Python
*(Portfolio Project)*

---

## 📌 **Overview**

This project automatically generates a fully formatted PowerPoint presentation from a single row of data in an Excel file. It is designed for real-world scenarios where:

* A company uses a **PowerPoint template**
* A user fills in a few fields in **Excel**
* The system injects those values into predefined **placeholders inside the PPTX**

The script replaces placeholders such as:

```
{{ClientName}}
{{ProjectName}}
{{Revenue}}
{{StartDate}}
{{EndDate}}
{{Summary}}
```

and outputs a ready-to-use presentation.

This is the exact type of automation used in consulting, reporting, enterprise ops, and marketing teams.

---

## 🔧 **Key Features**

### ✔ Works with any PowerPoint template

Automatically reads all shapes and replaces text in *any* slide.

### ✔ Handles broken PowerPoint runs

Merges text internally so placeholder replacement is always correct.

### ✔ Excel dates formatted cleanly

Ensures dates appear as: `2025-01-10`

### ✔ Zero manual editing

The user only updates Excel and runs:

```
python excel_to_ppt.py
```

### ✔ Output auto-named

For example:

```
ClientName = Globex Ltd → outputs /output/Globex_Ltd.pptx
```

---

## 🧩 **How It Works**

### **1. User fills Excel sheet**

Example:

| ClientName | ProjectName           | Revenue | StartDate  | EndDate    | Summary                                          |
| ---------- | --------------------- | ------- | ---------- | ---------- | ------------------------------------------------ |
| Globex Ltd | Compliance Automation | 98000   | 2025-01-10 | 2025-03-05 | Automated data validation and reporting workflow |

---

### **2. PowerPoint contains placeholders**

In PowerPoint, designer places text like:

```
Project: {{ProjectName}}
Start Date: {{StartDate}}
Revenue: {{Revenue}}
```

---

### **3. Python reads Excel → replaces placeholders → saves output**

---

## 🚀 **Running the Script**

**Prerequisites:**

```
pip install python-pptx openpyxl
```

Then run:

```
python excel_to_ppt.py 2
```

Where `2` is the Excel row number.

---

## 🧠 **Core Python Script**

Located in `src/excel_to_ppt.py`.

*(Do not paste script here — already added in your code.)*

---

## 📁 **Folder Setup**

Place your template here:

```
/template/template.pptx
```

Place your Excel file here:

```
/data/data.xlsx
```

Outputs will be saved here:

```
/output/YourClientName.pptx
```

---

## 📝 **Real-World Use Cases**

* Automated sales proposal decks
* Project onboarding decks
* Marketing report generation
* Client briefing templates
* Healthcare or SaaS customer setup slides
* Quarterly business review (QBR) generation

---

## 🏆 **Why This Is A Strong Portfolio Project**

This project demonstrates:

### ✔ Python automation

### ✔ Working with real enterprise tools (Excel + PowerPoint)

### ✔ Dynamic templating

### ✔ Text run consolidation (hard part of python-pptx)

### ✔ File system management

### ✔ Realistic client workflow

This is exactly the type of automation consulting clients pay for.

---


# done 🎉

