:- module('spec', [trace_expression/2, match/2]).
:- use_module(monitor('deep_subdict')).
match(_event, d1) :- deep_subdict(_{'data':Val,'topic':"detect_fire_uav1"}, _event), =(Val, 1).
match(_event, d2) :- deep_subdict(_{'data':Val,'topic':"detect_fire_uav2"}, _event), =(Val, 2).
match(_event, d3) :- deep_subdict(_{'data':Val,'topic':"detect_fire_uav3"}, _event), =(Val, 3).
match(_event, d4) :- deep_subdict(_{'data':Val,'topic':"detect_fire_uav4"}, _event), =(Val, 4).
match(_event, d5) :- deep_subdict(_{'data':Val,'topic':"detect_fire_uav5"}, _event), =(Val, 5).
match(_event, d6) :- deep_subdict(_{'data':Val,'topic':"detect_fire_uav6"}, _event), =(Val, 6).
match(_, any).
trace_expression('Main', Main) :- Main=plus((d1 \/ d2 \/ d3 \/ d4 \/ d5 \/ d6)).	
