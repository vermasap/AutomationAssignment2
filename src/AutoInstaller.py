from selenium import webdriver
import time
from pathlib import Path
import os

driver = None

def downloadInstaller():
    setDriver("chrome", exefile=None)
    global driver
    driver = webdriver.Edge()
    driver.get("https://www.bluestacks.com/")
    driver.maximize_window()
    try:
        elem = driver.find_element_by_xpath("//a[contains(.,'Download BlueStacks 5')]")
        defaultPath = str(os.path.join(Path.home(), "Downloads"))
        prevlatest = getlatestfile(defaultPath)
        elem.click()
        latestFile = waitfordownloadcompletion(prevlatest, defaultPath)
        driver.quit()
        return latestFile
    except Exception as e:
        print("Exception found")
        print(e)
        exit(1)

def waitfordownloadcompletion(prevNewestFile, defaultPath):
    newNewestFile = prevNewestFile
    while(newNewestFile==prevNewestFile or "Unconfirmed" in newNewestFile or ".tmp" in newNewestFile):
        time.sleep(1)
        newNewestFile = getlatestfile(defaultPath)
    print("Download complete")
    return newNewestFile

def getlatestfile(defPath):
    files = os.listdir(defPath)
    files = [os.path.join(defPath, file) for file in files]
    newest = max(files, key=os.path.getctime)
    return newest


def startInstallation(file):
    setDriver("Winium.Desktop.Driver.exe", file)
    global driver
    try:
        time.sleep(10)
        driver.find_element_by_name("Accept").click()
        driver.find_element_by_name("Accept").click()
        driver.find_element_by_name("Customize installation").click()
        driver.find_element_by_name("Folder").click()
        select_folder(driver, "This PC->Local Disk (D:)->New folder")
        driver.find_element_by_name("Back").click()
        driver.find_element_by_name("Install now").click()
        time.sleep(2)
        elems = driver.find_elements_by_class_name("ProgressBar")
        while len(elems) > 0:
            time.sleep(5)
            elems = driver.find_elements_by_class_name("ProgressBar")
            print("Installing")
        print("Installed")
    except Exception as e:
        print("Caught exception.Please start again")
        print(e)
    finally:
        driver.quit()

def setDriver(driverfile, exefile):
    global driver
    if driverfile=='chrome':
        driver = webdriver.chrome
    else:
        os.startfile(driverfile)
        driver = webdriver.Remote(command_executor='http://localhost:9999', desired_capabilities={"debugConnectToRunningApp": 'false',"app": r"{}".format(exefile)})


def select_folder(driver, folderPath):
    for name in folderPath.split("->"):
        driver.find_element_by_name(name).click()
    driver.find_element_by_name("OK").click()


downloadedfile = downloadInstaller()
print("Download Finished. Starting Installation.")
startInstallation(os.path.abspath(downloadedfile))
