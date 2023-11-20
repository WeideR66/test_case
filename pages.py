from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep
from settings import DOWNLOAD_ROOT
from typing import Tuple, List
from locators import *


class Base:
    base_url: str
    download_root = DOWNLOAD_ROOT
    
    def __init__(self, driver: WebDriver) -> None:
        self.br = driver

    def go_to_page(self) -> None:
        self.br.get(self.base_url)
        
    def go_to_url(self, url: str) -> None:
        self.br.get(url)
    
    @property
    def get_current_url(self) -> str:
        return self.br.current_url
    
    @property
    def get_title(self) -> str:
        return self.br.title
        
    def find_element(self, locator: Tuple[str, str], timeout: float = 5.0) -> WebElement:
        return WebDriverWait(self.br, timeout).until(
            EC.presence_of_element_located(locator),
            message=f"Не удалось найти элемент по локатору {locator}"
        )
        
    def find_elements(self, locator: Tuple[str, str], timeout: float = 5.0) -> List[WebElement]:
        return WebDriverWait(self.br, timeout).until(
            EC.presence_of_all_elements_located(locator),
            message=f"Не удалось найти элементы по локатору {locator}"
        )
        
    def staleness_of(self, element: WebElement, timeout: float = 5.0) -> WebElement | bool:
        return WebDriverWait(self.br, timeout).until(
            EC.staleness_of(element),
            message=f"Элемент не стареет"
        )


class SbisPage(Base):
    base_url = "https://sbis.ru/"
    
    def go_to_contact_page(self) -> 'SbisContacts':
        elem = self.find_element(SbisPageLocators.sbis_contact)
        elem.click()
        return SbisContacts(self.br)
        
    def go_to_download_page(self) -> 'SbisDownload':
        url = self.find_element(SbisPageLocators.sbis_download).get_attribute("href")
        self.go_to_url(url)
        return SbisDownload(self.br)


class SbisContacts(Base):
    base_url = "https://sbis.ru/contacts"
    
    def click_tensor_banner(self) -> 'Tensor':
        elem = self.find_element(SbisContactsLocators.sbis_tensor_banner)
        elem.click()
        return Tensor(self.br)
        
    def get_current_region(self) -> tuple[WebElement, str]:
        elem = self.find_element(SbisContactsLocators.sbis_region)
        return elem, elem.text
    
    def get_current_partners_names(self) -> tuple[list[WebElement], list[str]]:
        elem = self.find_elements(SbisContactsLocators.sbis_partners)
        names = [obj.text for obj in elem]
        return elem, names
    
    def change_region(self, region: str, old_elem: WebElement) -> str:
        self.find_element(SbisContactsLocators.sbis_region).click()
        new = self.find_element(SbisContactsLocators.sbis_change_region(region))
        new_region_number = new.text.split()[0]
        new.click()
        self.staleness_of(old_elem)
        return new_region_number


class SbisDownload(Base):
    base_url = "https://sbis.ru/download?tab=ereport&innerTab=ereport25"
    
    def download_plugin(self) -> str:
        if not os.path.exists(self.download_root):
            os.mkdir(self.download_root)
        link = self.find_element(SbisDownloadLocators.sbis_plugin_download_link).get_attribute("href")
        self.go_to_url(link)
        tmp_files = [file for file in os.listdir(self.download_root) if file.endswith((".tmp", ".crdownload"))]
        while tmp_files:
            tmp_files = [file for file in os.listdir(self.download_root) if file.endswith((".tmp", ".crdownload"))]
            sleep(1)
        downloaded_file = sorted(
            [(file, os.path.getmtime(os.path.join(self.download_root, file))) for file in os.listdir(self.download_root)],
            reverse=True,
            key=lambda x: x[-1]
        )[0]
        return downloaded_file[0]   
        

class Tensor(Base):
    base_url = "https://tensor.ru/"
    
    def switch_to_tensor_page(self) -> None:
        success = False
        for handles in self.br.window_handles:
            self.br.switch_to.window(handles)
            if self.base_url == self.br.current_url:
                success = True
                break
        if not success:
            raise NoSuchWindowException(f"Окно {self.base_url} не открыто")
    
    def get_strength_block(self) -> tuple[WebElement, str]:
        elem = self.find_element(TensorLocators.tensor_strength_block)
        text = elem.find_element(*TensorLocators.tensor_strength_block_title).text
        return elem, text
    
    def go_to_tensor_about_page(self) -> 'TensorAbout':
        url = self.find_element(TensorLocators.tensor_strength_block_more).get_attribute("href")
        self.go_to_url(url)
        return TensorAbout(self.br)


class TensorAbout(Base):
    base_url = "https://tensor.ru/about"
    
    def get_work_photos_params(self) -> list[tuple[str | None, str | None]]:
        items = self.find_elements(TensorAboutLocators.tensor_work_photos)
        return [(obj.get_attribute("width"), obj.get_attribute("height")) for obj in items]
