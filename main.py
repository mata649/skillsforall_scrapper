from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

import sys, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

driver = None

def get_module_and_sections(url:str) -> list[list[str]]:
    logger.info(f"getting html from {url}")
    driver.get(url)
    logger.info("Getting modules and sections")
    
    modules = driver.find_elements(by=By.CLASS_NAME, value="nodeName--AZrtx")
    logger.info(f"Found {len(modules)} modules")
    modules = [i.text for i in modules if i.text != ""]
    
    sections = driver.find_elements(by=By.CLASS_NAME, value="subModuleName--NhmoF") 
    logger.info(f"Found {len(sections)} sections")
    sections = [i.get_attribute("title") for i in sections if i.get_attribute("title") != ""]
    
    return [modules, sections]

def is_url_a_valid_course(url: str) -> bool:
    possible_starts = [
        "https://skillsforall.com/es/course/",
        "skillsforall.com/es/course/",
        "https://skillsforall.com/en/course/",
        "skillsforall.com/en/course/",
    ]
    return url.startswith(tuple(possible_starts))
        
def match_modules_and_sections(modules: list[str], sections: list[str]) -> dict[str, list[str]]:
    logger.info("Matching modules and sections")
    result = {}
    for module in modules:
        result[module] = []
        for section in sections:
            if section.startswith(module.split(" ")[2]):
                result[module].append(section)
    return result

def run(urls: list[str]):
    
    for url in urls:
        if not is_url_a_valid_course(url):
           logger.warning(f"{url} is not a valid course url")
           continue
        [modules, sections] = get_module_and_sections(url)
        result = match_modules_and_sections(modules, sections)
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(f"{url}\n")
            for module, sections in result.items():
                f.write(f"{module}\n")
                for section in sections:
                    f.write(f"\t{section}\n")
            f.write("\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error("at least one url is required")
        sys.exit(1)
    driver = Chrome()
    driver.implicitly_wait(3)
    run(sys.argv[1:])