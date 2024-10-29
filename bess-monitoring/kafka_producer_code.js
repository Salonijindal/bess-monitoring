const { Kafka } = require("kafkajs");

const kafka = new Kafka({
  brokers: [
    "b-3.bessmonitoringmsk.4u6ji5.c4.kafka.ca-central-1.amazonaws.com:9092",
    "b-2.bessmonitoringmsk.4u6ji5.c4.kafka.ca-central-1.amazonaws.com:9092",
    "b-1.bessmonitoringmsk.4u6ji5.c4.kafka.ca-central-1.amazonaws.com:9092",
  ],
});
const producer = kafka.producer();

const statuses = ["operational", "maintenance", "fault"];
const alertTypes = [
  "temperature_high",
  "low_voltage",
  "over_current",
  "battery_depleted",
];

async function produceData() {
  await producer.connect();
  setInterval(async () => {
    let randomDeviceNumber = Math.floor(Math.random() * (100 - 1 + 1)) + 1;
    const message = {
      device_id: `bess${randomDeviceNumber}`, // random device id
      timestamp: new Date(Date.now()).toISOString(),
      voltage: parseFloat((360 + Math.random() * 40).toFixed(2)), // Volts between 360 and 400
      current: parseFloat((10 + Math.random() * 10).toFixed(2)), // Amperes between 10 and 20
      temperature: parseFloat((20 + Math.random() * 25).toFixed(1)), // Celsius between 20 and 45
      state_of_charge: parseFloat((10 + Math.random() * 90).toFixed(1)), // Percentage between 10 and 100
      power_output: parseFloat((4500 + Math.random() * 1500).toFixed(2)), // Watts between 4500 and 6000
      frequency: parseFloat((59.9 + Math.random() * 0.3).toFixed(1)), // Hertz around 60
      status: statuses[Math.floor(Math.random() * statuses.length)],
      alerts: Array.from(
        { length: Math.floor(Math.random() * 3) },
        () => alertTypes[Math.floor(Math.random() * alertTypes.length)]
      ),
    };
    await producer.send({
      topic: "bess-monitoring-topic",
      messages: [{ value: JSON.stringify(message) }],
    });
  }, 10); // data produced after every 10 milliseconds
}

produceData().catch(console.error);

process.on("SIGINT", async () => {
  await producer.disconnect();
  process.exit(0);
});
