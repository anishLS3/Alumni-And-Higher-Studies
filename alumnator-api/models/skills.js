const mongoose = require('mongoose');
const Schema = mongoose.Schema

const SkillsSchema = new Schema(
    {
        name: {
            type: String,
            required: [true, "A Skill should be named!"]
        },
        lower_name: {
            type: String, 
            required: true
        },
        students: [{
            type: Schema.Types.ObjectId,
            ref: 'profiles',
        }]
    }
)

const Skills = mongoose.model('skills', SkillsSchema, 'Skills')

module.exports = Skills;