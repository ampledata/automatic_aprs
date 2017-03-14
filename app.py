#!/usr/bin/env python

import os
import json

import aprs
import flask



APRSApp = flask.Flask(__name__)

CALLSIGN_MAP = 'callsign_map.json'


@APRSApp.route('/', methods=['POST'])
def slash():
    post_data = json.loads(flask.request.data)

    if ('location' in post_data and 'vehicle' in post_data and
            'id' in post_data['vehicle']):
        location = post_data['location']
        vehicle_id = post_data['vehicle']['id']
    else:
        print 'No location or vehicle data in POST.'
        print locals()
        return 'OK'

    callsign_map = json.load(open(CALLSIGN_MAP))

    if vehicle_id in callsign_map:
        callsign = callsign_map[vehicle_id]
    else:
        print 'No valid vehicle_id to callsign mapping found.'
        print locals()
        return 'OK'

    aprs_conn = aprs.TCP(
        os.environ.get('APRS_LOGIN', 'AUTOMATIC'),
        os.environ.get('APRS_PORT')
    )
    aprs_conn.start()

    frame = aprs.Frame()
    frame.destination = 'APYSAU'
    frame.path = ['TCPIP']
    frame.source = callsign
    frame.text = (
        "!%s\\%s7Automatic-to-APRS gateway. http://ampledata.org" %
        (aprs.dec2dm_lat(location['lat']), aprs.dec2dm_lng(location['lon']))
    )

    print frame
    aprs_result = aprs_conn.send(frame)
    print aprs_result

    return 'OK'


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    APRSApp.run(host='0.0.0.0', port=port)
