def check_user_logged_in(request):
    is_logged_in = request.user.is_authenticated
    return {'user_logged_in': is_logged_in}