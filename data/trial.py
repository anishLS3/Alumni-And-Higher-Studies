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

    div_list_experience = section_experience.find_element(By.CLASS_NAME, "pvs-list__outer-container")
    experience_coll = div_list_experience.find_elements(By.CSS_SELECTOR, "li.artdeco-list__item")

    final_exp_list = []

    for exp in experience_coll:
        temp_coll = {}
        profile_component_entity = exp.find_element(By.XPATH, "./div[@data-view-name='profile-component-entity']")

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
            elif re.search(".*(yr|mo)+.*",raw_t):
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
            "small": small_t
        }


        try:
            other_div = right_flex_div.find_element(By.XPATH, "./div[2]")         
            further_nest = other_div.find_elements(By.XPATH, "./ul/li/div[@data-view-name='profile-component-entity']")
        except:
            pass
        else:
            temp_coll.update({"sub_exp":[]})

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
                    elif re.search(".*(yr|mo)+.*",raw_nt):
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

    print("\n\n\n")
    print(final_exp_list)

        # img_src = exp.find_element(By.TAG_NAME, "img").get_attribute("src")
        # if re.match("data.*",img_src):
        #     img_src = None

        # print("\nStart\n")
        # for x in spans_list:
        #     print(x.text)
        # print("\nOver\n")

    




driver = webdriver.Firefox()
# Opening linkedIn's login page
driver.get("https://linkedin.com/uas/login")

# waiting for the page to load
time.sleep(10)

# entering username
username = driver.find_element(By.NAME, "session_key")

# In case of an error, try changing the element
# tag used here.
username.clear()
username.click()
# Enter Your Email Address
username.send_keys("anishnaraswamy@gmail.com")  

# entering password
pword = driver.find_element(By.NAME, "session_password")
# In case of an error, try changing the element 
# tag used here.
pword.clear()
pword.click()
# Enter Your Password
pword.send_keys("Anirudh1!")

# Clicking on the log in button
# Format (syntax) of writing XPath --> 
# //tagname[@attribute='value']
driver.find_element(By.XPATH, "//button[@type='submit']").click()
# In case of an error, try changing the

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

    with open("studentdetails.json","r") as readFile:
        studentDetails = json.load(readFile)
    
    finalCollection = []

    driver.get("https://www.linkedin.com/in/aadhithya-b-kailash-195b115b/")

    time.sleep(10)

    #temporary (finding elements by class names instead of a permanent id; susceptible to id changes)
    #name_heading = driver.find_element(By.CLASS_NAME,"text-heading-xlarge.inline.t-24.v-align-middle.break-words")
    scaffold_main = driver.find_element(By.XPATH, "//main")
    profile_card = scaffold_main.find_element(By.CLASS_NAME, "artdeco-card")
    profile_img = profile_card.find_element(By.CLASS_NAME, "pv-top-card-profile-picture__image")

    profile_name = profile_card.find_element(By.XPATH, "//h1").text
    profile_job = profile_card.find_element(By.CLASS_NAME, "text-body-medium").text
    # Doesn't work: profile_location = profile_card.find_element(By.XPATH, "text-body-small")

    #will give a weird link if the profile does not have a profile picture
    img_src = profile_img.get_attribute("src")
    
    if re.match("data.*",img_src):
        img_src = None

    experience_list = get_experience(scaffold_main=scaffold_main)
    
    print(experience_list)


    # scaffold_main = driver.find_element(By.XPATH, "//main")
    # skills_list = get_skills(scaffold_main=scaffold_main, driver=driver)
    
    # scaffold_main = driver.find_element(By.XPATH, "//main")
    # awards_list = get_awards(scaffold_main=scaffold_main, driver=driver)
    
    # scaffold_main = driver.find_element(By.XPATH, "//main")
    # volunteer_list = get_volunteering(scaffold_main=scaffold_main, driver=driver)

    # scaffold_main = driver.find_element(By.XPATH, "//main")
    # publications_list = get_publications(scaffold_main=scaffold_main, driver=driver)

    # scaffold_main = driver.find_element(By.XPATH, "//main")
    # education_list = get_education(scaffold_main=scaffold_main, driver=driver)

    # final_json = {
    #     "register_num": register_num,
    #     "profile_name": profile_name,
    #     "profile_img": img_src,
    #     "profile_job": profile_job,
    #     "experience": experience_list,
    #     "skills": skills_list,
    #     "awards": awards_list,
    #     "volunteering": volunteer_list,
    #     "publications": publications_list,
    #     "education": education_list
    # }
    # return final_json
    