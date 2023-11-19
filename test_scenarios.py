import pytest
from settings import DOWNLOAD_ROOT
from selenium import webdriver
from pages import *


@pytest.fixture(scope="session")
def browser():
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": f"{DOWNLOAD_ROOT}",
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    br = webdriver.Chrome(options=options)
    yield br
    br.quit()
    
    
def test_first_scenario(browser):
    sbis = SbisPage(browser)
    sbis.go_to_page()
    sbis_contancts = sbis.go_to_contact_page()
    tensor = sbis_contancts.click_tensor_banner()
    tensor.switch_to_tensor_page()
    block, text = tensor.get_strength_block()
    assert block.is_displayed(), "Блок не отображен"
    assert text == "Сила в людях", "Отсутствует фраза 'Сила в людях'"
    tensor_about = tensor.go_to_tensor_about_page()
    assert tensor_about.base_url == tensor_about.get_current_url, f"Открылась другая страница - {tensor_about.get_current_url}"
    sizes = tensor_about.get_work_photos_params()
    assert len(set(sizes)) == 1, "Размеры фото не равны"
    

def test_second_scenario(browser):
    sbis = SbisPage(browser)
    sbis.go_to_page()
    sbis_contacts = sbis.go_to_contact_page()
    _, old_region_name = sbis_contacts.get_current_region()
    old_partners, old_partners_names = sbis_contacts.get_current_partners_names()
    assert old_region_name == "Республика Башкортостан", "Стартовый регион не верен"
    assert old_partners_names, "Нету списка партнеров"
    new_region = "Камчатский край"
    new_region_number = sbis_contacts.change_region(region=new_region, old_elem=old_partners[0])
    _, new_region_name = sbis_contacts.get_current_region()
    _, new_partners_names = sbis_contacts.get_current_partners_names()
    curr_url = sbis_contacts.get_current_url
    title = sbis_contacts.get_title
    assert new_region_name == new_region, f"Регион не изменился на '{new_region}'"
    assert new_partners_names[0] != old_partners_names[0], "Список партнеров не изменился"
    assert "Камчатский край" in title, "В тайтле нет текщуего региона"
    assert curr_url.split("/")[-1].startswith(new_region_number), "В URL не поменялся регион"
    

def test_third_scenario(browser):
    sbis = SbisPage(browser)
    sbis.go_to_page()
    sbis_download = sbis.go_to_download_page()
    file = sbis_download.download_plugin()
    file_path = os.path.join(DOWNLOAD_ROOT, file)
    assert os.path.exists(file_path), "Файл не скачался"
    file_size = round(os.stat(file_path).st_size / (1024 ** 2), 2)
    assert file_size == 3.66, "У файла другой размер"