const mongoose = require('mongoose')
const Schema = mongoose.Schema

const EducationSchema = new Schema(
    {
        register_num: {
            type: String,
            required: true
        },
        educationArr: [{
            big: String,
            mid: String,
            dur: String,
            img_src: String,
            desc: String
        }]
    }
)

const Education = mongoose.model('education', EducationSchema, 'Education')

module.exports = Education;

