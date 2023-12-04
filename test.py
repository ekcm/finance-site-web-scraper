from selenium import webdriver
import time

# capitalIQ link:
capitalIQUrl = "https://secure.signin.spglobal.com/sso/saml2/0oa1n9y64jc36qEBE1d8/app/spglobaliam_sp_1/exk1mregn1oWwP2NB1d8/sso/saml?RelayState=https%3A%2F%2Fwww.capitaliq.com%2FCIQDotNet%2Fsaml-sso.aspx"

driver = webdriver.Chrome()
driver.maximize_window()
driver.get(capitalIQUrl)
time.sleep(5)

