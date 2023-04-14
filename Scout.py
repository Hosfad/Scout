import os
import sys
from threading import Thread
from time import sleep
import requests
import socket

r = "\033[31m"
g = "\033[32m"
y = "\033[33m"
b = "\033[34m"
p = "\033[35m"
d = "\033[2;37m"
w = "\033[0m"
lr = "\u001b[38;5;196m"
W = f"{w}\033[1;47m"
R = f"{w}\033[1;41m"
G = f"{w}\033[1;42m"
Y = f"{w}\033[1;43m"
B = f"{w}\033[1;44m"

userrecon_num = 0
userrecon_working = 0
userrecon_results = []

space = "         "

logo = f"""{b}
              Scout
⠀⣰⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⡾
⠀⠀⣿⡍⠛⠲⣶⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⡴⠞⠉⣠⡞⠀⠀
⠀⠀⠘⣽⢷⣦⣌⣈⠋⡚⠿⣦⡀⠀⠀⣴⣶⡄⠀⠀⣠⡶⠚⠛⣙⣭⠠⣤⣶⣯⠆⠀⠀⠀
⠀⠀⠀⣼⣷⣀⠀⠀⠈⠀⠀⠀⢻⡇⠺⡿⠛⣿⡅⠀⢿⠀⠀⣼⠿⣫⣭⣠⣤⡶⠂
⠀⠀⠀⠀⠉⠛⠿⣹⣾⠔⠃⠀⠈⠳⠾⠏⠀⠻⣷⡺⠋⠀⣤⣸⣷⣶⡾⠖⠀
⠀⠀⠀⠀⠀⠈⠒⠷⣿⡻⣞⣀⣄⣀⣀⡄⠀⠀⣠⣄⣸⡿⣾⣿⡽⡄
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠟⠯⣽⢿⡿⠃⠀⢀⣿⡙⠑⠙⠛⠉⠁⠀                
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣯⣦⣾⣿⠃⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣼⣿⣿⣿⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⢩⡿⠘
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣽⡃⠀⠀

 {d}A simple {w}{r}reconnaissance{d} tool{w}
 {d}By {w}{r}Hosfad{w} https://hosfad.dev
"""

choices = f"""
{G}\033[2;30m Choose an operation  (0 to exit){w}
        
{w}{b}  1{w} User lookup      {d} Checks most of the social media sites for the username 
{w}{b}  2{w} Ip lookup        {d} Lookup ip adress information (location,isp,etc)
{w}{b}  3{w} DNS lookup       {d} Lookup for DNS records 
{w}{b}  4{w} RDNS lookup      {d} Reverse DNS lookup 
{w}{b}  0{w} Exit             {d} Cya later 
{w}{b}  {w}  COMMING SOON     {d} (Email lookup,Phone lookup,Social media scrappers and much more) 
        """


def handleInput(userInput: str):
    match (userInput):
        case "1":
            userrecon()
        case "2":
            iplocation()
        case "3":
            infoga("dnslookup")
        case "4":
            infoga("reverseiplookup")
        case "0":
            sys.exit(1)


req = None


def userrecon():
    global userrecon_results, userrecon_working, userrecon_num
    username = input(
        f"{space}{w}{b}>{w} Enter username (Empty to go back): {b} ").lower()
    if len(username) == 0:
        return
    print(f"Searching for username : {username} ,This may take a moment")

    for url in socialMediaLinks:
        req = None
        Thread(target=send_req, args=(url, username)).start()
        sleep(0.2)
    while True:
        if userrecon_num == len(socialMediaLinks):
            break
    print()
    # Search snapchat
    if (search_snap(username)):
        userrecon_num += 1
        url = "https://snapchat.com/add/" + username
        userrecon_results.append(
            f"  {space}{b}[{g}200{b}] {userrecon_num}/72 {w}{url.format(url)}")

    for user in userrecon_results:
        if "200" in user:
            print(user)
    userrecon_results = []
    userrecon_working = 0
    userrecon_num = 0


def display_progress(iteration, total, text=""):
    bar_max_width = 40  # chars
    bar_current_width = bar_max_width * iteration // total
    bar = "█" * bar_current_width + " " * (bar_max_width - bar_current_width)
    progress = "%.1f" % (iteration / total * 100)
    print(f"{space}{iteration}/{total} |{bar}| {progress}% {text}", end="\r")
    if iteration == total:
        print()


def send_req(url, username):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
    global req
    try:
        req = requests.get(url.format(username), headers=headers)
    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.TooManyRedirects:
        pass
    except requests.exceptions.ConnectionError:
        pass
    global userrecon_num, userrecon_results, userrecon_working

    userrecon_num += 1
    if (req == None):
        pass

    if req.status_code == 200:
        color = g
        userrecon_working += 1
    elif req.status_code == 404:
        color = r
    else:
        color = y
    display_progress(userrecon_num, 72, f"Users found: {userrecon_working}")
    url = url.format(username)
    userrecon_results.append(
        f"  {space}{b}[{color}{req.status_code}{b}] {userrecon_num}/71 {w}{url.format(username)}")


socialMediaLinks = ["https://facebook.com/{}","https://instagram.com/{}","https://twitter.com/{}","https://youtube.com/{}","https://vimeo.com/{}","https://github.com/{}","https://plus.google.com/{}","https://pinterest.com/{}","https://flickr.com/people/{}","https://vk.com/{}","https://about.me/{}","https://disqus.com/{}","https://bitbucket.org/{}","https://flipboard.com/@{}","https://medium.com/@{}","https://hackerone.com/{}","https://keybase.io/{}","https://buzzfeed.com/{}","https://slideshare.net/{}","https://mixcloud.com/{}","https://soundcloud.com/{}","https://badoo.com/en/{}","https://imgur.com/user/{}","https://open.spotify.com/user/{}","https://pastebin.com/u/{}","https://wattpad.com/user/{}","https://canva.com/{}","https://codecademy.com/{}","https://last.fm/user/{}","https://blip.fm/{}","https://dribbble.com/{}","https://en.gravatar.com/{}","https://foursquare.com/{}","https://creativemarket.com/{}","https://ello.co/{}","https://cash.me/{}","https://angel.co/{}","https://500px.com/{}","https://houzz.com/user/{}","https://tripadvisor.com/members/{}","https://kongregate.com/accounts/{}","https://{}.blogspot.com/","https://{}.tumblr.com/","https://{}.wordpress.com/","https://{}.devianart.com/","https://{}.slack.com/","https://{}.livejournal.com/","https://{}.newgrounds.com/","https://{}.hubpages.com","https://{}.contently.com","https://steamcommunity.com/id/{}","https://www.wikipedia.org/wiki/User:{}","https://www.freelancer.com/u/{}","https://www.dailymotion.com/{}","https://www.etsy.com/shop/{}","https://www.scribd.com/{}","https://www.patreon.com/{}","https://www.behance.net/{}","https://www.goodreads.com/{}","https://www.gumroad.com/{}","https://www.instructables.com/member/{}","https://www.codementor.io/{}","https://www.reverbnation.com/{}","https://www.designspiration.net/{}","https://www.bandcamp.com/{}","https://www.colourlovers.com/love/{}","https://www.ifttt.com/p/{}","https://www.trakt.tv/users/{}","https://www.okcupid.com/profile/{}","https://www.trip.skyscanner.com/user/{}","http://www.zone-h.org/archive/notifier={}"]


def iplocation():
   # print(f"{space}{b}>{w} local IP: {os.popen('curl ifconfig.co --silent').readline().strip()}")
    x = input(f"{space}{b}>{w} Enter IP adress:{b} ")
    if len(x) == 0:
        return
    if x.split(".")[0].isnumeric():
        pass
    req = requests.get("https://ipinfo.io/" + x + "/json").json()
    try:
        ip = "Ip adress: " + req["ip"]
    except KeyError:
        ip = ""
    try:
        city = "City: " + req["city"]
    except KeyError:
        city = ""
    try:
        country = "Country: " + req["country"]
    except KeyError:
        country = ""
    try:
        loc = "Location: " + req["loc"]
    except KeyError:
        loc = ""
    try:
        org = "Internet provider: " + req["org"]
    except KeyError:
        org = ""
    try:
        tz = "Timezone: " + req["timezone"]
    except KeyError:
        tz = ""
    z = [ip, city, country, loc, org, tz]
    for res in z:
        print(f"{space}{b}-{w} {res}")


def infoga(opt):
    apihack = "https://api.hackertarget.com/{}/?q={}"
    x = input(f"{space}{b}>{w} enter domain or IP:{b} ")
    if len(x) == 0:
        return
    if x.split(".")[0].isnumeric():
        x = socket.gethostbyname(x)
    else:
        pass
    req = requests.get(apihack.format(opt, x), stream=True)
    for res in req.iter_lines():
        print(f"{space}{b}-{w} {res.decode('utf-8')}")





def search_snap(username):
    url = "https://accounts.snapchat.com:443/accounts/get_username_suggestions"
    headers = {"Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\"", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36", "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
           "Accept": "*/*", "Origin": "https://accounts.snapchat.com", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "same-origin", "Sec-Fetch-Dest": "empty", "Referer": "https://accounts.snapchat.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
    xsrf_token = "JxVkpuY3VbHfOFagfT0csQ"
    cookies = {"xsrf_token": xsrf_token}
    data = {"requested_username": username,
            "xsrf_token": xsrf_token}
    res = requests.post(url, headers=headers,
                        cookies=cookies, data=data)
    return True if "OK" in res.text else False


if __name__ == '__main__':
    print(logo)
    lastLen = 1
    while True:
        print(choices)
        inp = input(f"Choice : ")
        inp = ''.join(i for i in inp if i.isdigit())
        handleInput(inp)
