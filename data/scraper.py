from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from gmail.getCode import getCode
import time
import re
import json

def get_experience(scaffold_main):
    try:
        experience_anchor = scaffold_main.find_element(By.ID, "experience")
        section_experience = experience_anchor.find_element(By.XPATH, "..")
    except:
        return None

    experience_coll = section_experience.find_elements(By.CSS_SELECTOR, "li.artdeco-list__item")

    final_exp_list = []

    for exp in experience_coll:
        temp_coll = {}
        profile_component_entity = exp.find_element(By.XPATH, "./div[@data-view-name='profile-component-entity']")

        try:
            img_src = profile_component_entity.find_element(By.TAG_NAME, "img").get_attribute("src")
            if re.match(r"data.*",img_src):
                    img_src = None
        except:
            img_src = None

        right_flex_div = profile_component_entity.find_element(By.XPATH, "./div[2]")
        req_text_div = right_flex_div.find_element(By.XPATH, "./div[1]")
        spans_text = req_text_div.find_elements(By.CSS_SELECTOR, "span.visually-hidden")

        big_t = ""
        exp_t = None
        small_t = ""

        counter = 0
        for text_el in spans_text:
            raw_t = text_el.text
            
            if counter == 0:
                big_t = raw_t
                counter += 1
                continue
            elif re.search(r".*(yr|mo)+.*",raw_t):
                exp_t = raw_t
            else:
                if small_t == "":
                    small_t += raw_t
                else:
                    small_t += "\n" + raw_t
        
        small_t = small_t if small_t != "" else None

        temp_coll = {
            "big": big_t,
            "exp": exp_t,
            "small": small_t,
            "sub_exp":[]
        }


        try:
            other_div = right_flex_div.find_element(By.XPATH, "./div[2]")         
            further_nest = other_div.find_elements(By.XPATH, "./ul/li/div[@data-view-name='profile-component-entity']")
        except:
            pass
        else:
            for nested_role in further_nest:
                nest_rflex_div = nested_role.find_element(By.XPATH, "./div[2]")
                nest_rtext_div = nest_rflex_div.find_element(By.XPATH, "./div[1]")
                nest_spans_text = nest_rtext_div.find_elements(By.CSS_SELECTOR, "span.visually-hidden")

                big_nt = ""
                exp_nt = None
                small_nt = ""

                counter = 0
                for ntext_el in nest_spans_text:
                    raw_nt = ntext_el.text
                    
                    if counter == 0:
                        big_nt = raw_nt
                        counter += 1
                        continue
                    elif re.search(r".*(yr|mo)+.*",raw_nt):
                        exp_nt = raw_nt
                    else:
                        if small_nt == "":
                            small_nt += raw_nt
                        else:
                            small_nt += "\n" + raw_nt
                
                small_nt = small_nt if small_nt != "" else None

                n_coll = {
                    "big": big_nt,
                    "exp": exp_nt,
                    "small": small_nt
                }

                temp_coll["sub_exp"].append(n_coll)
        
        print(temp_coll)
        final_exp_list.append(temp_coll)

    return final_exp_list


def get_skills(scaffold_main, driver):
    try:
        skills_anchor = scaffold_main.find_element(By.ID, "skills")
        section_skills = skills_anchor.find_element(By.XPATH, "..")
    except:
        return None

    try:
        div_footer = section_skills.find_element(By.CLASS_NAME, "pvs-list__footer-wrapper")
        expand_skills = div_footer.find_element(By.CSS_SELECTOR,"a.artdeco-button")
        expand_skills.click()
    except:
        list_skills = section_skills.find_elements(By.XPATH, "//a[@data-field='skill_page_skill_topic']")
    else:
        time.sleep(5)
        skills_scaffold_main = driver.find_element(By.TAG_NAME, "main")
        list_skills = skills_scaffold_main.find_elements(By.XPATH, "//a[@data-field='skill_page_skill_topic']")

    final_skills_list = []

    for skill in list_skills:
        skill_text = skill.find_element(By.CSS_SELECTOR, "span.visually-hidden").text
        final_skills_list.append(skill_text)
    
    try:
        goback_button = skills_scaffold_main.find_element(By.XPATH, "//button[@aria-label='Back to the main profile page']")
        goback_button.click()
    except:
        pass
    else:    
        time.sleep(3)
    
    final_skills_list = [x for x in final_skills_list if x != '']
    return final_skills_list

def get_awards(scaffold_main, driver):
    try:
        awards_anchor = scaffold_main.find_element(By.ID, "honors_and_awards")
        section_awards = awards_anchor.find_element(By.XPATH, "..")
    except:
        return None

    try:
        div_footer = section_awards.find_element(By.CLASS_NAME, "pvs-list__footer-wrapper")
        expand_awards = div_footer.find_element(By.CSS_SELECTOR,"a.artdeco-button")
        expand_awards.click()
    except:
        list_awards = section_awards.find_elements(By.CSS_SELECTOR, "li.artdeco-list__item")
    else:
        time.sleep(5)

        awards_scaffold_main = driver.find_element(By.TAG_NAME, "main")
        list_awards = awards_scaffold_main.find_elements(By.CSS_SELECTOR, "li.artdeco-list__item")

    final_awards_list = []

    for award in list_awards:
        award_text_coll = award.find_elements(By.CSS_SELECTOR, "span.visually-hidden")

        midVar = None
        dateVar = None

        try:        
            date_sep = re.search(r"(.*) \u00b7 (.*)", award_text_coll[1].text)
            if date_sep:
                midVar = date_sep.group(1)
                dateVar = date_sep.group(2)
            if re.match(r".* \d{4}", award_text_coll[1].text):
                dateVar = award_text_coll[1].text
        except:
            pass
        final_awards_list.append({"big":award_text_coll[0].text, "mid":midVar, "date":dateVar})
    
    try:
        goback_button = awards_scaffold_main.find_element(By.XPATH, "//button[@aria-label='Back to the main profile page']")
        goback_button.click()
    except:
        pass
    else:
        time.sleep(3)

    return final_awards_list

def get_publications(scaffold_main, driver):
    try:
        pub_anchor = scaffold_main.find_element(By.ID, "publications")
        section_pub = pub_anchor.find_element(By.XPATH, "..")
    except:
        return None

    try:
        div_footer = section_pub.find_element(By.CLASS_NAME, "pvs-list__footer-wrapper")
        expand_pubs = div_footer.find_element(By.CSS_SELECTOR,"a.artdeco-button")
        expand_pubs.click()
    except:
        list_pubs = section_pub.find_elements(By.CSS_SELECTOR, "li.artdeco-list__item")
    else:
        time.sleep(5)

        pubs_scaffold_main = driver.find_element(By.TAG_NAME, "main")
        list_pubs = pubs_scaffold_main.find_elements(By.CSS_SELECTOR, "li.artdeco-list__item")

    final_pubs_list = []

    for pub in list_pubs:
        pub_text_coll = pub.find_elements(By.CSS_SELECTOR, "span.visually-hidden")
        date_sep = re.search(r"(.*) \u00b7 (.*)", pub_text_coll[1].text)

        journalVar = None
        dateVar = None

        if date_sep:
            journalVar = date_sep.group(1)
            dateVar = date_sep.group(2)
        
        try:
            pub_link = pub.find_element(By.CSS_SELECTOR, "a.artdeco-button").get_attribute("href")
            print(pub_link)
        except:
            pub_link = None
        
        descVar = None
        if len(pub_text_coll[2:]) != 0:
            
            if journalVar is None:
                journalVar = pub_text_coll[1].text
            
            descVar = pub_text_coll[2].text

        final_pubs_list.append({"title":pub_text_coll[0].text, "journal":journalVar, "date":dateVar, "desc": descVar, "pub_link": pub_link})
    
    try:
        goback_button = pubs_scaffold_main.find_element(By.XPATH, "//button[@aria-label='Back to the main profile page']")
        goback_button.click()
    except:
        pass
    else:
        time.sleep(3)

    return final_pubs_list

def get_volunteering(scaffold_main, driver):
    try:
        volunteering_anchor = scaffold_main.find_element(By.ID, "volunteering_experience")
        section_volunteering = volunteering_anchor.find_element(By.XPATH, "..")
    except:
        return None

    try:
        div_footer = section_volunteering.find_element(By.CLASS_NAME, "pvs-list__footer-wrapper")
        expand_volunteering = div_footer.find_element(By.CSS_SELECTOR,"a.artdeco-button")
        expand_volunteering.click()
    except:
        list_volunteering = section_volunteering.find_elements(By.CSS_SELECTOR, "li.artdeco-list__item")
    else:
        time.sleep(5)
        volunteering_scaffold_main = driver.find_element(By.TAG_NAME, "main")
        list_volunteering = volunteering_scaffold_main.find_elements(By.CSS_SELECTOR, "li.artdeco-list__item")

    final_volunteering_list = []

    for event in list_volunteering:
        event_text_coll = event.find_elements(By.CSS_SELECTOR, "span.visually-hidden")
        
        durVar = None
        expVar = None

        try:
            date_sep = re.search(r"(.*) \u00b7 (.*)", event_text_coll[2].text)
        except:
            pass
        else:
            if date_sep:
                durVar = date_sep.group(1)
                expVar = date_sep.group(2)

        
        try:
            img_src = event.find_element(By.TAG_NAME, "img").get_attribute("src")
            if re.match(r"data.*",img_src):
                img_src = None
        except:
            img_src = None

        final_volunteering_list.append({"big":event_text_coll[0].text, "mid":event_text_coll[1].text, "dur":durVar, "exp":expVar, "img":img_src})
    
    try:
        goback_button = volunteering_scaffold_main.find_element(By.XPATH, "//button[@aria-label='Back to the main profile page']")
        goback_button.click()
    except:
        pass
    else:
        time.sleep(3)

    return final_volunteering_list

def get_education(scaffold_main, driver):
    try:
        education_anchor = scaffold_main.find_element(By.ID, "education")
        section_education = education_anchor.find_element(By.XPATH, "..")
    except:
        return None

    try:
        div_footer = section_education.find_element(By.CLASS_NAME, "pvs-list__footer-wrapper")
        expand_education = div_footer.find_element(By.CSS_SELECTOR,"a.artdeco-button")
        expand_education.click()
    except:
        list_education = section_education.find_elements(By.CSS_SELECTOR, "li.artdeco-list__item")
    else:
        time.sleep(5)

        education_scaffold_main = driver.find_element(By.TAG_NAME, "main")
        list_education = education_scaffold_main.find_elements(By.CSS_SELECTOR, "li.artdeco-list__item")

    final_education_list = []

    for institution in list_education:
        institution_text_coll = institution.find_elements(By.CSS_SELECTOR, "span.visually-hidden")
        
        extraVar = None
        if len(institution_text_coll[3:]) != 0:
            extraVar = "\n".join([x.text for x in institution_text_coll[3:] if (x.text != '' and "\u00b7" not in x.text)])

        try:
            img_src = institution.find_element(By.TAG_NAME, "img").get_attribute("src")
            if re.match(r"data.*",img_src):
                img_src = None
        except:
            img_src = None

        try:
            durVar, midVar = None, None
            if re.search(r".*\d{4} - .*\d{4}", institution_text_coll[2].text):
                durVar = institution_text_coll[2].text
                midVar = institution_text_coll[1].text
            
            final_education_list.append({"big":institution_text_coll[0].text, "mid":midVar, "dur":durVar,"img_src":img_src, "desc":extraVar})
        except:
            durVar, midVar = None, None
            try:
                if re.search(r".*\d{4} - .*\d{4}", institution_text_coll[1].text):
                    durVar = institution_text_coll[1].text
                else:
                    midVar = institution_text_coll[1].text
            except:
                pass
            final_education_list.append({"big":institution_text_coll[0].text, "mid":None, "dur":durVar,"img_src":img_src,"desc":extraVar})

    try:
        goback_button = education_scaffold_main.find_element(By.XPATH, "//button[@aria-label='Back to the main profile page']")
        goback_button.click()
    except:
        pass
    else:
        time.sleep(3)

    return final_education_list


def getData(driver, register_num, url):
    print(url)
    driver.get(url)

    time.sleep(10)

    scaffold_main = driver.find_element(By.XPATH, "//main")
    profile_card = scaffold_main.find_element(By.CLASS_NAME, "artdeco-card")
    profile_img = profile_card.find_element(By.CLASS_NAME, "pv-top-card-profile-picture__image--show")

    profile_name = profile_card.find_element(By.XPATH, "//h1").text
    profile_job = profile_card.find_element(By.CLASS_NAME, "text-body-medium").text
    # Doesn't work: profile_location = profile_card.find_element(By.XPATH, "text-body-small")

    #will give a weird link if the profile does not have a profile picture
    img_src = profile_img.get_attribute("src")
    
    if re.match(r"data.*",img_src):
        img_src = None

    experience_list = get_experience(scaffold_main=scaffold_main)
    
    scaffold_main = driver.find_element(By.XPATH, "//main")
    skills_list = get_skills(scaffold_main=scaffold_main, driver=driver)
    
    scaffold_main = driver.find_element(By.XPATH, "//main")
    awards_list = get_awards(scaffold_main=scaffold_main, driver=driver)
    
    scaffold_main = driver.find_element(By.XPATH, "//main")
    volunteer_list = get_volunteering(scaffold_main=scaffold_main, driver=driver)

    scaffold_main = driver.find_element(By.XPATH, "//main")
    publications_list = get_publications(scaffold_main=scaffold_main, driver=driver)

    scaffold_main = driver.find_element(By.XPATH, "//main")
    education_list = get_education(scaffold_main=scaffold_main, driver=driver)

    final_json = {
        "register_num": register_num,
        "profile_name": profile_name,
        "profile_img": img_src,
        "profile_job": profile_job,
        "experience": experience_list,
        "skills": skills_list,
        "awards": awards_list,
        "volunteering": volunteer_list,
        "publications": publications_list,
        "education": education_list
    }
    return final_json

def main():
    driver = webdriver.Firefox()

    driver.get("https://linkedin.com/uas/login")
    
    time.sleep(10)
    

   # username = driver.find_element(By.NAME, "session_key")

    #username.clear()
    #username.click()

   # username.send_keys("aakashanirudh1234@gmail.com")  

    #pword = driver.find_element(By.NAME, "session_password")

   # pword.clear()
    #pword.click()

  #  pword.send_keys("Myfamilybvaas1!")
    

   # driver.find_element(By.XPATH, "//button[@type='submit']").click()


    captcha_solve = int(input("Did you solve captcha: "))
    if captcha_solve:
        time.sleep(10)
        try:
            emailVerObj = driver.find_element(By.ID, "email-pin-challenge")

            if emailVerObj:
                code = getCode()

                # id if NAME does not work: #input__email_verification_pin
                inputPin = driver.find_element(By.NAME, "pin")
                inputPin.clear()
                inputPin.click()
                inputPin.send_keys(code)

                driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(10)
        except:
            pass

        with open("input/JSON/itdept2024.json","r") as readFile:
            studentDetails = json.load(readFile)
        
        finalCollection = []

        
        flag = 0

        for student in studentDetails:
            register_num = student["register_num"]
            name = student["name"]
            url = student["url"]

            # Uncomment below code if you want to start in-between
            if register_num == "205002113":
                flag = 1
            if not flag:
                with open(f"output/indiv_output/2024/{register_num}.json","r") as readFile:
                    studentOutput = json.load(readFile)
                finalCollection.append(studentOutput)
                continue
        
            studentOutput = getData(driver=driver, register_num=register_num, url=url)
            with open(f"output/indiv_output/2024/{register_num}.json","w") as writeFile:
                json.dump(studentOutput, writeFile, indent=4)

            finalCollection.append(studentOutput)
        
        with open("output/final_output/2024.json","w") as writeFile:
            json.dump(finalCollection, writeFile, indent=4)
        


if __name__ == "__main__":
    main()