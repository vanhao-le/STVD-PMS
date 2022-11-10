import os
# ------------------------------------------------------------------
def get_channel_name_by_code(channel_code):
    return {
        "c192": "TF1",
        "c4": "France 2",
        "c80": "France 3",
        "c34": "Canal+",
        "c47": "France 5",
        "c118": "M6",        
        "c111": "Arte",
        "c445": "C8",
        "c119": "W9",
        "c195": "TMC",
        "c446": "TFX",
        "c444": "NRJ 12",
        "c78": "France 4",
        "c234": "La Chaîne parlementaire",
        "c481": "BFMTV",
        "c226": "CNEWS",
        "c458": "CSTAR",
        "c482": "Gulli",
        "c1404": "TF1 Séries Films",
        "c1401": "L'Equipe",
        "c1403": "6ter",
        "c1402": "RMC Story",
        "c1400": "RMC Découverte",
        "c1399": "Chérie 25",
        "c112": "LCI",
        "c2111": "Franceinfo"
    }.get(channel_code, "c00")
# ------------------------------------------------------------------
def check_file(file_name, path_name):    
    for _, _, files in os.walk(path_name):
        for name in files:            
            if(name.strip() == file_name):
                return True
    return False
# ------------------------------------------------------------------
def map_channel(channel_code):
    return {
        "c192": 1,
        "c4": 2,
        "c80": 3,        
        "c47": 4,
        "c118": 5,        
        "c111": 6,
        "c445": 7,
        "c119": 8,
        "c34": 9,
        "c195": 10,
        "c446": 11,
        "c444": 12,
        "c78": 13,
        "c234": 14,
        "c481": 15,
        "c226": 16,
        "c458": 17,
        "c482": 18,
        "c1404": 19,
        "c1401": 20,
        "c1403": 21,
        "c1402": 22,
        "c1400": 23,
        "c1399": 24,
        "c112": 25,
        "c2111": 26
    }.get(channel_code, 0)
# ------------------------------------------------------------------