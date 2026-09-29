import rospy
import logging
from technic.srv import SetLEDEffect

logger = logging.getLogger(__name__)

set_effect_service = rospy.ServiceProxy('led/set_effect', SetLEDEffect)

def set_effect(*args, **kwargs):
    try:
        if args and not kwargs:
            effect = args[0] if len(args) > 0 else 'fill'
            r = args[1] if len(args) > 1 else 0
            g = args[2] if len(args) > 2 else 0
            b = args[3] if len(args) > 3 else 0
            set_effect_service(effect, r, g, b)
        else:
            effect = kwargs.get('effect', 'fill')
            r = kwargs.get('r', 0)
            g = kwargs.get('g', 0)
            b = kwargs.get('b', 0)
            set_effect_service(effect, r, g, b)
    except rospy.ServiceException as e:
        logger.error("Can't set led effect: %s", e)
