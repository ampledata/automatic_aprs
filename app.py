#!/usr/bin/env python

import os
import json

import flask


APRSApp = flask.Flask(__name__)


@APRSApp.route('/', methods=['POST'])
def slash():
    print 'slash'
    post_data = json.loads(flask.request.data)
    print post_data
    print

    if 'location' in post_data:
        pprint.pprint(post_data['location'])

    return 'OK'


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    APRSApp.debug = True
    APRSApp.run(host='0.0.0.0')
