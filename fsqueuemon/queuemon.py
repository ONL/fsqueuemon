#!/usr/bin/env python

# This file is part of fsqueuemon - https://github.com/gonicus/fsqueuemon
# Copyright (C) 2014 GONICUS GmbH, Germany - http://www.gonicus.de
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

URI = 'http://freeswitch:works@127.0.0.1:8080'
BABEL_DEFAULT_LOCALE = 'de'
BABEL_DEFAULT_TIMEZONE = 'Europe/Berlin'

from flask import Flask, request, render_template, abort, redirect, jsonify
from pprint import pformat
from urllib.parse import urlencode
from time import strftime
from datetime import datetime
import time
from backends import CallcenterStatusBackend
from flask_babel import Babel, gettext, ngettext

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
babel = Babel(app, BABEL_DEFAULT_LOCALE, BABEL_DEFAULT_TIMEZONE)

backend = CallcenterStatusBackend

@babel.localeselector
def get_locale():
    # try to guess the language from the user accept
    # header the browser transmits.  We support de/en. 
    # The best match wins.
    return request.accept_languages.best_match(['de', 'en'])

@app.template_filter('tsformat')
def filter_timestamp_format(timestamp):
    ts = datetime.fromtimestamp(int(timestamp))
    delta = datetime.now() - ts
    if delta.days < 1:
        hours = delta.seconds / 3600.
        if hours < 1:
            minutes = delta.seconds % 3600 / 60
            ts = gettext(u'vor %(num)s Min.', num=minutes)
        else:
            ts = ngettext(u'vor %(num).1f Stunde', u'vor %(num).1f Stunden', num=hours)
    return ts

@app.template_filter('deltaformat')
def filter_timedelta_format(timestamp):
    now = int(time.mktime(datetime.now().timetuple()))
    delta = now - int(timestamp)
    minutes = delta / 60
    seconds = delta % 60
    output = ""
    if minutes:
        output += ngettext(u'%(num).1f Minute', u'%(num).1f Minuten', num=minutes)
    output += ngettext(u'%(num).1f Sekunde', u'%(num).1f Sekunden', num=seconds)
    return output

@app.route('/raw')
def raw_status():
    fs = backend(URI)
    data = {'agents': fs.get_agents(), 'queues': fs.get_queues()}
    return '<pre>%s</pre>' % pformat(data, True)

@app.route('/json')
def json_status():
    fs = backend(URI)
    data = {'agents': fs.get_agents(), 'queues': fs.get_queues()}
    return jsonify(data)

@app.route('/')
def status():
    content_parameters = {}
    if request.args.get('showoffline'):
        content_parameters['showoffline'] = request.args['showoffline']
    if request.args.get('showlinks'):
        content_parameters['showlinks'] = request.args['showlinks']
    if request.args.get('showclock'):
        content_parameters['showclock'] = request.args['showclock']
    return render_template('status.html', content_view='status_content', content_parameters=content_parameters)

@app.route('/content/status')
def status_content():
    fs = backend(URI)
    agents = fs.get_agents()
    for a in agents.keys():
        if a in hide_agents:
            del agents[a]
    agent_stats = {
            'available': len([a['name'] for a in agents.itervalues() if a['status'] != 'Logged Out']),
            'free': len([a['name'] for a in agents.itervalues() if a['status'] != 'Logged Out' and a.get('callstate') is None])
            }
    queues = fs.get_queues()
    clock = strftime('%H:%M') if request.args.get('showclock') and request.args['showclock'] != 0 else None
    return render_template('status_content.html', agents=agents, agent_stats=agent_stats, queues=queues, clock=clock)

@app.route('/settings', methods=['POST'])
def settings():
    redirect_to = request.form.get('view')
    if not redirect_to:
        abort(403)
    params = {}
    if request.form.get('refresh') and request.form['refresh'].isdigit() and int(request.form['refresh']) != 0:
        params['refresh'] = request.form['refresh']
    if not request.form.get('showoffline'):
        params['showoffline'] = '0'
    if not request.form.get('showlinks'):
        params['showlinks'] = '0'
    if request.form.get('showclock'):
        params['showclock'] = '1'

    if params:
        redirect_to = '%s?%s' % (redirect_to, urlencode(params))

    return redirect(redirect_to)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
