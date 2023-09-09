import { createClient, print } from 'redis';


const client = createClient();

client.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

const cities = {
    Portland: 50,
    Seattle: 80,
    'New York': 20,
    Bogota: 20,
    Cali: 40,
    Paris: 2
};

function main() {
    for (const [key, value] of Object.entries(cities)) {
        client.HSET('HolbertonSchools', key, value, print)
    }
    client.HGETALL('HolbertonSchools', (_err, reply) => console.log(reply))
}

client.on('connect', () => {
  console.log('Redis client connected to the server');
  main()
});

