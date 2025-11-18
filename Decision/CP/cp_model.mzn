% CP/cp_model.mzn

int: n;
set of int: TEAMS = 1..n;
int: weeks = n - 1;
int: periods = n div 2;

set of int: WEEKS = 1..weeks;
set of int: PERIODS = 1..periods;

array[PERIODS, WEEKS] of var TEAMS: Home;
array[PERIODS, WEEKS] of var TEAMS: Away;

% --- Core constraints ---
constraint
  forall(p in PERIODS, w in WEEKS)(Home[p,w] != Away[p,w]);

constraint
  forall(t in TEAMS, w in WEEKS)(
    sum(p in PERIODS)(
      bool2int((Home[p,w] = t) \/ (Away[p,w] = t))
    ) = 1
  );

constraint
  forall(i,j in TEAMS where i < j)(
    sum(w in WEEKS, p in PERIODS)(
      bool2int(
        (Home[p,w] = i /\ Away[p,w] = j) \/
        (Home[p,w] = j /\ Away[p,w] = i)
      )
    ) = 1
  );

constraint
  forall(t in TEAMS, p in PERIODS)(
    sum(w in WEEKS)(
      bool2int((Home[p,w] = t) \/ (Away[p,w] = t))
    ) <= 2
  );

% --- Symmetry breaking (recommended) ---
% Fix Week 1 pairings: (1 vs n), (2 vs n-1), ...
constraint forall(p in PERIODS)(
  Home[p,1] = p /\ Away[p,1] = n - p + 1
);

% Team 1 never away vs a larger team (fix home/away orientation)
constraint
  forall(t in TEAMS where t > 1, p in PERIODS, w in WEEKS)(
    not (Home[p,w] = t /\ Away[p,w] = 1)
  );



solve satisfy;

output [
  "SOL=[",
  concat([
    "[" ++
    concat([
      "[" ++ show(Home[p,w]) ++ "," ++ show(Away[p,w]) ++ "]"
      ++ (if w < weeks then "," else "" endif)
      | w in WEEKS
    ])
    ++ "]"
    ++ (if p < periods then "," else "" endif)
    | p in PERIODS
  ]),
  "]"
];
