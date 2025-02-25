from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class AttendanceScraper:
    def __init__(self):
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Initialize Chrome driver with necessary options"""
        print("Setting up Chrome driver...")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-logging')
        options.add_argument('--disable-notifications')
        options.add_argument('--blink-settings=imagesEnabled=false')  # Disable images
        options.page_load_strategy = 'eager'
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 5)  # Reduced timeout
        print("Chrome driver setup complete")
        
    def login(self, username, password):
        """Login to the VNRVJIET portal"""
        try:
            print("\nStarting login process...")
            print(f"Navigating to login page...")
            self.driver.get("https://automation.vnrvjiet.ac.in/eduprime3")
            time.sleep(3)
            
            # Take screenshot of login page
            self.driver.save_screenshot("login_page.png")
            print("Login page screenshot saved as 'login_page.png'")
            
            # Using XPath selectors
            username_xpath = "/html/body/section/form/div/div[1]/div[2]/div/input[1]"
            password_xpath = "/html/body/section/form/div/div[1]/div[2]/div/input[2]"
            login_button_xpath = "/html/body/section/form/div/div[1]/div[2]/div/input[3]"
            
            print("\nLocating username field...")
            username_field = self.wait.until(
                EC.presence_of_element_located((By.XPATH, username_xpath))
            )
            print("Username field found")
            
            print("Locating password field...")
            password_field = self.wait.until(
                EC.presence_of_element_located((By.XPATH, password_xpath))
            )
            print("Password field found")
            
            # Clear and fill fields
            print("\nFilling login form...")
            username_field.clear()
            time.sleep(1)
            username_field.send_keys(username)
            print(f"Username entered: {username}")
            
            password_field.clear()
            time.sleep(1)
            password_field.send_keys(password)
            print("Password entered")
            
            # Take screenshot of filled form
            self.driver.save_screenshot("filled_form.png")
            print("Filled form screenshot saved as 'filled_form.png'")
            
            print("\nLocating login button...")
            try:
                login_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, login_button_xpath))
                )
                print("Login button found")
                
                print("Attempting to click login button...")
                self.driver.execute_script("arguments[0].click();", login_button)
                print("Login button clicked")
                
                # Take screenshot after click
                time.sleep(2)
                self.driver.save_screenshot("after_click.png")
                print("Post-click screenshot saved as 'after_click.png'")
                
            except Exception as e:
                print(f"Error with login button: {str(e)}")
                return False
            
            print("\nWaiting for login to complete...")
            time.sleep(5)
            
            # Take screenshot of result
            self.driver.save_screenshot("login_result.png")
            print("Login result screenshot saved as 'login_result.png'")
            
            print("\nChecking if login was successful...")
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#attp"))
                )
                print("Login successful - Found dashboard element")
                return True
            except TimeoutException:
                print("Login failed - Could not find dashboard element")
                print(f"Current URL: {self.driver.current_url}")
                print("Page source after login attempt:")
                print(self.driver.page_source[:500] + "...")
                return False
            
        except Exception as e:
            print(f"\nLogin error: {str(e)}")
            return False
            
    def get_attendance_data(self):
        """Extract attendance data from the portal"""
        try:
            print("\nStarting attendance data extraction...")
            time.sleep(2)
            
            # Click attendance button
            print("Looking for attendance button...")
            attendance_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#attp"))
            )
            print("Clicking attendance button...")
            self.driver.execute_script("arguments[0].click();", attendance_btn)
            
            # Wait for modal to appear
            print("Waiting for modal to appear...")
            modal = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#dynamicModal"))
            )
            print("Modal found")
            
            # Wait for modal header to confirm it's loaded
            print("Waiting for modal header...")
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#dynamicModal > div > div > div.modal-header"))
            )
            print("Modal header found")
            
            # Take screenshot of modal
            self.driver.save_screenshot("modal.png")
            print("Modal screenshot saved")
            
            # Wait for table to load
            print("Waiting for attendance table...")
            table_div = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 
                "#popattdiv > div > div:nth-child(2) > div > div > div"))
            )
            print("Table div found")
            
            # Get cumulative attendance from 12th row
            print("Looking for cumulative attendance...")
            cumulative_cell = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                "#popattdiv > div > div:nth-child(2) > div > div > div > table > tbody > tr:nth-child(12) > td:nth-child(3)"))
            )
            
            attendance_text = cumulative_cell.text
            print(f"Found cumulative attendance: {attendance_text}")
            
            # Parse attendance data (format: "146/204 (71.57%)")
            try:
                # Extract numbers before the parenthesis
                numbers = attendance_text.split('(')[0].strip()
                attended, total = map(int, numbers.split('/'))
                
                attendance_data = {
                    'attended': attended,  # 146
                    'total': total        # 204
                }
                print(f"Parsed attendance data: {attended}/{total}")
                
                return attendance_data
                
            except Exception as e:
                print(f"Error parsing attendance numbers: {str(e)}")
                print(f"Raw attendance text: {attendance_text}")
                return None
                
        except Exception as e:
            print(f"Attendance data error: {str(e)}")
            self.driver.save_screenshot("attendance_error.png")
            return None
            
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit() 