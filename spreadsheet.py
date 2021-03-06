import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import OrderedDict
import pprint

def matchBack(little_background, big_background):
    points = 0
    for little_back in little_background:
        for big_back in big_background:
            if (little_back == big_back):
                points += 3
    return points

def matchLiving(little_living, big_living):
    points = 0
    for little_liv in little_living:
        for big_liv in big_living:
            if (little_liv == big_liv):
                points += 2
    return points

def matchRace(little_race, big_race):
    points = 0
    for lit_race in little_race:
        for b_race in big_race:
            if (lit_race == b_race):
                points += 2
    return points

def matchInterests(little_interests, big_interests):
    points = 0
    for little_int in little_interests:
        for big_int in big_interests:
            if (little_int == big_int):
                points += 1
    return points
    


scope = ['https://spreadsheets.google.com/feeds' + ' ' +'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

little_sheet = client.open('Test CSE Little Sign Up (Autumn 2020) (Responses)').sheet1
big_sheet = client.open('Test CSE Big Sign Up (Autumn 2020) (Responses)').sheet1
matches = client.open('Testing Matches')

littles = little_sheet.get_all_values()
bigs = big_sheet.get_all_values()

bigs_left = {""}


# add all bigs to bigs-left set
for big in bigs[1:len(bigs)]:
    bigs_left.add(big[7])

bigs_left.discard("")

d = {}

mapping = OrderedDict(sorted(d.items(), key=lambda t: t[0]))

class_standings = ["Freshman", "Sophomore", "Junior", "Senior", "Other", "5th year"]

worksheet = matches.get_worksheet(1)

row = 1 # update for each little

# matching each little 
cell_list = []
for little in littles[1:len(littles)]:
    key = little[7]
    mapping[key] = []
    little_background = little[13].split(", ")
    little_race = little[17].split(", ")
    little_interests = little[19].split(", ")
    little_living = little[14].split(", ")
    row += 1
    col = 1
    big_list = []
    for big in bigs[1:len(bigs)]:
        # comparing class standing
        points = 0
        if ((class_standings.index(big[8]) - class_standings.index(little[8])) > 0):    # might have to change this
            # comparing number of classes taken
            if (len(big[12]) > len(little[12])):
                    big_living = big[14].split(", ")
                    big_background = big[13].split(", ")
                    big_race = big[17].split(", ")
                    big_interests = big[19].split(", ")    
                    
                    # match identities
                    points += matchBack(little_background, big_background)
                    
                    # match living situation
                    points += matchLiving(little_living, big_living)
                    
                    # match pronouns
                    if (big[15] == little[15]): # hesitant on adding these
                        points += 2
                    
                    # match sexuality
                    if (big[16].lower() == little[16].lower()):
                        points += 2
                    
                    # match race
                    points += matchRace(little_race, big_race)
                    
                    # match interests
                    points += matchInterests(little_interests, big_interests)
                    
                    # add big to map
                    if (points >= 11):
                       big_list.append([points, big[7]])
                       bigs_left.discard(big[7])

    sorted_list = sorted(big_list, key=lambda x: x[0], reverse=True)  
    for big in sorted_list:
        mapping[key].append(big[0]) # points
        mapping[key].append(big[1]) # cse email
    values = mapping[key]
    values = [key] + values
    
    # google sheets goes from A-Z
    if (len(values) > 26):
        values = values[0:25]

    end_col = chr(ord('A') + len(values) - 1)
    col_range = 'A' + str(row) + ':' + end_col + str(row)
    if (len(values) == 0):
        col_range = 'A' + str(row)
    curr_val = {'range': col_range, 'values': [values]}
    cell_list.append(curr_val)

# print(cell_list)

# adding bigs
worksheet.batch_update(cell_list)
# adding littles to spreadsheet


print(bigs_left)

# row will always change col will be A


