import google.generativeai as genai
import pprint

genai.configure(api_key="AIzaSyCsG1AnVaKsJkyPjn7cqYVgfj8ToSR8tDQ")
model = genai.GenerativeModel('gemini-1.5-flash-latest')

response = model.generate_content("Frame a message inviting an alumnus of the I.T department of your college for a hackathon titled 'Envision' on 28th October 2024, and ask him to fill the google form link if he wishes to attend the event.")
print(response.text)

#for model in genai.list_models():
#    pprint.pprint(model)