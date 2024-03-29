# The DynamoDB is defined with the following key
# partition key = device_id
# sort key = timestamp

from boto3.dynamodb.conditions import Key
import boto3

# load the table ()
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('art337-lora')

# print the creation date about the table
print(table.creation_date_time)

# create item; partition key and sort key (optional) must be provided for write
# attribute can added or missed freely
def write2LoraDynamoDB(json_object):
   table.put_item(
      Item={
	         'timestamp': json_object["timestamp"],
	         'header': json_object["header"],
           'device_id': json_object["device_id"],
	         'interval_count': json_object["interval_count"],
	         'data1': json_object["data1"],
	         'data2': json_object["data2"],
	         'rssi': json_object["rssi"],
	         'snr': json_object["snr"],
	         'cur': json_object["cur"],
           'crc': json_object["crc"],
	         'tailer': json_object["tailer"]
       }
   )


# test for write
json_object = {"timestamp": "1655975523", "header": "68", "device_id": "b0f0", "interval_count": "11", "data1": "3281ba", "data2": "3281ba", "rssi": "1f", "snr": "d1", "cur": "21", "crc": "04", "tailer": "16"}
write2LoraDynamoDB(json_object)


# test for read
print("=================================================")
response = table.get_item(
    Key={
        'device_id': 'b0f0',
	      'timestamp': '1656053050'
    }
)
item = response['Item']
print(item)

print("=================================================")
response = table.query(
  KeyConditionExpression=Key('device_id').eq('b0f0') & Key('timestamp').begins_with('16560530')
)
print(response['Items'])

print("=================================================")
response = table.query(
  KeyConditionExpression=Key('device_id').eq('b0f0')
)
print(response['Items'])
print("=================================================")



//=========================================================================================================================================//
// for nodejs; query partition key (location) and sortkey (timestamp) example
async function getRadarImagesResults(location_name){
   try{
        // location is reserved keyword for dynamodb; therefore ExpressionAttributeNames is needed; "#dynobase_" just like the conversion
        const params = {
            TableName: TABLE_NAME_FORECAST_RADAR,
            KeyConditionExpression: '#dynobase_location = :loc AND #dynobase_timestamp >= :ts',
            ExpressionAttributeValues: {
            ':loc': {S: 'sww'},
            ':ts': {S: '202302081030'}
            },
            ExpressionAttributeNames: { "#dynobase_timestamp": "timestamp", "#dynobase_location": "location" }
        };

        const data = await dynamoDb.query(params).promise();
        return {"data": data.Items}
    }catch (err) {
        console.log("Error loading item: ", err);
        return {'success': false, 'data': "Load data failed!"}
    }  
}
//=========================================================================================================================================//
data read from the dynamodb will have something like the following; eg {"N":"11111"}
{
    "updated_at":{"N":"146548182"},
    "uuid":{"S":"foo"},
    "status":{"S":"new"}
}

use the AWS function (AWS.DynamoDB.Converter.unmarshall) to decode it
AWS.DynamoDB.Converter.unmarshall({
    "updated_at":{"N":"146548182"},
    "uuid":{"S":"foo"},
    "status":{"S":"new"}
})

after running the above code, it gives:
{ updated_at: 146548182, uuid: 'foo', status: 'new' }








