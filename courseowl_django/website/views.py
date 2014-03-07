from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'website/index.html')


@login_required
def personalize(request):
    context = {}
    return render(request, 'website/personalize.html', context)

def search(request):
    query = request.GET.get('query')
    
    # test data for iteration 2
    courses = [ {'name': 'Introduction to Programming', 
                 'prov': 'Coursera',
                 'instr': 'J. Random Teacher I',
                 'src': 'Stanford'},
                 {'name': 'Introduction to Statistics', 
                 'prov': 'Coursera',
                 'instr': 'J. Random Teacher II',
                 'src': 'MIT'},
                 {'name': 'Introduction to AI', 
                 'prov': 'Udacity',
                 'instr': 'J. Random Teacher III',
                 'src': 'UC Berkeley'},
                 {'name': 'Introduction to Bagels', 
                 'prov': 'EdX',
                 'instr': 'J. Random Teacher I',
                 'src': 'Google'},
                 {'name': 'Introduction to Google', 
                 'prov': 'EdX',
                 'instr': 'J. Random Teacher I',
                 'src': 'Microsoft'},
              ]

    context = {'query': query, 'courses': courses}
    return render(request, 'website/search.html', context)
