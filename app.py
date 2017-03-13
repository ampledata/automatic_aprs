#!/usr/bin/env python

import os
import json

import aprs
import flask


APRSApp = flask.Flask(__name__)


# u'location': {u'ts': 1475531304740, u'lon': -94.7016, u'accuracy_m': 10, u'lat': 41.3578}
CALLSIGN = 'W2GMD-A'

@APRSApp.route('/', methods=['POST'])
def slash():
    aprs_conn = aprs.TCP(
        os.environ.get('APRS_LOGIN', 'AUTOMATIC'), os.environ.get('APRS_PORT'))
    aprs_conn.start()

    post_data = json.loads(flask.request.data)
    if 'location' in post_data:
        location = post_data['location']
    else:
        return 'OK'

    if 'vehicle' in post_data:
        vehicle = post_data['vehicle']['id']
    else:
        vehicle = ''

    print locals()

    frame = aprs.Frame()
    frame.destination = 'APYSAU'
    frame.path = ['TCPIP']
    frame.source = CALLSIGN
    frame.text = ("!%s\\%s7Automatic-to-APRS gateway. http://ampledata.org" %
        (aprs.dec2dm_lat(location['lat']), aprs.dec2dm_lng(location['lon'])))

    print frame
    aprs_result = aprs_conn.send(frame)
    print aprs_result

    return 'OK'


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    APRSApp.run(host='0.0.0.0', port=port)
