from bs4 import BeautifulSoup
import urllib.request
import csv

base_url = "http://results.eci.gov.in/ac/en/constituencywise/ConstituencywiseS012.htm"
with urllib.request.urlopen(base_url) as f:
    html_output = f.read().decode('utf-8')

def getResultRowDetails(result_tr,total_votes,state,constituency):
    result_list = result_tr.find_all("td")
    result_dict = {}
    result_dict["candidate_name"] = result_list[1].get_text().strip()
    result_dict["party"] = result_list[2].get_text().strip()
    result_dict["num_votes"] = int(result_list[5].get_text().strip())
    result_dict["total_votes"] = int(total_votes)
    result_dict["state"] = state
    result_dict["constituency"] = constituency
    result_dict["perc_votes"] = round(float(result_list[6].get_text().strip())/100,6)
    return result_dict


def getRankOrder(data_dict):
    return sorted(data_dict,key=lambda i:i['perc_votes'],reverse=True)
    
def setRankOrder(data_dict):
    for x in range(0,len(data_dict)):
        data_dict[x]['rank'] = x+1
        if(x==0):
            data_dict[x]['won'] = 1
        else:
            data_dict[x]['won'] = 0
    return data_dict

   
def parseElectionResults(html_data):
    soup = BeautifulSoup(html_data,"html.parser")
    results_div = soup.find_all(id="div1")[0].table.find_all("tr")
    numResults = len(results_div)
    
    state,constituency =  results_div[0].td.get_text().strip().split("-")
    print("{}-{}".format(state,constituency))
    #print(results_div)

    total_votes = results_div[numResults-1].find_all("td")[-2].get_text().strip()
    #print(total_votes)

    data_dict = []

    for x in range(3,numResults-1):
        data_dict.append(getResultRowDetails(results_div[x],total_votes,state,constituency))

    data_dict = setRankOrder(getRankOrder(data_dict))    
    return data_dict


final_data = []
for stateId in range(1,176):
    base_url = "http://results.eci.gov.in/ac/en/constituencywise/ConstituencywiseS01%s.htm"% (stateId)
    print(base_url)
    with urllib.request.urlopen(base_url) as f:
            html_output = f.read().decode('utf-8')
    final_data.extend(parseElectionResults(html_output))
    
with open('ap_2019_assembly.csv', 'w') as csvfile:
    fieldnames = ['state', 'constituency','candidate_name','party','num_votes','total_votes','perc_votes','rank','won']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for x in final_data:
        writer.writerow(x)





    #print(len(results_div));
    #print(results_div[len(results_div)-1])
    #print(results_div[0].find_all("td")[0].get_text().strip())
    #soup2 = BeautifulSoup(results_div,"html.parser")
    #print(soup2.table.find_all("tr"))
    #[{'won': 1, 'perc_votes': 0.5083, 'total_votes': 150691, 'constituency': 'Palasa', 'candidate_name': 'APPALARAJU SEEDIRI', 'rank': 1, 'num_votes': 76603, 'state': 'Andhra Pradesh', 'party': 'Yuvajana Sramika Rythu Congress Party'}
