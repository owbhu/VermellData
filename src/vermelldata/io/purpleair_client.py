from datetime import datetime, timezone
def fetch_recent_readings():
    now = datetime.now(timezone.utc).replace(microsecond=0)
    return [
        {"sensor_id":"demo_sensor_1","source":"purpleair","lat":41.354,"lon":2.126,"pm25":9.3,"pm10":12.1,"temp":22.4,"humidity":58.0,"ts":now},
        {"sensor_id":"demo_sensor_2","source":"purpleair","lat":41.361,"lon":2.107,"pm25":14.6,"pm10":20.2,"temp":23.0,"humidity":55.2,"ts":now},
    ]
