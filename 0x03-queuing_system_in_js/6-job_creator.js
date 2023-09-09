import kue from 'kue';

const queue = kue.createQueue();

const jobData = {
    phoneNumber: '07045679939',
    message: 'Account registered',
};

const job = queue.create('push_notification_code', jobData)

job.on('enqueue', () => {
    console.log('Notification job created:', job.id);
}).on('complete', () => {
    console.log('Notification job completed');
}).on('failed', () => {
    console.log('Notification job failed');
}).save()