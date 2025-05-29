# 💼 LinkedIn Job Scraper

A Python-based web scraper that collects job listings from LinkedIn using Selenium, saving them into a CSV file for further analysis or visualization (e.g., in Power BI).

## 🚀 Features

- 🔍 Scrapes job title, company name, location, post date, skills, and job link
- 📜 Supports multiple job titles and locations
- 🧭 Automatically scrolls and loads more listings
- 💾 Saves results to `data/linkedin_jobs.csv`
- 🧩 Modular project layout for easy reuse or extension

## 🛠️ Technologies Used

- Python
- Selenium
- WebDriver Manager
- dotenv
- CSV
- OS
- (Optional) Power BI for visualization

## 📁 Project Structure

linkedin-job-scraper/

├── linkedin_scraper/

│ ├── scraper.py # Core scraping logic

│ ├── config.py # Configurable search terms

├── data/

│ └── linkedin_jobs.csv # Output file

├── run.py # Entry point

├── .env # Contains LinkedIn credentials (not tracked)

├── .gitignore # Excludes sensitive files

├── requirements.txt # Python dependencies

└── README.md # You’re here!

## ⚙️ Setup & Usage

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/linkedin-job-scraper.git
   cd linkedin-job-scraper
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up your LinkedIn credentials in `.env` (optional)**
4. **Run the scraper**
   ```bash
   python run.py
   ```
5. **Check `data/linkedin_jobs.csv` for the scraped job listings**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🛑 Disclaimer

This project is for educational purposes only. Scraping LinkedIn may violate their terms of service. Use responsibly and at your own risk.

## 📦 Setup Instructions

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Create a .env file with your LinkedIn credentials:**
   ```ini
   LINKEDIN_EMAIL=your_email
   LINKEDIN_PASSWORD=your_password
   ```
3. **Run the scraper**
   ```bash
   python run.py
   ```
4. **Check the output**
   View scraped data in `data/linkedin_jobs.csv`

## 📊 Visualizing Data

You can visualize the scraped data using Power BI or any other data visualization tool. Import the `data/linkedin_jobs.csv` file to create charts, graphs, and dashboards.
