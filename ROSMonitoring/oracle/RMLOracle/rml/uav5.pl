:- module('spec', [trace_expression/2, match/2]).
:- use_module(monitor('deep_subdict')).
match(_event, d5) :- deep_subdict(_{'data':Val,'topic':"detect_fire_uav5"}, _event), =(Val, 5).
match(_, any).
trace_expression('Main', Main) :- Main=plus((d5)).	
