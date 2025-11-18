int: n;
set of int: TEAMS = 1..n;
int: weeks = n-1;
int: periods = n div 2;
set of int: WEEKS = 1..weeks;
set of int: PERIODS = 1..periods;
array[PERIODS, WEEKS] of var TEAMS: Home;
array[PERIODS, WEEKS] of var TEAMS: Away;
array[TEAMS] of var int: HomeCount = 
    [ sum(p in PERIODS, w in WEEKS)( bool2int(Home[p,w] = t) ) | t in TEAMS ];
array[TEAMS] of var int: AwayCount = 
    [ sum(p in PERIODS, w in WEEKS)( bool2int(Away[p,w] = t) ) | t in TEAMS ];

var int: total_imbalance = sum(t in TEAMS)( abs(HomeCount[t] - AwayCount[t]) );


constraint
  forall(p in PERIODS, w in WEEKS)(Home[p,w] != Away[p,w]);


constraint
  forall(t in TEAMS, w in WEEKS)(
    sum(p in PERIODS)(
      bool2int(
        (Home[p,w] = t) \/ (Away[p,w] = t)
      )
    ) = 1
  );


constraint
  forall(i,j in TEAMS where i<j)(
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
      bool2int(
        (Home[p,w] = t \/ Away[p,w] = t) 
      )
    ) <= 2
  );


constraint
  forall(p in 1..(periods-1)) (Home[p, 1] < Home[p+1, 1]);
  
  

solve minimize total_imbalance;
