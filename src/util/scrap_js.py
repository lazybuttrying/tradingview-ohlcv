import time
import random
from playwright.sync_api import Page

def delay_randomized(seconds: int = 2):
    """랜덤한 짧은 딜레이 (휴먼 인터랙션 시뮬레이션용)"""
    time.sleep(random.uniform(0.5, seconds))

def wait_then_click(page: Page, selector: str):
    page.wait_for_selector(selector)
    delay_randomized()
    page.click(selector)

def has_high_zindex_elements(page: Page, threshold=3) -> bool:
    return page.evaluate(f"""
        () => {{
            const elements = Array.from(document.querySelectorAll('*')).filter(el => {{
                const z = parseInt(getComputedStyle(el).zIndex);
                return !isNaN(z) && z > {threshold};
            }});
            return elements.length > 0;
        }}
    """)


def remove_high_zindex_elements(page: Page, threshold=3):
    print("⚠️ Removing high z-index elements...")
    JS = f"""
        const elements = Array.from(document.querySelectorAll('*')).filter(el => {{
            const z = parseInt(getComputedStyle(el).zIndex);
            return !isNaN(z) && z > {threshold};
        }});
        elements.forEach(el => el.remove());
    """
    page.evaluate(JS)
