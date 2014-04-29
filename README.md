# CourseOwl

[![Build Status](http://ci.courseowl.com/github.com/crimsonredmk/courseowl/status.png?branch=master)](http://ci.courseowl.com/github.com/crimsonredmk/courseowl)

Home: http://courseowl.com/

Wiki: https://wiki.engr.illinois.edu/display/cs428sp14/CourseOwl

### Overview
CourseOwl is a system that will provide recommendations to people based 
on their interests and courses they have taken. The user will be asked
what interests they have and will have the option to select subjects 
already known/learned. They will then receive recommendations of 
classes they may like from MOOCs such as Coursera, Udacity, edX, and 
iversity.

### Group Members
* Michael Staszel <staszel1@illinois.edu>
* Erik Chen <chen320@illinois.edu>
* Zheng Kang <zkang3@illinois.edu>
* Daniel Garcia-Carrillo <garciac2@illinois.edu>
* Akshay Singh <asingh38@illinois.edu>
* David Eisenberg <eisenbe7@illinois.edu>

### Installation

See this: https://wiki.engr.illinois.edu/display/cs428sp14/CourseOwl+Local+Installation

### Generating Documentation with epydoc
This will generate a folder of HTML documentation based on the comment
strings in the application:

    cd courseowl_django
    export DJANGO_SETTINGS_MODULE=courseowl_django.settings
    fab generate_html_docs
