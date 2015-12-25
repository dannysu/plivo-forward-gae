"""`main` is the top level module for your Flask application."""

import env

# Import the Plivo library
import plivo, plivoxml

# Import the Flask Framework
from flask import Flask, request, make_response
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/ping')
def ping():
    return env.PING_RESPONSE


@app.route('/forward_call', methods=['GET', 'POST'])
def forward_call():
    # Generate a Dial XML to forward an incoming call.

    # The phone number of the person calling your Plivo number,
    # we'll use this as the Caller ID when we forward the call.

    from_number = request.values.get('From')

    # The number you would like to forward the call to.
    forwarding_number = env.FORWARD_TO

    params = {
        'callerId': from_number # The phone number to be used as the caller id. It can be set to the from_number or any custom number.
    }

    response = plivoxml.Response()

    d = response.addDial(**params)
    d.addNumber(forwarding_number)
    print response.to_xml()
    return response.to_xml()


@app.route('/forward_sms', methods=['GET', 'POST'])
def forward_sms():
    # Sender's phone number
    from_number = request.values.get('From')

    # Receiver's phone number - Plivo number
    to_number = request.values.get('To')

    # The text which was received
    text = request.values.get('Text')

    # Print the message
    print 'Text received: %s - From: %s' % (text, from_number)

    # Generate a Message XML with the details of the reply to be sent

    resp = plivoxml.Response()

    # The phone number to which the SMS has to be forwarded
    to_forward = env.FORWARD_TO

    body = '%s: %s' % (from_number, text)
    params = {
    'src' : to_number, # Sender's phone number
    'dst' : to_forward, # Receiver's phone number
    }

    # Message added
    resp.addMessage(body, **params)

    ret_response = make_response(resp.to_xml())
    ret_response.headers["Content-type"] = "text/xml"

    # Prints the XML
    print resp.to_xml()
    # Returns the XML
    return ret_response


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
