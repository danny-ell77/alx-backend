import express from "express";
import { createQueue } from "kue";
import { promisify } from 'util';
import { createClient } from 'redis';

const client = createClient();

const app = express()

const port = 1245;

let reservationEnabled  = true

client.on('error', (err) => {
    console.log('Redis client not connected to the server:', err.toString());
});


client.on('connect', () => {
    console.log('Redis client connected to the server');
});


const reserveSeat = (number) => {
    client.SET('available_seats', number)
}

const getCurrentAvailableSeats = async () => {
    return promisify(client.GET).bind(client)('available_seats')
}

const queue = createQueue();

app.get('/available_seats', (req, res) => {
    if (!reservationEnabled) {
        return res.json({ "status": "Reservation are blocked" })
    }
    getCurrentAvailableSeats().then((reply) => res.json({numberOfAvailableSeats: reply}))
})

app.get('/reserve_seat', (req, res) => {
    if (!reservationEnabled) {
        return res.json({ "status": "Reservation are blocked" })
    }
    try {
        const job = queue.create("reserve_seat")
        job.on('complete', () => {
             console.log(`Seat reservation job ${job.id} completed`);
            }).on('failed', () => {
                console.log('Seat reservation job failed');
            }).save()
        return res.json({ "status": "Reservation in process" })
    }catch (e) {
        return res.json({ "status": "Reservation failed" })   
    }
})

app.get('/process', (req, res) => {
    queue.process('reserve_seat', (job, done) => {
        getCurrentAvailableSeats().then((reply) => {
            const availableSeats = (+reply || 0) - 1
            reserveSeat(availableSeats)
            if (availableSeats >= 0) {
                if (availableSeats === 0) reservationEnabled = false
                done()
            } else {
                done(new Error('Not enough seats available'))
            }
        })
    })
    res.json({ "status": "Queue processing" })
})

app.listen(port, () => {
    console.log(`Server listening on PORT ${port}`);
    reserveSeat(50)
});

