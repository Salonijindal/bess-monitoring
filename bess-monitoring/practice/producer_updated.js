const faker = require("faker");
const fs = require("fs");

// Configuration for data generation
const numDevices = 500; // Number of BESS units
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
        device_id: `bess-${Math.floor(Math.random() * (100 - 1 + 1)) + 1}`,
        voltage: `${parseFloat((360 + Math.random() * 40).toFixed(2))}`, 
        current: `${parseFloat((10 + Math.random() * 10).toFixed(2))}`, 
        temperature: `${parseFloat((20 + Math.random() * 25).toFixed(1))}`, 
        state_of_charge: `${parseFloat((10 + Math.random() * 90).toFixed(1))}`, 
        power_output: `${parseFloat((4500 + Math.random() * 1500).toFixed(2))}`, 
        frequency: `${parseFloat((59.9 + Math.random() * 0.3).toFixed(1))}`, 
        status: statuses[Math.floor(Math.random() * statuses.length)],
        alert: alertTypes[Math.floor(Math.random() * alertTypes.length)],
      };
      console.log(JSON.stringify(record))
    //   records.push(record);
    }
  }

  return records;
}

// Generate data and display it
const fakeTelemetryData = generateTelemetryData(numRecords, numDevices);
// console.log(JSON.stringify(fakeTelemetryData));


// fs.writeFile("data.json", data, (error) => {
    // throwing the error
    // in case of a writing problem
    // if (error) {
      // logging the error
//       console.error(error);
  
//       throw error;
//     }
  
//     console.log("data.json written correctly");
//   });