import time
from playwright.sync_api import sync_playwright
import logging

def check_1und1(username, password):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            logging.info("Öffne Login-Seite...")
            page.goto('https://account.1und1.de/')
            
            logging.info("Führe Login durch...")
            page.fill('#login-form-user', username)
            page.fill('#login-form-password', password)
            
            page.click('#login-button')
            logging.info("Login erfolgreich")
            
            logging.info("Cookies ablehnen...")
            try:
                page.click('#consent_wall_optout')
            except:
                logging.info("Cookie-Banner nicht vorhanden oder bereits geschlossen.")

            logging.info("Weiterleitung zu Verbrauchsübersicht...")
            page.goto('https://control-center.1und1.de/usages.html')
            
            time.sleep(3)
            
            page.wait_for_selector('div[data-testid="usage-volume-used"] strong')
            used_data = page.locator('div[data-testid="usage-volume-used"] strong').nth(-1).text_content()
            if used_data:
                logging.info(f"Verbrauchte Daten: {used_data}")
            else:
                logging.warning("Verbrauchsdaten nicht gefunden.")
            
            button = page.locator('button:has-text("+1 GB")')
            if button:
                is_disabled = button.get_attribute('disabled') is not None
                if is_disabled:
                    logging.info("Button gefunden, aber er ist deaktiviert.")
                else:
                    logging.info("Button gefunden und aktiv. Versuche zu klicken...")
                    button.click()
                    logging.info("Button erfolgreich geklickt.")
                    time.sleep(3)
                    confirm_button = page.locator('button:has-text("Ok")')
                    if confirm_button:
                        confirm_button.click()
                        logging.info("Bestätigungsdialog erfolgreich geschlossen.")
                    
            else:
                logging.warning("Button '+1 GB' nicht gefunden.")

            logging.info("Schließe Browser.")
            browser.close()
            
    except Exception as e:
        logging.error(f"Fehler bei der Ausführung: {str(e)}")