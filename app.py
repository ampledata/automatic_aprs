#!/usr/bin/env python

import os
import json

import aprs
import aprs.util
import aprs.geo_util
import flask


APRSApp = flask.Flask(__name__)


# u'location': {u'ts': 1475531304740, u'lon': -94.7016, u'accuracy_m': 10, u'lat': 41.3578}
CALLSIGN = 'W2GMD-A'

@APRSApp.route('/', methods=['POST'])
def slash():
    aprs_conn = aprs.APRS('AUTOMATIC', '15600')
    aprs_conn.connect()

    post_data = json.loads(flask.request.data)
    if 'location' in post_data:
        location = post_data['location']
    else:
        return 'OK'

    frame = {
        'destination': 'APRS',
        'path': 'TCPIP',
        'source': CALLSIGN,
        'text': "!%s\\%s7Automatic-to-APRS gateway." %
            (aprs.geo_util.dec2dm_lat(location['lat']),
             aprs.geo_util.dec2dm_lng(location['lon']))
    }

    aprs_frame = aprs.util.format_aprs_frame(frame)
    print(aprs_frame)

    aprs_result = aprs_conn.send(aprs_frame, protocol='TCP')
    print(aprs_result)

    return 'OK'


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    APRSApp.run(host='0.0.0.0', port=port)
