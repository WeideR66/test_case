from selenium.webdriver.common.by import By
    

class SbisPageLocators:
    sbis_contact = (By.XPATH, '//a[@class="sbisru-Header__menu-link sbisru-Header__menu-link--hover"][contains(text(), "Контакты")]')
    sbis_download = (By.XPATH, '//div[@class="sbisru-Footer__container"]//a[contains(text(), "Скачать СБИС")]')


class SbisContactsLocators:
    sbis_tensor_banner = (By.XPATH, '//a[@class="sbisru-Contacts__logo-tensor mb-12"]')
    sbis_region = (By.XPATH, '//span[@class="sbis_ru-Region-Chooser__text sbis_ru-link"]')
    sbis_partners = (By.XPATH, '//div[@class="sbisru-Contacts-List__col-1"]')
    sbis_change_region = lambda region: (By.XPATH, f'//ul[@class="sbis_ru-Region-Panel__list"]/li/span[@title="{region}"]')
    


class SbisDownloadLocators:
    sbis_plugin_download_link = (By.XPATH, '//a[@class="sbis_ru-DownloadNew-loadLink__link js-link"][contains(text(), "Скачать (Exe 3.66 МБ) ")]')


class TensorLocators:
    tensor_strength_block = (By.XPATH, '//div[@class="tensor_ru-Index__block4-content tensor_ru-Index__card"]')
    tensor_strength_block_title = (By.XPATH, tensor_strength_block[-1] + "/p")
    tensor_strength_block_more = (By.XPATH, tensor_strength_block[-1] + "/*/a")


class TensorAboutLocators:
    tensor_work_photos = (By.XPATH, '//div[@class="tensor_ru-About__block3-image-wrapper"]/img')