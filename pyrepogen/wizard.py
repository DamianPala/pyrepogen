'''
Created on 20.12.2018

@author: Haz
'''


def get_data(name, msg):
    return input("{}: [WIZARD]: {}: ".format(name, msg))
    
    
def choose_one(name, msg, choices):
    no_choice = True
    while no_choice:
        choice = input("{}: [CHECKPOINT]: {} ({}): ".format(name, msg, get_choices_string(choices)))
        for item in choices:
            if item == choice:
                no_choice = False
                break
            
    return choice


def is_checkpoint_ok(name, msg, choices, valid_value):
    choice = choose_one(name, msg, choices)
            
    return True if choice == valid_value else False


def get_choices_string(choices):
    choices_string = ""
    for choice in choices:
        choices_string += "{}/".format(choice)
        
    return choices_string[:-1]