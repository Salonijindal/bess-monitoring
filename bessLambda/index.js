const AWS = require('aws-sdk');
const athena = new AWS.Athena();

const s3Output = 's3://bess-monitoring-output/';  

exports.handler = async (event) => {
    const query = event.query || 'SELECT * FROM "bessdatadb"."bess" limit 10;';

    try {
        const queryExecution = await athena.startQueryExecution({
            QueryString: query,
            QueryExecutionContext: { Database: 'bessdatadb' }, 
            ResultConfiguration: { OutputLocation: s3Output }
        }).promise();

        const queryExecutionId = queryExecution.QueryExecutionId;

        
        let queryStatus = 'RUNNING';
        while (queryStatus === 'RUNNING') {
            const queryExecution = await athena.getQueryExecution({ QueryExecutionId: queryExecutionId }).promise();
            queryStatus = queryExecution.QueryExecution.Status.State;

            if (queryStatus === 'SUCCEEDED') {
                break;
            } else if (queryStatus === 'FAILED' || queryStatus === 'CANCELLED') {
                return {
                    statusCode: 400,
                    body: JSON.stringify({ error: 'Query failed or was cancelled' })
                };
            }
            await new Promise(resolve => setTimeout(resolve, 1000));
        }

        const queryResults = await athena.getQueryResults({ QueryExecutionId: queryExecutionId }).promise();

        const rows = queryResults.ResultSet.Rows.map(row =>
            row.Data.map(field => field.VarCharValue || '')
        );

        return {
            statusCode: 200,
            body: JSON.stringify(rows)
        };

    } catch (error) {
        console.error("Error executing query:", error);
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Error executing query', details: error.message })
        };
    }
};
