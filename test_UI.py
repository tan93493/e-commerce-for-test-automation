from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from selenium.webdriver.chrome.options import Options
import unittest
import time
import random
import string
import os
import logging

# Cấu hình logging cơ bản
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def random_email():
    letters = string.ascii_lowercase
    name = ''.join(random.choice(letters) for _ in range(8))
    return f"{name}@example.com"

def random_password():
    digits = string.digits
    return ''.join(random.choice(digits) for _ in range(8))

class AuthTests(unittest.TestCase):
    email = None
    password = None

    def setUp(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.frontend_url = os.getenv('FRONTEND_URL', "https://e-commerce-for-testing.onrender.com/")
        logging.info(f"Sử dụng frontend URL: {self.frontend_url}")

    def tearDown(self):
        self.driver.quit()

    def test_1_register_success(self):
        driver = self.driver
        driver.get(self.frontend_url)

        AuthTests.email = random_email()
        AuthTests.password = random_password()

        logging.info(f"Random email: {AuthTests.email}")
        logging.info(f"Random password: {AuthTests.password}")

        try:
            register_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Register')]"))
            )
            register_btn.click()
            logging.info("PASS: Click nút Register thành công")
            time.sleep(1)
        except Exception as e:
            logging.error(f"FAIL: Click nút Register không thành công: {e}")
            self.fail("Không thể click nút Register")

        try:
            email_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "email"))
            )
            email_input.clear()
            email_input.send_keys(AuthTests.email)
            logging.info("PASS: Nhập email thành công")
            time.sleep(1)
        except Exception as e:
            logging.error(f"FAIL: Nhập email không thành công: {e}")
            self.fail("Không thể nhập email")

        try:
            password_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "password"))
            )
            password_input.clear()
            password_input.send_keys(AuthTests.password)
            logging.info("PASS: Nhập password thành công")
            time.sleep(1)
        except Exception as e:
            logging.error(f"FAIL: Nhập password không thành công: {e}")
            self.fail("Không thể nhập password")

        try:
            confirm_password_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "passwordConfirm"))
            )
            confirm_password_input.clear()
            confirm_password_input.send_keys(AuthTests.password)
            logging.info("PASS: Nhập lại password thành công")
            time.sleep(1)
        except Exception as e:
            logging.error(f"FAIL: Nhập lại password không thành công: {e}")
            self.fail("Không thể nhập lại password")

        try:
            signup_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Sign Up')]")
            signup_btn.click()
            logging.info("PASS: Click nút Sign Up thành công")
            time.sleep(1)
        except Exception as e:
            logging.error(f"FAIL: Click nút Sign Up không thành công: {e}")
            self.fail("Không thể click nút Sign Up")

        try:
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert_text = alert.text
            logging.info(f"Alert thông báo: {alert_text}")
            alert.accept()
            logging.info("PASS: Đã xử lý alert thành công")
            time.sleep(1)
        except TimeoutException:
            logging.warning("WARN: Không thấy alert sau khi đăng ký.")
        except NoAlertPresentException:
            logging.error("FAIL: Alert không tồn tại khi mong đợi.")
            self.fail("Alert không tồn tại")

    def test_2_login_success(self):
        driver = self.driver
        driver.get(self.frontend_url)
        time.sleep(1)

        if not AuthTests.email or not AuthTests.password:
            logging.warning("Email/Password chưa được tạo từ test đăng ký.")
            self.skipTest("Cần chạy test đăng ký trước để có tài khoản.")
            return

        try:
            login_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]"))
            )
            login_btn.click()
            logging.info("PASS: Click nút Login thành công")
            time.sleep(1)
        except Exception as e:
            logging.error(f"FAIL: Click nút Login không thành công: {e}")
            self.fail("Không thể click nút Login")

        try:
            mail_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "email"))
            )
            mail_input.clear()
            mail_input.send_keys(AuthTests.email)
            logging.info("PASS: Nhập email để đăng nhập thành công")
            time.sleep(1)
        except Exception as e:
            logging.error(f"FAIL: Nhập email đăng nhập không thành công: {e}")
            self.fail("Không thể nhập email đăng nhập")

        try:
            pass_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "password"))
            )
            pass_input.clear()
            pass_input.send_keys(AuthTests.password)
            logging.info("PASS: Nhập password để đăng nhập thành công")
            time.sleep(1)
        except Exception as e:
            logging.error(f"FAIL: Nhập password đăng nhập không thành công: {e}")
            self.fail("Không thể nhập password đăng nhập")

        try:
            submit_btn = driver.find_element(By.XPATH, "//form[.//input[@name='email']]//button[@type='submit']")
            submit_btn.click()
            logging.info("PASS: Click nút Submit đăng nhập thành công")
            time.sleep(2)
        except Exception as e:
            logging.error(f"FAIL: Submit đăng nhập thất bại: {e}")
            self.fail("Submit đăng nhập thất bại")

    def test_3_logout_success(self):
        driver = self.driver
        driver.get(self.frontend_url)
        time.sleep(1)

        if not AuthTests.email or not AuthTests.password:
            logging.warning("Email/Password chưa có. Bỏ qua test logout.")
            self.skipTest("Cần có tài khoản đã đăng nhập trước.")
            return

        try:
            login_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]"))
            )
            login_btn.click()
            logging.info("PASS: Click nút Login thành công")
            time.sleep(1)
        except Exception as e:
            logging.error(f"FAIL: Không thể click nút Login: {e}")
            self.fail("Không thể click nút Login")

        try:
            email_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "email"))
            )
            email_input.clear()
            email_input.send_keys(AuthTests.email)

            password_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "password"))
            )
            password_input.clear()
            password_input.send_keys(AuthTests.password)

            submit_btn = driver.find_element(By.XPATH, "//form[.//input[@name='email']]//button[@type='submit']")
            submit_btn.click()
            logging.info("PASS: Đăng nhập thành công")
            time.sleep(2)
        except Exception as e:
            logging.error(f"FAIL: Không thể đăng nhập: {e}")
            self.fail("Đăng nhập thất bại")

        try:
            profile_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Profile')]"))
            )
            profile_btn.click()
            logging.info("PASS: Click nút Profile thành công")
            time.sleep(2)
        except Exception as e:
            logging.error(f"FAIL: Không thể click nút Profile: {e}")
            self.fail("Không thể vào trang Profile")

        try:
            logout_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Logout')]"))
            )
            logout_btn.click()
            logging.info("PASS: Click nút Logout thành công")
            time.sleep(2)
        except Exception as e:
            logging.error(f"FAIL: Không thể click nút Logout: {e}")
            self.fail("Không thể Logout")

        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//button[contains(text(),'Login')]"))
            )
            logging.info("PASS: Đăng xuất thành công, nút Login hiển thị lại.")
        except Exception as e:
            logging.error(f"FAIL: Nút Login không hiển thị sau khi logout: {e}")
            self.fail("Đăng xuất thất bại")

    def test_4_add_and_remove_from_basket_success(self):
        driver = self.driver
        driver.get(self.frontend_url)
        time.sleep(1)

        if not AuthTests.email or not AuthTests.password:
            logging.warning("Email/Password chưa có. Bỏ qua test.")
            self.skipTest("Cần có tài khoản để tiếp tục.")
            return
        # Bước 1: Đăng nhập
        try:
            login_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]"))
            )
            login_btn.click()
            time.sleep(1)

            email_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "email"))
            )
            email_input.clear()
            email_input.send_keys(AuthTests.email)

            password_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "password"))
            )
            password_input.clear()
            password_input.send_keys(AuthTests.password)

            submit_btn = driver.find_element(By.XPATH, "//form[.//input[@name='email']]//button[@type='submit']")
            submit_btn.click()
            logging.info("PASS: Đăng nhập thành công")
            time.sleep(2)
        except Exception as e:
            logging.error(f"FAIL: Không thể đăng nhập: {e}")
            self.fail("Đăng nhập thất bại")

        # Bước 2: Nhấn vào thẻ <a> có nội dung "eCommerce" để về trang chủ
        try:
            ecommerce_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'eCommerce')]"))
            )
            ecommerce_link.click()  # Nhấn vào thẻ <a> với nội dung "eCommerce"
            logging.info("PASS: Đã quay lại trang chủ")
            time.sleep(2)
        except Exception as e:
            logging.error(f"FAIL: Không thể quay lại trang chủ bằng thẻ <a>: {e}")
            self.fail("Không thể quay lại trang chủ")

        # Bước 3: Click "Add to Basket"
        try:
            add_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add to Basket')]"))
            )
            add_btn.click()
            logging.info("PASS: Click 'Add to Basket' thành công")
            time.sleep(1)
        except Exception as e:
            logging.error(f"FAIL: Không thể thêm sản phẩm vào giỏ hàng: {e}")
            self.fail("Không thể click 'Add to Basket'")

        # Bước 4: Click "Basket"
        try:
            basket_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Basket')]"))
            )
            basket_btn.click()
            logging.info("PASS: Click nút 'Basket' thành công")
            time.sleep(1)
        except Exception as e:
            logging.error(f"FAIL: Không thể mở giỏ hàng: {e}")
            self.fail("Không thể click 'Basket'")

        # Bước 5: Click "Remove from Basket"
        try:
            remove_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Remove from Basket')]"))
            )
            remove_btn.click()
            logging.info("PASS: Click 'Remove from Basket' thành công")
            time.sleep(1)
        except Exception as e:
            logging.error(f"FAIL: Không thể xóa sản phẩm khỏi giỏ hàng: {e}")
            self.fail("Không thể click 'Remove from Basket'")

if __name__ == "__main__":
    unittest.main(verbosity=2)
