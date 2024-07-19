const express = require('express')
const mongoose = require('mongoose')
const cors = require('cors')
const dotenv = require('dotenv')
dotenv.config();

const { GoogleGenerativeAI } = require("@google/generative-ai");
const genAI = new GoogleGenerativeAI(process.env.API_KEY);

const { Client, LocalAuth, MessageMedia } = require("whatsapp-web.js");
const qrcode = require('qrcode-terminal');

const Profiles = require('./models/profiles')
const Education = require('./models/education')
const Experience = require('./models/experience')
const Skills = require('./models/skills')
const Domains = require('./models/domains');
const Events = require('./models/events');

const app = express()

app.use(express.json())
app.use(cors())

mongoose.connect("mongodb://localhost:27017/ProfileDB")
.then(() => {
    console.log("Connection successful")
})
.catch(() => {
    console.log("Connection fail")
})

app.get('/', (request, response) => {
    response.send("<p>Hello!</p>")
})


app.get('/api/profiles', async (request, response) => {
    try{
        const query = request.query.q;
        const profiles = (query) ? await Profiles.find({profile_name: {$regex: `^${query}`, $options: "i"} }).sort({register_num: 1})
                                : await Profiles.find({}).sort({register_num: 1});
        response.status(200).json(profiles);

    } catch (error) {
        response.status(500).json({message: error.message})
    } 
})

app.get('/api/profiles/:id', async (request, response) => {
    try{
        const id = request.params.id;
        const profile = await Profiles.findOne({register_num: id});
        const education = await Education.findOne({register_num: id}, {_id: 0, educationArr: 1})
        const experience = await Experience.findOne({register_num: id}, {_id: 0, experienceArr: 1})
        
        const newProfile = {
            register_num: profile.register_num,
            profile_name: profile.profile_name,
            profile_job: profile.profile_job,
            batch: profile.batch,
            education: (education === null) ? null : education.educationArr,
            experience: (experience === null) ? null : experience.experienceArr,
            awards: profile.awards,
            volunteering: profile.volunteering,
            publications: profile.publications,
            skills: profile.skills,
        }
    
        response.status(200).json(newProfile);

    } catch (error) {
        response.status(500).json({message: error.message})
    } 
})

app.get('/api/skills', async (request, response) => {
    try{
        const distinctSkills = await Skills.find({});
        response.status(200).json(distinctSkills);
    } catch (error) {
        response.status(500).json({message: error.message})
    }
})

app.get('/api/domains', async (request, response) => {
    try{
        const domains = await Domains.find({}).collation({locale:'en', strength: 2}).sort({"name":1});
        response.status(200).json(domains);
    } catch (error) {
        response.status(500).json({message: error.message})
    }
})

app.post('/api/domains', async (request, response) => {
    try{
        const domain = await Domains.create(request.body)
        response.status(200).json(domain);
    } catch (error) {
        response.status(500).json({message: error.message})
    }
})

app.get('/api/events', async (request, response) => {
    try{
        const events = await Events.find({}).sort({_id:-1});
        response.status(200).json(events); 
    } catch (error) {
        response.status(500).json({message: error.message})
    }
})

app.post('/api/events', async (request, response) => {
    try{
        const event = await Events.create(request.body)
        response.status(200).json(event);
    } catch (error) {
        response.status(500).json({message: error.message})
    }
})

app.get('/api/events/:id', async (request, response) => {
    try {
        const id = request.params.id;
        const event = await Events.findOne({_id: id})
        response.status(200).json(event)
    } catch (error) {
        response.status(500).json({message: error.message})
    }
})

app.put('/api/events/:id', async (request, response) => {
    try {
        const id = request.params.id;
        const studentsArr = request.body;

        const result = await Events.updateOne({_id: id}, {$push: {students: { $each: studentsArr}}})
        response.status(200).json(result)
    } catch (error) {
        response.status(500).json({message: error.message})
    }
})

app.delete('/api/events/:id', async (request, response) => {
    try {
        const id = request.params.id;
        const respBool = await Events.deleteOne({_id: id})
        response.status(204).end()
    } catch (error) {
        response.status(500).json({message: error.message})
    }
})

app.post('/api/genmessage', async (request, response) => {
    try{
        const model = genAI.getGenerativeModel({model: "gemini-1.5-flash"});

        const prompt = request.body.textPrompt;
        const result = await model.generateContent(prompt);
        const resultResp = await result.response;
        const text = resultResp.text();
        response.status(200).json({"message": text})
    } catch(error){
        console.log(error.message);
        response.status(500).json({message: error.message})
    }
})

const client = new Client({
    puppeteer: {
        headless: true,
        args: ["--no-sandbox"]
    },
    authStrategy: new LocalAuth({
        clientId: "YOUR_CLIENT_ID",
    }),
})

client.initialize(); 
client.on("ready", async () => { 
    console.log("CLIENT OPEN")

    app.post('/api/sendmessage', async (request, response) => {
        console.log("PHONE OPEN")
        const phoneMessages = request.body;
        
            for (const item of phoneMessages) {
                let phone = `91${item.phone}@c.us`;

                if(item.url){
                    const media = await MessageMedia.fromUrl(item.url);
                    await client.sendMessage(phone, media, {caption: item.message})
                }else{
                    await client.sendMessage(phone, item.message)
                }
                console.log(phone, item.message);
            };
            return response.status(200).json({message:"Successfully sent!"})

        })
    
    app.get('/api/getmessage', async (request, response) => {
        let phoneList = request.query.phone
        phoneList = (typeof phoneList !== "object") ? [ phoneList ] : phoneList;
        const finalResponse = []

        for (const item of phoneList) {
            const chat = await client.getChatById(`91${item}@c.us`)
            const result = await chat.fetchMessages(searchOptions={limit:10});
            console.log(result)
            const responseItem = {
                phone: item,
                messages: []
            }
            
            for (const resultItem of result){
                const messageItem = {
                    fromMe: resultItem.fromMe,
                    body: resultItem.body,
                    hasMedia: resultItem.hasMedia
                }
                responseItem.messages.push(messageItem)
            }
            
            finalResponse.push(responseItem);
        };
        
        return response.status(200).json(finalResponse)
    })

})


const PORT = 3002
app.listen(PORT, () => {
    console.log(`Server running on ${PORT}`)
})

