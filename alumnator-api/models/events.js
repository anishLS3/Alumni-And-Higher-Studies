const mongoose = require('mongoose')
const Schema = mongoose.Schema

const EventsSchema = new Schema(
    {
        event_name: {
            type: String,
            required: true
        },
        date: {
            from: {
                type: Date,
                required: true,
            },
            to: {
                type: Date,
                required: true,
            }
        },
        event_venue: {
            type: String,
            required: true,
        },
        additional_info: {
            type: String,
            required: true,
        },
        template: {
            type: String,
            required: true,
        },
        students: [{
            name: {
                type: String,
                required: true,
            },
            batch: {
                type: Number,
                required: true,
            },
            register_num: {
                type: String,
                required: true,
            },
            phone: {
                type: String,
                required: true,
            }
        }]
    }
)

const Events = mongoose.model('events', EventsSchema, 'Events');
module.exports = Events;
