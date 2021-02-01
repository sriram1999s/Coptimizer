
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ASSIGN DIVIDE EQ FOR GE GT ID INT LE LT L_FLOWERBRACE L_PAREN MINUS MULTIPLY NE PLUS R_FLOWERBRACE R_PAREN SEMICOLON TYPE\n    detector : expression\n             | empty\n    \n    empty :\n    \n    expression : expression MULTIPLY expression\n               | expression DIVIDE expression\n               | expression PLUS expression\n               | expression MINUS expression\n    \n    expression : INT\n    '
    
_lr_action_items = {'INT':([0,5,6,7,8,],[4,4,4,4,4,]),'$end':([0,1,2,3,4,9,10,11,12,],[-3,0,-1,-2,-8,-4,-5,-6,-7,]),'MULTIPLY':([2,4,9,10,11,12,],[5,-8,5,5,5,5,]),'DIVIDE':([2,4,9,10,11,12,],[6,-8,6,6,6,6,]),'PLUS':([2,4,9,10,11,12,],[7,-8,7,7,7,7,]),'MINUS':([2,4,9,10,11,12,],[8,-8,8,8,8,8,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'detector':([0,],[1,]),'expression':([0,5,6,7,8,],[2,9,10,11,12,]),'empty':([0,],[3,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> detector","S'",1,None,None,None),
  ('detector -> expression','detector',1,'p_detector','detector.py',88),
  ('detector -> empty','detector',1,'p_detector','detector.py',89),
  ('empty -> <empty>','empty',0,'p_empty','detector.py',95),
  ('expression -> expression MULTIPLY expression','expression',3,'p_expression','detector.py',101),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression','detector.py',102),
  ('expression -> expression PLUS expression','expression',3,'p_expression','detector.py',103),
  ('expression -> expression MINUS expression','expression',3,'p_expression','detector.py',104),
  ('expression -> INT','expression',1,'p_expression_type','detector.py',110),
]
