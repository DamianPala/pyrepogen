#!/usr/bin/env python
# -*- coding: utf-8 -*-


from enum import EnumMeta


def get_data(name, msg):
    return input(f'{name}: [WIZARD]: {msg}: ')
    
    
def choose_one(name, msg, choices):
    if type(choices) is EnumMeta:
        choices = [item.value for item in choices]
    
    no_choice = True
    while no_choice:
        choice = input(f'{name}: [CHECKPOINT]: {msg} ({get_choices_string(choices)}): ')
        for item in choices:
            if item == choice:
                no_choice = False
                break
            
    return choice


def choose_bool(name, msg):
    return True if choose_one(name, msg, ['y', 'n']) == 'y' else False


def is_checkpoint_ok(name, msg, choices=['y', 'n'], valid_value='y'):
    choice = choose_one(name, msg, choices)
            
    return True if choice == valid_value else False


def get_choices_string(choices):
    choices_string = ''
    for choice in choices:
        choices_string += f'{choice}/'
        
    return choices_string[:-1]