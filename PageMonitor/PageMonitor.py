from selenium import webdriver
import pickle
import winsound
import time
import datetime

def fnParseAddress(strinput):
    if strinput[:7] != "http://":
        if strinput.find("://") != -1:
            print("Error: Cannot retrieve URL, protocol must be HTTP")
            sys.exit(1)
        else:
            strinput = "http://" + strinput
    return strinput


def fnCheckItem(m_webpage, bfirstuse, strsearchID, strsearchword, strbeepforit, iinterval):
    m_t1 = datetime.datetime.now()
    print(m_t1)
    if bfirstuse:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            m_webpage.add_cookie(cookie)
    m_webpage.refresh()
    time.sleep(5)
    m_webpage.execute_script("window.scrollTo(0, 2000)")
    elem = m_webpage.find_element_by_id(strsearchID)
    result = elem.text.splitlines()
    bflag = False
    iwords = len(strsearchword)
    for line in result:
        if bflag:
            print(line)
            bflag = False
        else:
            for i in range(0,iwords - 1,2):
                if line.find(strsearchword[i])>= 0:
                    if(strsearchword[i+1] == 0):
                        print(line)
                    else:
                        bflag = True
                for key in strbeepforit:
                    if line.lower().find(key.lower())>=0:
                        winsound.Beep(2000,1000)
    m_t2 = datetime.datetime.now()
    m_td = m_t2 - m_t1
    print("-----------------------------\n")
    time.sleep(iinterval - (m_td.seconds))

def main():
    strlenovo = fnParseAddress("http://outlet.lenovo.com/outlet_us/laptops/#/?page-index=1&page-size=100&facet-13=1")
    m_lenovo = webdriver.Chrome()
    m_lenovo.get(strlenovo)
    #pickle.dump( m_lenovo.get_cookies() , open("cookies.pkl","wb"))
    #time.sleep(600)
    strchecklist = ["Model details", 1, "Outlet sale price:", 1, "Graphics:", 0]
    SpecialList = ["750M", "755M", "745M", "740M"]
    iter = 0
    while True:
        iter = iter + 1
        if iter == 1:
            fnCheckItem(m_lenovo, True, "search-results-area", strchecklist, SpecialList, 30)
        else:
            fnCheckItem(m_lenovo, False, "search-results-area", strchecklist, SpecialList, 30)
    m_lenovo.close()


if __name__ == "__main__":
    main()
