import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin
import pandas as pd
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime, timedelta
import shutil



from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def init_driver_with_download(download_dir_path):
    # Ensure download_dir_path is absolute
    abs_download_path = os.path.abspath(download_dir_path)
    os.makedirs(abs_download_path, exist_ok=True)

    chrome_options = Options()
    prefs = {
        "download.default_directory": abs_download_path,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    return driver


# --- CONFIGURATION ---
TRENDLYNE_URL = "https://trendlyne.com/features/"
EMAIL = "avmgp.in@gmail.com"
PASSWORD = "Anupamvm1!"

# --- Set download folder to project directory ---
SCRIPT_DIR = os.getcwd()
CUSTOM_DOWNLOAD_FOLDER = os.path.join(SCRIPT_DIR, "trendlynedata")
os.makedirs(CUSTOM_DOWNLOAD_FOLDER, exist_ok=True)

# --- Configure Chrome to use custom download folder ---
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": CUSTOM_DOWNLOAD_FOLDER,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    "plugins.always_open_pdf_externally": True
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)

def login_to_trendlyne(driver):
    driver.get(TRENDLYNE_URL)
    time.sleep(2)

    login_button = driver.find_element(By.ID, "login-signup-btn")
    login_button.click()
    time.sleep(2)

    email_field = driver.find_element(By.ID, "id_login")
    password_field = driver.find_element(By.ID, "id_password")

    email_field.send_keys(EMAIL)
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

    if "logout" in driver.page_source.lower():
        print("✅ Login successful!")
    else:
        print("❌ Login may have failed. Please check manually.")

def getFnOData(driver):
    driver.get("https://trendlyne.com/futures-options/contracts-excel-download/")
    print("🔄 Navigated to FnO data downloader...")

    try:
        download_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Download')]"))
        )
        download_button.click()
        print("📥 Download initiated...")

        print("⏳ Waiting 10 seconds for download to complete...")
        time.sleep(10)

        files = [f for f in os.listdir(CUSTOM_DOWNLOAD_FOLDER) if f.endswith(".csv")]
        if not files:
            print("❌ No CSV found in custom folder.")
            return

        files.sort(key=lambda x: os.path.getctime(os.path.join(CUSTOM_DOWNLOAD_FOLDER, x)), reverse=True)
        latest_file = files[0]

        timestamp = datetime.now().strftime("%Y-%m-%d")
        new_filename = f"fno_data_{timestamp}.csv"
        old_path = os.path.join(CUSTOM_DOWNLOAD_FOLDER, latest_file)
        new_path = os.path.join(CUSTOM_DOWNLOAD_FOLDER, new_filename)
        os.rename(old_path, new_path)
        print(f"✅ File downloaded and saved as: {new_path}")

    except Exception as e:
        print(f"⚠️ Error during FnO data download: {e}")

def getMarketSnapshotData(driver):
    print("🔄 Navigating to Market Snapshot Downloader...")
    driver.get("https://trendlyne.com/tools/data-downloader/market-snapshot-excel/")
    time.sleep(5)

    try:
        download_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'DOWNLOAD')]"))
        )
        download_button.click()
        print("📥 Market Snapshot download initiated...")

        print("⏳ Waiting 10 seconds for file to download...")
        time.sleep(10)

        files = [f for f in os.listdir(CUSTOM_DOWNLOAD_FOLDER) if f.endswith(".csv")]
        if not files:
            print("❌ No CSV found in custom folder.")
            return

        files.sort(key=lambda x: os.path.getctime(os.path.join(CUSTOM_DOWNLOAD_FOLDER, x)), reverse=True)
        latest_file = files[0]

        timestamp = datetime.now().strftime("%Y-%m-%d")
        new_filename = f"market_snapshot_{timestamp}.csv"
        old_path = os.path.join(CUSTOM_DOWNLOAD_FOLDER, latest_file)
        new_path = os.path.join(CUSTOM_DOWNLOAD_FOLDER, new_filename)
        os.rename(old_path, new_path)
        print(f"✅ File downloaded and saved as: {new_path}")

    except Exception as e:
        print(f"⚠️ Error during Market Snapshot data download: {e}")

from bs4 import BeautifulSoup
import pandas as pd
import os
import time

def getTrendlyneForecasterData(driver):
    urls = {
        "High Bullishness": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/consensus_highest_bullish-above-0/",
        "High Bearishness": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/consensus_highest_bearish-above-0/",
        "Highest Forward 12Mth Upside %": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/consensus_highest_upside-above-0/",
        "Highest Forward Annual EPS Growth": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/eps_annual_growth-above-0/",
        "Lowest Forward Annual EPS Growth": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/eps_annual_growth-below-0/",
        "Highest Forward Annual Revenue Growth": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/revenue_annual_growth-above-0/",
        "Highest 3Mth Analyst Upgrades": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/consensus_analyst_upgrade-above-0/",
        "Highest Forward Annual Capex Growth": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/consensus_highest_capex-above-0/",
        "Highest Dividend Yield": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/consensus_highest_dps-above-0/",
        "Beat Annual Revenue Estimates": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/revenue-annual-surprise-above-0/",
        "Missed Annual Revenue Estimates": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/revenue-annual-surprise-below-0/",
        "Beat Quarter Revenue Estimates": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/revenue-quarter-surprise-above-0/",
        "Missed Quarter Revenue Estimates": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/revenue-quarter-surprise-below-0/",
        "Beat Annual Net Income Estimates": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/net-income-annual-surprise-above-0/",
        "Missed Annual Net Income Estimates": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/net-income-annual-surprise-below-0/",
        "Beat Quarter Net Income Estimates": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/net-income-quarter-surprise-above-0/",
        "Missed Quarter Net Income Estimates": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/net-income-quarter-surprise-below-0/",
        "Beat Annual EPS Estimates": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/eps-annual-surprise-above-0/",
        "Missed Annual EPS Estimates": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/eps-annual-surprise-below-0/",
        "Beat Quarter EPS Estimates": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/eps-quarter-surprise-above-0/",
        "Missed Quarter EPS Estimates": "https://trendlyne.com/equity/consensus-estimates/dashboard/forecaster/eps-quarter-surprise-below-0/"
    }

    output_dir = os.path.join(os.path.dirname(__file__), "trendlynedata")
    os.makedirs(output_dir, exist_ok=True)

    for label, url in urls.items():
        print(f"Fetching: {label}")
        driver.get(url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find("table", class_="trendlyne-screener-table")
        if not table:
            print(f"Table not found on {label}")
            continue

        headers = [th.text.strip() for th in table.find("thead").find_all("th")]
        rows = []
        for tr in table.find("tbody").find_all("tr"):
            row = [td.get_text(strip=True) for td in tr.find_all("td")]
            rows.append(row)

        df = pd.DataFrame(rows, columns=headers)
        safe_label = label.replace(" ", "_").replace("%", "pct").replace("/", "_")
        file_path = os.path.join(output_dir, f"trendlyne_{safe_label}.csv")
        df.to_csv(file_path, index=False)
        print(f"Saved {file_path}")





def getTrendlyneAnalytsSummary(driver, url="https://trendlyne.com/equity/consensus-estimates/533/HDFCBANK/hdfc-bank-ltd/"):
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    stockname = url.rstrip("/").split("/")[-1].replace("-", "_")
    base_folder = os.path.join(os.path.dirname(__file__), "trendlynedata", stockname)
    filename = f"{stockname}_analysts_summary.csv"

    os.makedirs(base_folder, exist_ok=True)
    filepath = os.path.join(base_folder, filename)

    data = {"Stock": stockname}

    try:
        share_card = soup.find("h3", string=re.compile("Share price target", re.I)).find_parent("div", class_="consensus-card")
        data["Current Price"] = share_card.find("div", class_="marker-1").find("div", class_="fw500 price").text.strip()
        data["Avg Estimate"] = share_card.find("div", class_="marker-color-2").find("div", class_="fw500 price").text.strip()
        data["Low Estimate"] = share_card.find("div", class_="low-estimate").find("div", class_="fw500 price").text.strip()
        data["High Estimate"] = share_card.find("div", class_="high-estimate").find("div", class_="fw500 rightAlgn price").text.strip()
        data["Upside %"] = re.search(r"upside of (.*?)\%?", share_card.text).group(1).strip() + "%"
    except Exception as e:
        print("Share price forecast extraction error:", e)

    try:
        eps_card = soup.find("h3", string=re.compile("EPS forecast", re.I)).find_parent("div", class_="consensus-card")
        data["EPS Insight"] = eps_card.find("h4", class_="consensus-heading").text.strip()
    except Exception as e:
        print("EPS insight extraction error:", e)

    try:
        rec_card = soup.find("h3", string=re.compile("Consensus Recommendation", re.I)).find_parent("div", class_="consensus-card")
        analyst_text = rec_card.find("div", class_="subtitle").text.strip()
        rec_text = rec_card.find("div", class_="insight-title").text.strip()
        data["Analyst Count"] = re.search(r"\d+", analyst_text).group()
        data["Recommendation"] = rec_text
    except Exception as e:
        print("Recommendation extraction error:", e)

    # Transpose and write
    transposed_data = [{"Variable": k, "Value": v} for k, v in data.items()]
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Variable", "Value"])
        writer.writeheader()
        writer.writerows(transposed_data)

    print(f"✅ Saved analyst summary to: {filepath}")



def getReportsFrom(driver, url="https://trendlyne.com/research-reports/stock/533/HDFCBANK/hdfc-bank-ltd/", download_dir="/tmp/trendlyne_downloads"):
    os.makedirs(download_dir, exist_ok=True)
    print(f"✅ Chrome download path set to: {download_dir}")

    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find("table", {"id": "brokerTable"})
    if not table:
        print("❌ Broker reports table not found.")
        return

    tbody = table.find("tbody", {"id": "allreportsbody"})
    rows = tbody.find_all("tr", {"role": "row"})

    stock_slug = url.rstrip("/").split("/")[-1]
    stock_folder = stock_slug.replace("-", "_").lower()
    base_dir = os.path.join("trendlynedata", stock_folder, "reports")
    os.makedirs(base_dir, exist_ok=True)
    summary_csv_path = os.path.join("trendlynedata", stock_folder, "reportssummary.csv")

    headers = [
        "Date", "Stock", "Author", "LTP", "Target", 
        "Price at Reco (Change)", "Upside (%)", "Type", "PDF Link", "Post Link"
    ]
    rows_data = []

    cutoff_date = datetime.now() - timedelta(days=183)

    for row in rows:
        cols = row.find_all("td")
        if not cols or len(cols) < 10:
            continue

        date_str = cols[1].text.strip()
        try:
            report_date = datetime.strptime(date_str, "%d %b %Y")
        except ValueError:
            continue

        if report_date < cutoff_date:
            continue

        stock = cols[2].text.strip()
        author = cols[3].text.strip()
        ltp = cols[4].text.strip()
        target = cols[5].text.strip()
        reco_price = cols[6].text.strip().replace("\n", " ")
        upside = cols[7].text.strip()
        rating = cols[8].text.strip()

        report_links = cols[9].find_all("a")
        pdf_link = ""
        post_link = ""
        for link in report_links:
            label = link.text.strip().lower()
            href = link.get("href", "")
            if "pdf" in label and "loginmodal" not in href:
                pdf_link = urljoin("https://trendlyne.com", href)
            elif "post" in label:
                post_link = urljoin("https://trendlyne.com", href)

        if pdf_link:
            try:
                # Clean up any old files
                for f in os.listdir(download_dir):
                    if f.endswith(".crdownload") or f.endswith(".pdf"):
                        os.remove(os.path.join(download_dir, f))

                before_files = set(os.listdir(download_dir))

                # Open the PDF in a new tab
                original_window = driver.current_window_handle
                driver.execute_script("window.open(arguments[0]);", pdf_link)
                time.sleep(1)

                new_window = [w for w in driver.window_handles if w != original_window][0]
                driver.switch_to.window(new_window)
                time.sleep(5)

                # Switch back and close the download tab
                driver.switch_to.window(original_window)
                driver.switch_to.window(new_window)
                driver.close()
                driver.switch_to.window(original_window)

                # Wait for PDF file to download
                downloaded_pdf = None
                for _ in range(30):
                    files_now = set(os.listdir(download_dir))
                    new_files = files_now - before_files
                    pdf_files = [f for f in new_files if f.endswith(".pdf")]
                    if pdf_files:
                        downloaded_pdf = pdf_files[0]
                        break
                    time.sleep(1)

                if downloaded_pdf:
                    src = os.path.join(download_dir, downloaded_pdf)
                    dest = os.path.join(base_dir, downloaded_pdf)
                    if os.path.exists(src):
                        print(f"📁 Moving {src} → {dest}")
                        shutil.move(src, dest)
                    else:
                        print(f"⚠️ File {src} does not exist, skipping move.")
                else:
                    print(f"⚠️ No PDF downloaded for: {pdf_link}")

            except Exception as e:
                print(f"❌ Error downloading PDF from browser: {pdf_link} | {e}")

        rows_data.append([
            date_str, stock, author, ltp, target, reco_price, upside, rating, pdf_link, post_link
        ])

    with open(summary_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows_data)

    
    print(f"✅ Downloaded {len(rows_data)} reports for {stock_folder}")



def move_pdfs_to_hdfc_reports(src_root="trendlynedata", dest_subpath="hdfc_bank_ltd/reports"):
    dest_path = os.path.join(src_root, dest_subpath)
    os.makedirs(dest_path, exist_ok=True)

    moved = 0
    for root, _, files in os.walk(src_root):
        for file in files:
            if file.lower().endswith(".pdf"):
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_path, file)

                # Avoid moving from destination to itself
                if os.path.abspath(src_file) == os.path.abspath(dest_file):
                    continue

                try:
                    shutil.move(src_file, dest_file)
                    print(f"📦 Moved: {src_file} → {dest_file}")
                    moved += 1
                except Exception as e:
                    print(f"❌ Failed to move {src_file}: {e}")

    print(f"✅ Moved {moved} PDF(s) to {dest_path}")



# --- MAIN DRIVER CODE ---
if __name__ == "__main__":
    try:
        login_to_trendlyne(driver)
        getFnOData(driver)
        getMarketSnapshotData(driver)
        getTrendlyneForecasterData(driver)
        getTrendlyneAnalytsSummary(driver)
        driver = init_driver_with_download("trendlynedata/tmp_downloads")
        getReportsFrom(driver)
        move_pdfs_to_hdfc_reports()
    finally:
        input("Press Enter to close browser...")
        driver.quit()
