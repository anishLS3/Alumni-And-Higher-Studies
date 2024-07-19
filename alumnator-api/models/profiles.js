const mongoose = require('mongoose')
const Schema = mongoose.Schema

const ProfilesSchema = new Schema(
    {
        register_num: {
            type: String,
            required: [true, "Register number is mandatory"]
        },
        profile_name: {
            type: String,
            required: [true, "Name is mandatory"]
        },
        profile_job: {
            type: String, 
            required: false,
        },
        batch: {
            type: Number,
            required: true,
        },
        phone_number: {
            type: String,
        },
        skills: [String],
        experience: {
            type: Schema.Types.ObjectId,
            ref: 'experience'
        },
        education: {
            type: Schema.Types.ObjectId,
            ref: 'education'
        },
        awards: [{
            big: String,
            mid: String,
            date: String
        }],
        volunteering: [{
            big: String,
            mid: String,
            dur: String,
            exp: String,
            img: String,
        }],
        publications: [{
            title: String,
            journal: String,
            date: String,
            desc: String,
            pub_link: String
        }],
        events: [{
            type: Schema.Types.ObjectId,
            ref: 'events'
        }]
        
    }
)

const Profiles = mongoose.model('profiles', ProfilesSchema, 'Profiles')

module.exports = Profiles;