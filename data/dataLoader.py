import json
import pymongo
from bson import ObjectId
import re

url = "mongodb://localhost:27017"
client = pymongo.MongoClient(url)

db = client.ProfileDB
profileColl = db.Profiles
skillColl = db.Skills
experienceColl = db.Experience
educationColl = db.Education

with open("data/output/final_output/2022B.json","r") as readFile:
    d = json.load(readFile)
with open("data/output/final_output/2022A.json","r") as readFile:
    d2 = json.load(readFile)
with open("data/output/final_output/2024.json","r") as readFile:
    d3 = json.load(readFile)

d.extend(d2)
total_d = {2022: d, 2024: d3}

x = 1
for batch, profileList in total_d.items():
    phone_number = "9176676138" if batch == 2022 else "9566541288"
    for profile in profileList:
        register_num = "".join(profile.get("register_num").split(" "))
        profile_name = profile.get("profile_name")
        profile_job = profile.get("profile_job")
        experience = profile.get("experience")
        skills = profile.get("skills")
        volunteering = profile.get("volunteering")
        awards = profile.get("awards")
        publications = profile.get("publications")
        education = profile.get("education")

        profileObjId = ObjectId()

        profileDict = {
            "_id": profileObjId,
            "register_num": register_num,
            "profile_name": profile_name,
            "batch": batch,
            "phone_number": phone_number,
        }

        if profile_job is not None:
            profileDict.update({"profile_job": profile_job})

        if skills is not None:
            listSkills = []

            for eachSkill in skills:
                regex = re.compile(eachSkill, re.IGNORECASE)

                respSkill = skillColl.find_one({"lower_name":eachSkill.lower()})
                if respSkill is None:
                    skillObjId = ObjectId()
                    name = eachSkill
                    lower_name = eachSkill.lower()
                    skillColl.insert_one({"_id":skillObjId, "name":name, "lower_name": lower_name, "students":[profileObjId]})
                else:
                    skillColl.update_one({"name": respSkill["name"]},{"$push":{"students": profileObjId}})

                listSkills.append(eachSkill)

            profileDict.update({"skills": listSkills})

        if experience is not None:
            expObjId = ObjectId()

            experienceDict = {
                "_id": expObjId,
                "register_num": register_num,
                "experienceArr": experience
            }

            experienceColl.insert_one(experienceDict)
            profileDict.update({"experience": expObjId})

        if education is not None:
            eduObjId = ObjectId()
        
            educationDict = {
                "_id": eduObjId,
                "register_num": register_num,
                "educationArr": education
            }

            educationColl.insert_one(educationDict)
            profileDict.update({"education": eduObjId})
        
        if awards is not None:
            profileDict.update({"awards": awards})

        if volunteering is not None:
            profileDict.update({"volunteering": volunteering})

        if publications is not None:
            profileDict.update({"publications": publications})

        profileDict.update({"events": []})
        profileColl.insert_one(profileDict)

        print(x)
        x+=1