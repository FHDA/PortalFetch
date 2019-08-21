# This code can fetch data from the website, but it needs to login and get cookies handly. 
# Because the cookies changes when login at different time, so new cookies and data should be use, 
# if you want to make this code work.   
# More work need to be done to make the fetch work automotically.
from bs4 import BeautifulSoup
import requests
import csv

#fetch data from the website
#how to get the cookies and data?1-login the website, 2-click right mouse-inspect-network-click refresh- click the first of the left 
#column-choose headers-then all the information are here
def fetchdata():
    url = "https://ssb-prod.ec.fhda.edu/PROD/bwskfcls.P_GetCrse_Advanced"
    cookies = dict(SESSID='TlJCV1JJMTkzMjQwMw==', AWSELB='8FC3B10C7C6F2E81FB85778EC82E80B35F6053EB3FB0A326C415E62DF224C6255601225080A4895B1FADB06E83D852FA6F81C67EE98881214B71E413F60117E73BEF0DB1',shib_idp_session='929644161fc2ac3b1694fdb45c1f9b89343665d7655bd8d380d505660fe18c2b',IDMSESSID='608050D4F1FB8791B3DE6BA6CE1CD30D6BB7E87CC6D28205E263CFDD18FB7C89B87904542F7037A0BAC33AF2D4787F522A0A9D73A8D1CF8754DED595C67FF92C8BE78596A938A2D17308051D07FAB282')
    data = "rsts=dummy&crn=dummy&term_in=202022&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj=ACCT&sel_subj=ADMJ&sel_subj=ANTH&sel_subj=ARTS&sel_subj=ASTR&sel_subj=AUTO&sel_subj=BIOL&sel_subj=BUS&sel_subj=CLP&sel_subj=CHEM&sel_subj=C+D&sel_subj=COMM&sel_subj=CIS&sel_subj=COUN&sel_subj=DANC&sel_subj=DMT&sel_subj=ECON&sel_subj=EDUC&sel_subj=EDAC&sel_subj=ENGR&sel_subj=ESL&sel_subj=ELIT&sel_subj=EWRT&sel_subj=ESCI&sel_subj=E+S&sel_subj=F%2FTV&sel_subj=FREN&sel_subj=GEO&sel_subj=GEOL&sel_subj=GERM&sel_subj=HTEC&sel_subj=HLTH&sel_subj=HNDI&sel_subj=HIST&sel_subj=HUMA&sel_subj=HUMI&sel_subj=ICS&sel_subj=INTL&sel_subj=ITAL&sel_subj=JAPN&sel_subj=JOUR&sel_subj=KNES&sel_subj=KORE&sel_subj=LART&sel_subj=LRNA&sel_subj=L+S&sel_subj=LIB&sel_subj=LING&sel_subj=MAND&sel_subj=MASG&sel_subj=MATH&sel_subj=MET&sel_subj=MUSI&sel_subj=NURS&sel_subj=NUTR&sel_subj=PARA&sel_subj=PERS&sel_subj=PHIL&sel_subj=PHTG&sel_subj=P+E&sel_subj=PEA&sel_subj=PHYS&sel_subj=POLI&sel_subj=PSYC&sel_subj=READ&sel_subj=REST&sel_subj=RUSS&sel_subj=SIGN&sel_subj=SKIL&sel_subj=SOSC&sel_subj=SOC&sel_subj=SPAN&sel_subj=THEA&sel_subj=VIET&sel_subj=WMST&sel_crse=&sel_title=&sel_schd=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_ptrm=%25&sel_instr=%25&sel_sess=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a&SUB_BTN=Section+Search&path=1"
    r = requests.post(url=url, data=data, cookies=cookies)
    #print(r.content)
    print(r.text)
    return (r.text)
  
# save the data to a list  
def get_contents(ulist, text):
    soup = BeautifulSoup(text, 'lxml')
    trs = soup.find_all('tr')
    for tr in trs:
        ui = []
        for td in tr:
            ui.append(td.string)
        ulist.append(ui)
 
# save the data in the list to a .csv file
def save_contents(urlist):
    with open("DeAnza.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['DeAnza'])

        for i in range(8,len(urlist)-1):
            if len(ulist[i]) >=35:
                writer.writerow([urlist[i][1], urlist[i][3], urlist[i][5],urlist[i][7], urlist[i][9], urlist[i][11],
                            urlist[i][13], urlist[i][15], urlist[i][17],urlist[i][19], urlist[i][21], urlist[i][23],
                            urlist[i][25], urlist[i][27], urlist[i][29],urlist[i][31], urlist[i][33], urlist[i][35]]
                            )
            else:
                writer.writerow(urlist[i])
                
ulist=[]
text = fetchdata()
get_contents(ulist, text)
save_contents(ulist)
