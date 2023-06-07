def search_with_parent(
 s0 : State,
 goals : List[State],
 succ : Callable[[State], List[State]],
 remove: Callable[[List[State]], Tuple[State, List[State]]],
 insert: Callable[[State, List[State]], List[State]],
) -> Tuple[Optional[State], Dict[State, Optional[State]]]:
 l: List[State] = [s0]
 save: Dict[State, Optional[State]] = {s0: None}
 s = s0
while l:
 s, l = remove(l)
if s in goals:
return s, save
else:
for s2 in succ(s):
if not s2 in save:
 save[s2] = s
 insert(s2, l)
return None, save

def dict2path(s, d):
 l = [s]
 parent = d[s]
while not parent is None:
 l.append(parent)
 s = parent
 parent = d[s]
 l.reverse()
return l

def insert2(s, l):
return l.append(s)
def remove2(l):
return l.pop(), l