# SAT/sat_model.py

from z3 import *


def build_vars(n):
    assert n % 2 == 0 and n >= 2, "n must be an even integer ≥ 2"

    W = n - 1  # weeks
    P = n // 2  # periods per week

    M = [
        [
            [
                [Bool(f"M_i{i}_j{j}_p{p}_w{w}")
                 for w in range(W)]
                for p in range(P)]
            for j in range(n)]
        for i in range(n)]

    return M, W, P


def one_match_per_slot(s, M, p, w, n):
    match_candidates = [M[i][j][p][w] for i in range(n) for j in range(n) if i != j]
    s.add(PbEq([(g, 1) for g in match_candidates], 1))


def team_plays_once_per_week(s, M, n, W, P):
    for t in range(n):
        for w in range(W):
            inv = []
            for j in range(n):
                if j != t:
                    for p in range(P):
                        inv.append(M[t][j][p][w])
            for i in range(n):
                if i != t:
                    for p in range(P):
                        inv.append(M[i][t][p][w])
            s.add(PbEq([(x, 1) for x in inv], 1))


def each_pair_plays_once(s, M, n, W, P):
    for i in range(n):
        for j in range(i + 1, n):
            games = []
            for w in range(W):
                for p in range(P):
                    games.append(M[i][j][p][w])
                    games.append(M[j][i][p][w])
            s.add(PbEq([(g, 1) for g in games], 1))


def limit_period_usage(s, M, n, W, P):
    for t in range(n):
        for p in range(P):
            apps = []
            for j in range(n):
                if j != t:
                    for w in range(W):
                        apps.append(M[t][j][p][w])
            for i in range(n):
                if i != t:
                    for w in range(W):
                        apps.append(M[i][t][p][w])
            s.add(AtMost(*apps, 2))
