from urllib.request import urlopen,Request # 인터넷 url를 열어주는 패키지
from urllib.parse import quote_plus # 한글을 유니코드 형식으로 변환해줌
from bs4 import BeautifulSoup # BeautifulSoup: 웹 크롤링이나 스크래핑할떄 쓰이는 python 라이브러리
from selenium import webdriver # webdriver 가져오기
import time # 크롤링 중 시간 대기를 위한 패키지
import warnings # 경고메시지 제거 패키지
from tqdm import tqdm
from selenium.webdriver.common.keys import Keys 
import pandas as pd
import json
from collections import OrderedDict
from datetime import datetime
 
warnings.filterwarnings(action='ignore') # 경고 메세지 제거

# [1] 인스타 그램 url 생성
baseUrl = "https://www.instagram.com/explore/tags/"
plusUrl = input('검색할 태그를 입력하세요 : ')
url = baseUrl + quote_plus(plusUrl)

# [2] chromedriver을 통해 웹을 띄운다.
driver = webdriver.Chrome(
    executable_path= "C:/Users/multicampus/chromedriver_win32/chromedriver.exe"
)
# 해당 url을 driver로 할당
driver.get(url)
time.sleep(2)

# [3] 로그인 하기
# 로그인 버튼 클릭
login_section = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button'
driver.find_element_by_xpath(login_section).click()
time.sleep(2)
# 계정, 비밀번호 압력
elem_login = driver.find_element_by_name("username")
elem_login.clear()
elem_login.send_keys('silver_jae@naver.com')
time.sleep(1)
elem_login = driver.find_element_by_name('password')
elem_login.clear()
elem_login.send_keys('ssafy%qks')
time.sleep(1)

# 로그인 버튼 클릭
xpath = """//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button"""
driver.find_element_by_xpath(xpath).click()
time.sleep(2)
# 건너뛰기 클릭
passbutton="""//*[@id="react-root"]/section/main/div/div/div/div/button"""
driver.find_element_by_xpath(passbutton).click()
time.sleep(2)

# [4] 해쉬태그에 input값을 넣어 해당 데이터들을 modal_page에 append시킴
# 1. bsObj 에 담아놓은 모든 데이터들의 좋아요 갯수를 체크해나간다.
# 2. 좋아요을 기준으로 이미지를 sort 시킨다. 
# 3. 어떤 이미지를 선택한다면 해당 이미지의 계정명, 이미지, 태그를 출력가능해야함
# 추후 계획 : 우리플랫폼 db유저들만 체크, 게시글내용을 자연어 처리하여 긍정 or 부정을 판단

SCROLL_PAUSE_TIME = 1.0
modal_page = []
cnt = 0 
while cnt < 1:
    cnt += 1
    pageString = driver.page_source
    bsObj = BeautifulSoup(pageString, 'lxml')
    
    try:
    # bsObj는 웹에서 모든 데이터를 크롤링한 결과데이터
        for line in bsObj.find_all(name='div', attrs={"class":"Nnq7C weEfm"}): # "class":"Nnq7C weEfm"는 이미지를 가리키는 클래스
            # 인스타는 1row 마다 3 column이 있음 => 1개의 line마다 3개의 개시글 데이터가존재
            for i in range(3):
                title = line.select('a')[i]
                real = title.attrs['href']
                modal_page.append(real)
    except IndexError as ider:
        print("인덱스에러발생")

    last_height = driver.execute_script('return document.body.scrollHeight')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        else:
            last_height = new_height
            continue

print("통과2")
print(modal_page)
num_of_data = len(modal_page)
print('총 {0}개의 데이터를 수집합니다.'.format(num_of_data))
file_data = OrderedDict()
for i in tqdm(range(num_of_data)):
    num = str(i+1)
    file_data[num] = {
        "rname" : "",
        "rbranch" : "",
        "instaid" : "",
        "iurl" : "",
        "likes" : "",
        "idate" : "",
    }
    # print("num ==>", num)
    file_data[num]["rname"] = plusUrl
    req = Request("https://www.instagram.com"+modal_page[i], headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    # 해당 페이지의 html을 모두 soup에 할당
    soup = BeautifulSoup(webpage, 'lxml', from_encoding='utf-8  ')

    # property : meta클래스에서 property가 og:description인걸 뽑아냄
    # info에 좋아요, 댓글, 이름 등이 있음
    info = soup.find('meta', attrs={'property':"og:description"})
    total = info['content']
    
    # 가게 지점명은 일단 공석

    print()
    # 계정명 저장
    account = total[total.find("@") + 1:total.find(")")]
    account = account[:20]
    if account == '':
        account = "Null"
    account = account.replace('posted on','')
    account = account.replace('shared a post on','')
    account = account.replace('on Instagram','')
    file_data[num]["instaid"] = account

    # 이미지 저장
    img = soup.find('meta', attrs={'property':"og:image"})
    img_url = img['content'].replace('amp;','')
    file_data[num]["iurl"] = img_url

    # 좋아요
    likes = 0
    if total.find("Likes") != -1:
        likes = total[0:total.find("Likes")-1 ]
        likes = likes.replace(',','')
    file_data[num]["likes"] = int(likes)

    # 현재시간
    my_date = datetime.now()
    file_data[num]["idate"] = my_date.isoformat()

    # # 댓글수
    # comments = 0
    # if total.find("Comments") != -1:
    #     comments = total[total.find(",")+2: total.find("Comments")]
    # file_data[users]["comments"] = int(comments)

# json 파일로 저장
with open(plusUrl + '.json', 'w', encoding="utf-8") as make_file:
    json.dump(file_data, make_file, ensure_ascii=False, indent="\t")
driver.close()

