import pandas as pd
import unicodedata
from xml.dom import minidom
import string
import re
from datetime import datetime, timedelta 
import hashlib
import common
import os
# global variable
data_list = []

def nomarlizeText(element):
    # str_title = " ".join(t.nodeValue for t in element[0].childNodes if t.nodeType == t.TEXT_NODE)
    # Convert text to lowercase
    str_lower = element.lower()
    # Punctuation removal
    # symbols [!”#$%&’()*+,-./:;<=>?@[\]^_`{|}~]:
    remove_symbols = str_lower.translate(str.maketrans('','', string.punctuation))
    # White spaces removal 
    remove_spaces = remove_symbols.strip()
    # remove duplicate space
    remove_dup_spaces = re.sub("\s\s+", " ", remove_spaces)
    # normalize string
    str_normalize = unicodedata.normalize('NFKD', remove_dup_spaces).encode('ascii', 'ignore').decode('ascii')
    # digits removal
    # remove_digits = str_normalize.translate(str.maketrans('', '', digits))    
    # white space removal
    result = str_normalize.replace(' ', '')
    return result
# ------------------------------------------------------------------
# the timestamp only valid if it was detected within the date that xml collected
def check_timestamp_valid(filename_str, date_valid):  
    
    datetime_str = filename_str.split('_')[0]
    datetime_str = re.sub('-', '', datetime_str)    
    if(date_valid==datetime_str):
        return True
    else:
        return False
# ------------------------------------------------------------------
def convert_xlm_file_to_date(filename_str):
    datetime_str = filename_str.split('_')[0]
    datetime_str = re.sub('-', '', datetime_str)    
    date_time_obj = datetime.strptime(datetime_str, '%Y%m%d')
    date_after = date_time_obj + timedelta(days=1)

    si = datetime(date_time_obj.year, date_time_obj.month, date_time_obj.day, hour=6, minute=10, second=0)
    ei = datetime(date_after.year, date_after.month, date_after.day, hour=1, minute=50, second=0)

    return si, ei
# ------------------------------------------------------------------
def checking():
    df_latency = pd.read_csv("matching_final.csv")
    df_collection = pd.read_csv("collection.csv")

    data_lst = []

    for row in df_latency.itertuples():
        h = str(row.Hashcode)
        candidate = str(row.Candidate)
        start_h = candidate.split('_')[1].split('.')[0].strip()  + "00"
        latency = int(row.Latency) 
        for r in df_collection.itertuples():
            # Channel_name,Title,Hashcode,Start,Stop
            channel_code = str(r.Channel_Code)        
            hashcode = str(r.Hashcode)
            start_time = str(r.Start)
            stop_time = str(r.Stop)
            if hashcode == h and start_time == start_h:
                case = ({
                    "Channel_Code": channel_code,                  
                    "Hashcode" : hashcode, 
                    "Start": start_time, 
                    "Stop": stop_time, 
                    "Latency": latency
                })
                data_lst.append(case)                
    
    df = pd.DataFrame(data_lst)
    df.to_csv("collection_pre.csv", index = False, header=True, encoding="utf-8-sig")
               
# ------------------------------------------------------------------
def read_xml(base_path, input_file, channel_c):
    file_path = base_path + "\\" + input_file
    xmldoc = minidom.parse(file_path)

    itemlist = xmldoc.getElementsByTagName('programme')
    # print("Total item:", len(itemlist))
    
    # print(itemlist[0].attributes['start'].value)
       
    for s in itemlist:
        start_time = s.attributes['start'].value.strip().split('+')[0].strip()
        stop_time = s.attributes['stop'].value.strip().split('+')[0].strip()
        channel_code = s.attributes['channel'].value.strip().split('.')[0].strip().lower()
        channel_name = common.get_channel_name_by_code(channel_code)
        title = s.getElementsByTagName('title')[0].firstChild.nodeValue
        nomarlized_title = nomarlizeText(title).strip()
        category_p = s.getElementsByTagName('category')[0].firstChild.nodeValue
        length_p = s.getElementsByTagName('length')[0].firstChild.nodeValue

        value_hash = str(channel_code)+str(nomarlized_title)
        hash_id = hashlib.sha1(value_hash.encode()).hexdigest()
        
        # latency = get_latency(hash_id, start_time)
        # if latency != 37000:
        year_start = int(start_time[:4])
        month_start = int(start_time[4:6])
        day_start = int(start_time[6:8])
        hour_start = int(start_time[8:10])
        min_start = int(start_time[10:12])
        second_start = 0


        # datetime_element = datetime(year, month, day, hour, minute, second, milliseconds)
        s_j = datetime(year=year_start, month=month_start, day=day_start, hour=hour_start, minute=min_start, second=second_start)

        year_stop = int(stop_time[:4])
        month_stop = int(stop_time[4:6])
        day_stop = int(stop_time[6:8])
        hour_stop= int(stop_time[8:10])
        min_stop = int(stop_time[10:12])
        second_stop = 0
        e_j = datetime(year=year_stop, month=month_stop, day=day_stop, hour=hour_stop, minute=min_stop, second=second_stop)
        
        s_i, e_i = convert_xlm_file_to_date(input_file)
        
        duration_program = int(length_p)
        str_start = start_time + "00"
        str_stop = stop_time + "00"
        if (s_j < e_j and s_j > s_i and e_j < e_i and channel_code==channel_c and duration_program >=5):
            value_hash = str(channel_code)+str(nomarlized_title)
            hash_id = hashlib.sha1(value_hash.encode()).hexdigest()
            data_row = {
            "Channel_Code": channel_code,
            "Hashcode" : hash_id,
            "Start": str_start,
            "Stop": str_stop
            }
            # print(data_row)
            data_list.append(data_row)

    return
# ------------------------------------------------------------------
def main():

    base_path = r"data\\01"
    # "c192", "c4", "c80", "c47", "c118", "c111", "c445", "c119"
    channel_list = ["c192", "c4", "c80", "c47", "c118", "c111", "c445", "c119"]

    for channel_name in channel_list:
        print("Processing: ", channel_name)
        for _, _, f in os.walk(base_path):
            for file_name in f:
                if(file_name.endswith(".xml")):
                    read_xml(base_path, file_name, channel_name)        

    df = pd.DataFrame(data_list)
    df.to_csv("collection.csv", index = False, header=True, encoding="utf-8-sig")

    # checking()
if __name__ == '__main__':
    main()
    



