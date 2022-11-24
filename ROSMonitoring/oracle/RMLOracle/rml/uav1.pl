:- module('spec', [trace_expression/2, match/2]).
:- use_module(monitor('deep_subdict')).
match(_event, d1) :- deep_subdict(_{'data':Val,'topic':"detect_fire_uav1"}, _event), =(Val, 0).
match(_, any).
trace_expression('Main', Main) :- Main=optional(((d1:eps)*Main)).	
