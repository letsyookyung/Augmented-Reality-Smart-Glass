import json

def post_attendance(id):
    with open("FaceBase_re.json","r", encoding='utf-8-sig') as jsonFile:
        data = json.load(jsonFile)
#    for d in data:
#        if id == d["ID"]:
#            tmp = d["Attend"]
#            d["Attend"] = 'true'
    for i in range(len(data)):
        if id == data[i]["ID"]:
            tmp = data[i]["Attend"]
            data[i]["Attend"] = 'true'
    with open("FaceBase_re.json","w", encoding='utf-8-sig') as jsonFile:
        json.dump(data, jsonFile)

def get_profile(id):
    with open("FaceBase_re.json",'r',encoding='utf-8-sig') as jsonFile:
        data = json.load(jsonFile)
        for i in range(len(data)):
            if id == data[i]["ID"]:
                stu_id = data[i]["StuID"]
                stu_name = data[i]["Name"]
                stu_major = data[i]["Major"]
                stu_grade = data[i]["Grade"]
                stu_attend = data[i]["Attend"]
                break
        return stu_id, stu_name, stu_major, stu_grade, stu_attend
