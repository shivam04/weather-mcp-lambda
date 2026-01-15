
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import json
from urllib import request, parse


def lambda_handler(event, context):
    # Extract tool name from context
    tool_name = context.client_context.custom.get('bedrockAgentCoreToolName', 'unknown')
    print(f"tool name: {tool_name}")

    if 'get_weather' in tool_name:
        api_key = 'api-key'
        base_url = "http://api.weatherapi.com/v1/current.json?"
        complete_url = base_url + "key=" + api_key + "&q=" + parse.quote(event.get('location', 'Unknown'), safe='')
        print(f"complete url: {complete_url}")
        req = request.Request(
            complete_url
        )
        x = None
        with request.urlopen(req) as res:
            x = json.loads(res.read().decode())
        if x is None:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Unknown location'})
            }
        print(f"weather data: {x}")
        y = x["current"]
        current_temperature = str(y["temp_f"]) + " F"
        condition = y["condition"]["text"]
        time_zone = x['location']["tz_id"]
        return {
            'statusCode': 200,
            'body': json.dumps({
                'location': event.get('location', 'Unknown'),
                'temperature': current_temperature,
                'condition': condition,
                'time_zone': time_zone
            })
        }
    elif 'get_time' in tool_name:
        time_zone = ZoneInfo(event.get('timezone', 'UTC'))
        print(f"time zone: {time_zone}")
        return {
            'statusCode': 200,
            'body': json.dumps({
                'timezone': event.get('timezone', 'UTC'),
                'time': datetime.now(time_zone).strftime('%H:%M:%S')
            })
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Unknown tool'})
        }
