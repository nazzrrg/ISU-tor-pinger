import requests
from playsound import playsound
import time
import random
from fake_useragent import UserAgent
from stem.control import Controller
from stem import Signal


def get_tor_session():
    session = requests.Session()
    session.proxies = {"http": "socks5://localhost:9050", "https": "socks5://localhost:9050"}
    return session


def renew_connection():
    with Controller.from_port(port=9051) as c:
        c.authenticate(password="password")
        # send NEWNYM signal to establish a new clean connection through the Tor network
        c.signal(Signal.NEWNYM)
        c.close()


if __name__ == "__main__":
    # url = "https://isu.ifmo.ru/"
    url = "®"
    url_tg = 'https://api.telegram.org/bot' + '1332257997:AAG2loW8TZJ37mjfyuqK57XFbnwaNGcaJAY' + '/sendMessage'
    flag = False
    ua = UserAgent()
    s = get_tor_session()
    s.headers = {'User-Agent': str(ua.chrome)}
    count = 0
    count2 = 0
    good_count = 0

    while True:
        renew_connection()
        status = -1
        try:
            ip = s.get("http://icanhazip.com", timeout=15).text
            print("\nIP:", ip, end='')
            response = s.get(url, timeout=15)
            status = response.status_code
        except:
            renew_connection()
            count+=1
            print("FAIL")

        if count > 10 or count2 > 2:
            flag = True

        hold = random.randint(10, 20)

        if 0 < status < 400:
            print("GOOD")
            count = 0
            count2 = 0
            # if (flag):
            #     good_count += 1
            # if flag and good_count > 2:
            if flag:
                print("оруоруору")
                flag = False
                for i in (1, 20):
                    requests.get(url_tg + '?chat_id=211463351&text= ИСУ (возможно) ОЖИЛ СЕГОДНЯ')
                    playsound("02582.mp3")
                # time.sleep(300)

                # requests.get(url_tg + '?chat_id=-1001399796511&text= ИСУ (возможно) ОЖИЛ СЕГОДНЯ')
        else:
            print("BAD, response: ", status)
            if status >= 400:
                if not flag:
                    good_count = 0
                count2 += 1

        print("Waiting for ", hold, "s")
        for i in range(1, hold + 1):
            print("\r", i, end='')
            time.sleep(1)
        print("\r", end='')
