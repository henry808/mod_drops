import base64
import hashlib
import hmac
import simplejson
import time
import os
from mod_drops.settings import DISQUS_SECRET_KEY, DISQUS_PUBLIC_KEY
from mod_drops.settings import STATIC_URL, BASE_DIR


def get_disqus_sso(user):

    # create a JSON packet of our data attributes
    data = simplejson.dumps({
        'id': user.pk,
        'username': user.username,
        'email': user.email,
    })
    # encode the data to base64
    message = base64.b64encode(data)
    # generate a timestamp for signing the message
    timestamp = int(time.time())

    # generate our hmac signature
    sig = hmac.HMAC(DISQUS_SECRET_KEY, '%s %s' % (message, timestamp), hashlib.sha1).hexdigest()

    # generate icon and avatar
    url = "http://localhost:8000/"

    icon = os.path.join(STATIC_URL, 'mod_drops/images/favicon.png')

    avatar = os.path.join(url, user.profile.picture.url[1:])

    print avatar

    # return a script tag to insert the sso message
    return """<script type="text/javascript">
    var disqus_config = function() {
        this.page.remote_auth_s3 = "%(message)s %(sig)s %(timestamp)s";
        this.page.api_key = "%(pub_key)s";

        this.sso = {
          name:   "Mod Drops Title",
          width:   "800",
          height:  "400",
          icon:    "%(icon)s",
          avatar:   "%(avatar)s",
    };
    }
    </script>""" % dict(
        message=message,
        timestamp=timestamp,
        sig=sig,
        pub_key=DISQUS_PUBLIC_KEY,
        icon=icon,
        avatar=avatar,
    )

    # use to customize button:
    #       button:  "/test.gif",
    #       url:     "http://moddrops.com/login/",
    #       logout:  "http://moddrops.com/logout/",
