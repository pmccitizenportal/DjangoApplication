from django.shortcuts import redirect

from django.shortcuts import redirect

class FirstVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('has_visited', False):
            request.session['has_visited'] = True
            if not request.user.is_authenticated:
                return redirect('/login/')

        response = self.get_response(request)
        return response