import os               # OS routines for NT or Posix depending on what system we're on
import sys              # Used for system calls
import bs4              # Beautiful Soup Elixir and Tonic - "The Screen-Scraper's Friend"
import time             # Time manipulation
import plyer            # Notification handler
import datetime         # Concrete date/time and related types
import requests         # HTML requests
import simple_colors    # More on -> https://github.com/fatih/color/blob/master/color.go

def createDesktopNotification(title, message, appname, timeout):

    plyer.notification.notify(
        title=title,            # Title of notification
        message=message,        # Message text of notification
        app_name=appname,       # App name that produced the notification
        timeout=timeout         # The notification will automatically disappear after specified number of seconds
    )

def formatTime(timeLikeObject):
    
    hour = timeLikeObject.hour
    minute = timeLikeObject.minute
    second =timeLikeObject.second
    returnString = "-| "
    
    if hour < 10:
        returnString += "0"
    returnString += str(hour) + ":"
        
    if minute < 10:
        returnString += "0"
    returnString += str(minute) + ":"
    
    if second < 10:
        returnString += "0"
    returnString += str(second)
    
    returnString += " |-"
    return returnString

def formatLinkName(name):
    norm = 60   # Maximum length for link name
    newName = name + " " * (norm - len(name))
    return newName

def printLinksFromText(htmlText):
    for element in htmlText.find_all('a'):
        if element.has_attr('href'):
            href_value = element.get('href')
            href_value = href_value.replace(" ", "%20")
            if href_value.startswith("pub"):
                href_value = "https://imi.pmf.kg.ac.rs/" + href_value
            print(formatLinkName(element.text) + " -> Link: " + href_value)

def getNewsText(soup, newsTitle):
    newsTitle = newsTitle.replace(" ", "")
    list1 = soup.findAll('p')
    
    for i in range(len(list1)):
        string = list1[i].get_text()
        string = string.replace(" ", "")
        if(string == newsTitle):
            print("----------------------------------------------------------------")
            print(simple_colors.red("Text:"))
            print("----------------------------------------------------------------")
            print(list1[i+3].text)
            print("----------------------------------------------------------------")
            if list1[i+3].find_all('a') != []:
                print(simple_colors.red("Links:"))
                print("----------------------------------------------------------------")
                printLinksFromText(list1[i+3])
                print("----------------------------------------------------------------")
            break

def ParseWebPage(url):
    response = requests.get(url)
    
    if not response.status_code == 200:
        print(simple_colors.red("Could not retrieve page source. Response status code: " + str(response.status_code)))
        sys.exit(1)
    
    page_source = response.text
    soup = bs4.BeautifulSoup(page_source, 'html.parser')
    
    news = soup.findAll('tr')
    tmp_list = list()
    for i in range(1, len(news)):
        pom = news[i].findAll('td', {'class' : 'naslov_oglasa'})
        first = pom
        tmp_list.append(first)
    
    return [tmp_list, soup]

def checkNewsFunction(url, timeToSleep, timeoutTime):
    
    ret = ParseWebPage(url)
    first = ret[0][0]
    soup = ret[1]
    
    while(True):
        test = ParseWebPage(url)
        newFirst = test[0][0]
        soup = test[1]
        
        os.system('cls')
        print("------------------------------------------------------------------------------------------------------")
        print("The latest available is: " + simple_colors.red(newFirst[0].get_text()))
        getNewsText(soup, newFirst[0].get_text())
        
        if(first != newFirst):
            first = newFirst
            createDesktopNotification("IMI NEWS arrived!", first[0].text, "Python IMI Scrapper", timeoutTime)
        else:
            formatTime(datetime.datetime.now().time())
            print("\tThere is not any news... | New check in " + simple_colors.red(str(timeToSleep/60) + " minutes") + " | Time of the last check: " + formatTime(datetime.datetime.now().time()))
            print("------------------------------------------------------------------------------------------------------")
        print("Finish the execution with [ " + simple_colors.red(" CTRL + C") + " ]")
        time.sleep(timeToSleep)

def main():
    
    url                 = "https://imi.pmf.kg.ac.rs/oglasna-tabla"      # IMI URL
    searchTimeout       = 5 * 60                                        # Duration of sleep (in seconds) between checking for news. Change this responsibly!
    timeoutTime         = 10                                            # Time in seconds representing for how long will the notification will be visible
    
    checkNewsFunction(url, searchTimeout, timeoutTime)
    
if __name__ == "__main__":
    main()
