const mongoose = require('mongoose');
const Schema = mongoose.Schema

const DomainsSchema = new Schema(
    {
        name: {
            type: String,
            required: [true, "A Skill should be named!"]
        },
        lower_name: {
            type: String, 
            required: true
        },
        skills: [{
            type: Schema.Types.ObjectId,
            ref: 'skills',
        }],
        students: [{
            type: Schema.Types.ObjectId,
            ref: 'profiles',
        }]
        
    },{
        collection: 'Domains',
        versionKey: false
    }
)

const Domains = mongoose.model('domains', DomainsSchema, 'Domains')

module.exports = Domains;