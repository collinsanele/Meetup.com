from selenium import webdriver
import time
from datetime import datetime
import pandas as pd


driver = webdriver.Chrome("chromedriver.exe")


print("Note this script uses browser automation\nPlease do not close chrome browser window\n")
while True:
    print("Welcome to meetup.com event scraper\nEnter q at any time to quit\n")
    start = input("Enter any key to continue or q to quit\n")
    if str(start) == 'q':
        break
    else:
        url = input("Enter meetup event url\nFor example https://www.meetup.com/BelfastJUG/events/263550129/\n")
        if str(url) == "q":
            break
        if "https" not in url:
            url = "https://"+url
            
        driver.get(url)
        print("Please wait this might take about 15min\n Thanks\n")
        time.sleep(6)
        
        try:
            driver.find_element_by_link_text("See all").click()
            
        except Exception as e:
            print(e)
            continue
            
        time.sleep(6)
            
        try:
            target = driver.find_element_by_class_name("list--infinite-scroll")
            attendees_links = target.find_elements_by_tag_name("a")
            attendees_links = [item.get_attribute("href") for item in attendees_links]
            links = list(set(attendees_links))
            
        except Exception as e:
            print(e)
            continue
        
        
        results = []
        
        c = 0
        for link in links[0:]:
            obj = {"Name":"", "Email":"", "Address":"", "Topic":"", "Profile Link":link}
            try:
                driver.get(link)
            except Exception as e:
                print(e)
                continue

            try:
                name = driver.find_element_by_class_name("text--big").text
                obj["Name"] = name
            except Exception as e:
                print(e)
                pass

            try:
                event_url = links[0]
                obj["Event Url"] = event_url
            except Exception as e:
                print(e)
                pass

            try:
                email = driver.find_elements_by_class_name("card")[1].text.split("\n")[-1]
                obj["Email"] = email
            except Exception as e:
                print(e)
                pass

            try:
                address = driver.find_element_by_class_name("memberLocation").text.split("\n")[-1]
                obj["Address"] = address
            except Exception as e:
                print(e)
                pass

            try:
                topic = driver.find_elements_by_class_name("card")[2].text.split("\n")[-1]
                obj["Topic"] = topic
            except Exception as e:
                print(e)
                pass

            if "@" in obj["Topic"] and "." in obj["Topic"]:
                a = ''
                b = ''

                a = obj["Email"]
                b = obj["Topic"]

                obj["Email"] = b
                obj["Topic"] = a

            if "@" not in obj["Email"]:
                obj["Email"] = "NA"

            results.append(obj)
            c+=1
            print(f"{c} of {len(links[1:])}")
            time.sleep(0.07)
    
    df = pd.DataFrame(results)
    df = df[["Name", "Email", "Address", "Topic", "Profile Link", "Event Url"]]
    df.to_excel(f"""{url.split("/")[3]}{url.split("/")[-2]}.xlsx""")
    print("Done!\nPlease check the directory this script is running from to see downloaded excel file\nThanks")
    
print("Thanks and bye\n This script is in its development phase, if you found any bug please contact the developer on collinsanele@gmail.com\n")
        
            
            
            