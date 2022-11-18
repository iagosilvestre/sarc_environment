:- module('spec', [trace_expression/2, match/2]).
:- use_module(monitor('deep_subdict')).
match(_event, d1) :- deep_subdict(_{'data':Val,'topic':"detect_fire_uav1"}, _event), =(Val, 1).
match(_, any).
trace_expression('Main', Main) :- Main=plus((d1)).	
