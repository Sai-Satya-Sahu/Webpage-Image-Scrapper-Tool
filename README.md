# 🎉 Welcome to My First Project

## 🌐 Webpage Image Scraper + 📄 PDF Converter

Welcome to my very first GitHub project!  
This tool is designed to **scrape all important document images from a webpage** — like scanned book pages or online document viewers — and **convert them into a PDF** automatically.

I hope you like my project and find it helpful! ❤️

---

### ✨ Features

- ✅ **Smart Document Image Detection**  
  Automatically skips logos, ads, buttons, and other non-document images.

- 📜 **Deep Scroll & Lazy Load Support**  
  Scrolls the page fully and waits to load even lazy-loaded images.

- 🔁 **Auto Retry on Timeout or Connection Issues**  
  Built-in retry mechanism ensures reliable downloads even on slow networks.

- 📂 **Organized Output**  
  Downloads go into a folder named `downloaded_images/`.

- 🧠 **PDF Generator Tool**  
  Automatically combines the downloaded images into a clean, page-by-page PDF.

---

### 🧠 How Filtering Works

Only **important images** (like scanned pages or document content) are downloaded.  
We filter out common junk like:

- `logo`, `icon`, `ad`, `banner`, `favicon`, `share`, etc.
- Images smaller than `300x300` pixels

> ⚙️ **Want everything?**  
Just **remove or comment out** the `is_document_image()` function to disable filtering.

---

### 📦 Project Structure

```bash
📁 downloaded_images/
├── image_1.jpg
├── image_2.jpg
└── document.pdf        # Created using the PDF converter tool

📄 doc_image_downloader.py   # Scrapes images from a webpage
📄 images_to_pdf.py          # Converts images into a single PDF
```
### 🚀 Getting Started

1. Clone this repository:
```bash
   git clone https://github.com/Sai-Satya-Sahu/Webpage-Image-Scrapper-Tool.git
   cd Webpage-Image-Scrapper-Tool
```
2. Install dependencies:
```bash
   pip install -r requirements.txt
```
3. Run The Downloader:
```bash
   python ImgDownloader.py
```
4. Then Convert The Images Into PDF:
```bash
   python ImgToPdf.py
```
- **Remember While Converting, The Converter Takes Serially Input from Name Image_1 ...**
- `There is also a Power Script. Please Read The UsagesManual.txt For More Information.`
---
### 🚨 IMPORTANT ALERT!!!
- ` I Will Suggest To Download These Files And Run In Your Local Machine`
If you are running this project in **GitHub Codespaces**, please note:

> 🛑 **This project uses Selenium with Chrome WebDriver, which requires a browser to be present on the system.**  
Codespaces **does not come with Chrome or Chromium pre-installed**, and your script will fail with an error like:

```bash
   selenium.common.exceptions.WebDriverException: unknown error: cannot find Chrome binary
```
---
### ✅ Recommended Fix for Codespaces
Run the following command in the **Codespaces terminal** before running the script:
```bash
   sudo apt-get update
   sudo apt-get install -y chromium-browser
```
Then, make sure your script is updated to look for Chromium at `/usr/bin/chromium-browser.`

If you're using a custom environment or container, you can also set the environment variable:
```bash
   export CHROME_BINARY=/path/to/chrome
```

---
### 🔧 Requirements
- Python 3.7+
- `selenium`, `beautifulsoup4`, `requests`, `Pillow`, `webdriver-manager`

Install Them With:
```bash
   pip install selenium beautifulsoup4 requests Pillow webdriver-manager
```
---

### 🤝 Support & Feedback

`If you liked this project or found it useful, please consider ⭐️ starring the repo.`  
`I'd love to hear your feedback and suggestions — open an issue or drop a message!`

---

### 🙏 Thank You!
> **Made with ❤️ by Sai**  
**"Every pro was once a beginner."**