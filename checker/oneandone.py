import time
from playwright.sync_api import sync_playwright
import logging
from utils.screenshot import take_screenshot

def check_1und1(username, password, CHECK_INTERVAL, tariff_id=""):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    browser = None
    page = None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            logging.info("Öffne Login-Seite...")
            page.goto('https://account.1und1.de/')
            take_screenshot(page, "before_login", "1und1")
            logging.info("Führe Login durch...")
            page.fill('#login-form-user', username)
            page.fill('#login-form-password', password)
            page.click('#login-button')
            
            logging.info("Warte auf Roboter-Verifizierung...")
            try:
                robot_button = page.wait_for_selector('button.button-primary.button-access:has-text("E-Mail senden")', timeout=5000)
                if robot_button and robot_button.is_visible():
                    logging.info("Roboter-Verifizierung erkannt")
                    logging.info("Sende Verifizierungs-Email...")
                    robot_button.click()
                    
                    logging.info("Bitte öffnen Sie die Verifizierungs-Email und bestätigen Sie den Link.")
                    logging.info("Der Prozess wird in 60 Sekunden neu gestartet.")
                    
                    time.sleep(60)
                    
                    if browser:
                        browser.close()
                    return
            except Exception as e:
                logging.info(f"Keine Roboter-Verifizierung erkannt, gehe weiter...")
                
            take_screenshot(page, "after_login", "1und1")
            
            logging.info("Login erfolgreich")
            
            take_screenshot(page, "cookies_page", "1und1")
            
            logging.info("Cookies ablehnen...")
            try:
                page.click('#consent_wall_optout')
            except:
                logging.info("Cookie-Banner nicht vorhanden oder bereits geschlossen.")

            while True:
                try:
                    logging.info("Lade Verbrauchsübersicht...")
                    take_screenshot(page, "usage_page_before", "1und1")
                    page.goto('https://control-center.1und1.de/usages.html')
                    time.sleep(5)
                    take_screenshot(page, "usage_page_after", "1und1")
                    logging.info("Buchungseite geladen, warte 5 Sekunden...")
                    
                    if not tariff_id:
                        extract_tariff_info(page)
                    
                    if tariff_id:
                        logging.info(f"Suche nach Tarif mit ID: {tariff_id}")
                        try:
                            page.evaluate(f'document.getElementById("{tariff_id}").scrollIntoView()')
                            logging.info(f"Tarif mit ID {tariff_id} gefunden und fokussiert")
                            
                            tariff_section = page.locator(f'#usages div[id="{tariff_id}"]').first
                            if tariff_section:
                                parent_section = page.locator(f'#usages div[id="{tariff_id}"]').locator('xpath=..').first
                                if parent_section:
                                    button = parent_section.locator('button:has-text("+1 GB")')
                                else:
                                    logging.warning(f"Konnte den Container für Tarif {tariff_id} nicht finden")
                                    button = page.locator('button:has-text("+1 GB")')
                            else:
                                logging.warning(f"Tarif mit ID {tariff_id} nicht gefunden, verwende Standard-Suche")
                                button = page.locator('button:has-text("+1 GB")')
                        except Exception as e:
                            logging.warning(f"Fehler beim Suchen des Tarifs: {str(e)}")
                            button = page.locator('button:has-text("+1 GB")')
                    else:
                        try:
                            page.wait_for_selector('div[data-testid="usage-volume-used"] strong', timeout=10000)
                            used_data = page.locator('div[data-testid="usage-volume-used"] strong').nth(-1).text_content()
                            if used_data:
                                logging.info(f"Verbrauchte Daten: {used_data}")
                            else:
                                logging.warning("Verbrauchsdaten nicht gefunden.")
                        except TimeoutError:
                            logging.warning("Timeout beim Warten auf Verbrauchsdaten.")
                        
                        button = page.locator('button:has-text("+1 GB")')
                    
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
                                take_screenshot(page, "after_booking", "1und1")
                    else:
                        logging.warning("Button '+1 GB' nicht gefunden.")

                    logging.info(f"Warte {CHECK_INTERVAL} Sekunden bis zur nächsten Überprüfung...")
                    time.sleep(CHECK_INTERVAL)

                except Exception as e:
                    logging.error(f"Fehler während der Überprüfung: {str(e)}")
                    logging.error(page.content())
                    if browser:
                        browser.close()
                    return

    except Exception as e:
        logging.error(f"Fehler bei der Ausführung: {str(e)}")
        if browser:
            browser.close()

def extract_tariff_info(page):
    """
    Extract and log information about all available tariffs on the page.
    This helps users identify the correct tariff ID to use in the configuration.
    """
    try:
        tariff_sections = page.locator('div._usageBoxes-cm__scrollMarginTop___lnens').all()
        
        if not tariff_sections:
            logging.warning("Keine Tarife auf der Seite gefunden.")
            return
        
        logging.info("=== Verfügbare Tarife ===")
        for section in tariff_sections:
            try:
                tariff_id = section.get_attribute('id')
                
                contract_header = page.locator(f'div[id="{tariff_id}"] + div._contractHeader-cm__headerContainer___QbYMh')
                
                tariff_name = contract_header.locator('h4[data-testid="contract-title"]').text_content()
                tariff_alias = contract_header.locator('div._contractHeader-cm__alias___kYK9s').text_content()
                
                logging.info(f"Tarif ID: {tariff_id}")
                logging.info(f"Name: {tariff_name}")
                logging.info(f"Alias: {tariff_alias}")
                logging.info("---")
            except Exception as e:
                logging.warning(f"Fehler beim Extrahieren der Tarifinformationen: {str(e)}")
        
        logging.info("Um einen bestimmten Tarif zu aktualisieren, setzen Sie die TARIFF_ID in der .env-Datei.")
    except Exception as e:
        logging.warning(f"Fehler beim Extrahieren der Tarifinformationen: {str(e)}")