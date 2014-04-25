def unify_subject_name(subject_name):
    first_word = subject_name.split('-')[0]
    first_word = first_word.split()[0] # python runs a cool split algorithm without any parameters
    return first_word