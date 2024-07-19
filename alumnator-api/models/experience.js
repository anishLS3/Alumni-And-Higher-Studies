const mongoose = require('mongoose')
const Schema = mongoose.Schema

const ExperienceSchema = new Schema(
    {
        register_num: {
            type: String,
            required: true
        },
        experienceArr: [{
            
            big: {
                type: String,
                required: true
            },
            exp: String,
            small: String,
            sub_exp: [{
                big: String,
                exp: String,
                small: String
            }]
        
        }]
    }
)

const Experience = mongoose.model('experience', ExperienceSchema, 'Experience')

module.exports = Experience;