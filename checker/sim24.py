from playwright.sync_api import sync_playwright
import logging
from utils.screenshot import take_screenshot

def check_sim24(username, password):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            logging.info("Öffne Login-Seite...")
            page.goto('https://service.sim24.de/mytariff/invoice/showGprsDataUsage')
            
            logging.info("Führe Login durch...")
            page.fill('input[name="UserLoginType[alias]"]', username)
            page.fill('input[name="UserLoginType[password]"]', password)
            
            page.click('a.c-button.submitOnEnter[title="Login"]')
            take_screenshot(page, "after_login", "sim24")
            
            logging.info("Deny Cookies...")
            consent_button = page.query_selector('#consent_wall_optout')
            if consent_button and consent_button.is_visible():
                consent_button.click()
            else:
                logging.info("Consent button not visible, skipping...")
            
            logging.info("Suche nach Button...")
            try:
                button = page.wait_for_selector('#ButtonBuchen-ChangeServiceType-showGprsDataUsage-0V5I3', timeout=10000)
                
                data_usage_bar = page.wait_for_selector('.dataUsageBar-info', timeout=10000)
                
                if data_usage_bar:
                    data_numbers = page.query_selector_all('.dataUsageBar-info-numbers')
                    if len(data_numbers) >= 2:
                        used_data_element = data_numbers[0].query_selector('.font-weight-bold')
                        total_data_element = data_numbers[1].query_selector('.l-txt-small')
                        
                        if used_data_element and total_data_element:
                            used_data = used_data_element.inner_text()
                            total_data = total_data_element.inner_text().replace('von', '').strip()
                            logging.info(f"Verbrauchte Daten: {used_data} von {total_data}")
                            take_screenshot(page, "usage_page", "sim24")
                        else:
                            logging.warning("Konnte Datenverbrauch-Elemente nicht finden")
                    else:
                        logging.warning("Nicht genügend dataUsageBar-info-numbers Elemente gefunden")
                
                if button:
                    is_disabled = button.get_attribute('disabled') is not None
                    
                    if is_disabled:
                        logging.info("Button gefunden, aber deaktiviert")
                    else:
                        logging.info("Button gefunden und aktiv - Klicke...")
                        button.click()
                        logging.info("Button erfolgreich geklickt")
                    
                        page.click('#ButtonAktivieren-ChangeServiceType-getChangeServiceInfo-1V5I3')
                        take_screenshot(page, "after_booking", "sim24")
                    
                        logging.info("Prozess erfolgreich beendet")
                        return
                else:
                    logging.warning("Button nicht gefunden")
                
            except Exception as e:
                logging.warning(f"Button nicht gefunden oder nicht klickbar: {str(e)}")
            
            logging.info("Schließe Browser")
            browser.close()
            
    except Exception as e:
        logging.error(f"Fehler bei der Ausführung: {str(e)}") 