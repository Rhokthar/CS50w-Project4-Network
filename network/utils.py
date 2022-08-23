from .models import *

# UTILITY FUNCTIONS
def IsFollower(request, user):
    # user = Visited Profile
    # request.user = Visitor
    followStatus = False
    followersList = user.followers_list.all()

    if request.user in followersList:
        followStatus = True

    return followStatus
