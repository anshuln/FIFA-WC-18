from urllib import request
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import threading
import time
def get_links():
	container = "https://www.sportsmole.co.uk"
	match_links=[]
	source="https://www.sportsmole.co.uk/football/live-commentary/"
	page=request.urlopen(source)
	body = page.read()
	soup = bs(body, 'html.parser')
	page.close()
	matches = soup.find_all("div",class_="hot_topics")[0]
	m = matches.find_all("a")
	for p in m:
		if(p.text.find("LIVE!") == 0 ):
			match_links.append(container+p["href"])
	return match_links

def give_notif(event,teams):
    from win10toast import ToastNotifier
    toaster = ToastNotifier()
    toaster.show_toast(event,teams,duration=10)
    driver=webdriver.Chrome()
    driver.get('https://www.sonyliv.com/')
    time.sleep(120)
    return
    
    
    
def get_highlights(match):
    s=[]
    running=True
    notifs=[]   
    teams=match.split("live-commentary-")[1].split('_')[0].replace('-',' ')
    print("Getting updates for ",teams)

    while running == True:
        f=0
        curr=[]
        s_prev=s
        s=[]
        page=request.urlopen(match)
        body = page.read()
        soup = bs(body, 'html.parser')
        page.close()
        interests=soup.find_all("span",class_="post")
        for i in interests:
            if(len(i.find_all("strong")))>0:
                    for j in i.find_all("strong"):
                            if(j.text.find('BOOKING')>-1 or j.text.find('CLOSE')>-1 or j.text.find('GOAL')>-1 or j.text.find('CHANCE')>-1 or j.text.find('SAVE')>-1 or j.text.find('CORNER')>-1 or j.text.find('SHOT')>-1 or j.text.find('FREE KICK')>-1 or j.text.find('PENALTY')>-1 or j.text.find('FULL-TIME')>-1):
                                    
                                    times=j.parent.parent.find_all("a",class_="period")[0].text
                                    s.append(j.text+" "+times)
        if(len(s_prev)):
                
                if(s[0].find("FULL-TIME")>-1):
                    running=False
                    print("GAME OVER!")
                if(s[0]==s_prev[0]):
                    pass
                else:
                    notifs.append([s[0].split(' ')[0],teams,time.time(),0])
                    
                for notif in notifs:
                    if (time.time()-notif[2])>210:
                        notif[3]=1
                        f=1
                        curr=notif
                        break
                notifs=[notif for notif in notifs if notif[3]==0]
                if(f==1):
                    give_notif(curr[0],curr[1])
                else:

                    time.sleep(60)
        else:
                time.sleep(60)

    return                
    


    
    


if __name__=="__main__":
        f=0
        while f==0:
                print("INside main loop")

                matches=get_links()
                threads = []
                if len(matches):
                    for match in matches:
                        t=threading.Thread(target=get_highlights,args=(match,))
                        t.daemon=True
                        threads.append(t)
                        f=1
                for t in threads:
                        t.start()
                for t in threads:
                        t.join()
                

    
    
    
