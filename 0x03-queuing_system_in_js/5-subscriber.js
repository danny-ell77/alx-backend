import { createClient } from 'redis';

const EXT_MSG = 'KILL_SERVER';

const client = createClient();

client.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

client.subscribe('holberton school channel')

client.on('message', (channel, message) => {
    console.log(message)
    if (message === EXT_MSG) {
        client.unsubscribe();
        client.quit()
    }
})

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

