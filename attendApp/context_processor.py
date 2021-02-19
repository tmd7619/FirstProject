def global_name(request):
    if request.session['user_name'] != None:
        return {
            'global_name' : request.session['user_name']
        }
    else:
        return {
            'global_name' : None
        }