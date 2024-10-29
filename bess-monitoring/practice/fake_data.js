const faker = require("faker");

// Configuration for data generation
const numDevices = 5; // Number of BESS units
const numRecords = 100; // Number of records per device

// Possible statuses and alert types
const statuses = ["operational", "maintenance", "fault"];
const alertTypes = [
  "temperature_high",
  "low_voltage",
  "over_current",
  "battery_depleted",
];

// Function to generate random telemetry data
function generateTelemetryData(numRecords, numDevices) {
  const records = [];

  for (let i = 0; i < numRecords; i++) {
    for (let deviceId = 1; deviceId <= numDevices; deviceId++) {
      const record = {
        device_id: `bess-${deviceId}`,
        timestamp: new Date(Date.now() - i * 10000).toISOString(), // Decrease timestamp by 10 seconds per record
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
      records.push(record);
    }
  }

  return records;
}

// Generate data and display it
const fakeTelemetryData = generateTelemetryData(numRecords, numDevices);
console.log(JSON.stringify(fakeTelemetryData, null, 2));


