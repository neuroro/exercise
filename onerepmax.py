# 
# •.° One Repetition Maximum & Equivalent Loads °.•
# _____________________________________________________________________________
#
# Calculate one repetition maximum and equivalent loads for sets of up to 12
# repetitions from the load and repetitions of the last completed heavy working
# set, using validated (Simonsen, 2025) estimates of one repetition maximum and
# the expected value of the inverses of the estimates weighted by the inverse
# of the normalised mean absolute error (Simonsen, 2025), rounded to 1.25 kg
#
# • Usage •
# -----------------------------------------------------------------------------
# In: import onerepmax
# In: onerepmax.sets( load_used, repetitions_completed )
#
# • Author •
# -----------------------------------------------------------------------------
# Rohan O. C. King (2026)
# GitHub @neuroro


# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 15:16:26 2026

@author: Rohan O. C. King (2026)
"""

import math  as m
import numpy as n


# Repetitions range
reprange = list( range( 1, 12 + 1 ) )


# Adams (1998)
def Adams_onerepmax( load, reps ):
    onerepmax = load / (1 - 0.02 * reps)
    return onerepmax
def Adams_equivalent( onerepmax, reps ):
    load = onerepmax * (1 - 0.02 * reps)
    return load
nmae_Adams = 0.098

# Lombardi (1989)
def Lombardi_onerepmax( load, reps ):
    onerepmax = load * reps**0.1
    return onerepmax
def Lombardi_equivalent( onerepmax, reps ):
    load = onerepmax / reps**0.1
    return load
nmae_Lombardi = 0.058

# Mayhew et al. (1992)
def MayhewEtAlia_onerepmax( load, reps ):
    onerepmax = load / (0.522 + 0.419 * m.exp(-0.055 * reps))
    return onerepmax
def MayhewEtAlia_equivalent( onerepmax, reps ):
    load = onerepmax * (0.522 + 0.419 * m.exp(-0.055 * reps))
    return load
nmae_MayhewEtAlia = 0.093

# O'Connor et al. (1989)
def OConnorEtAlia_onerepmax( load, reps ):
    onerepmax = load * (1 + reps / 25)
    return onerepmax
def OConnorEtAlia_equivalent( onerepmax, reps ):
    load = onerepmax / (1 + reps / 25)
    return load
nmae_OConnorEtAlia = 0.079


# # Estimators with >10% normalised mean absolute error (Simonsen, 2025)
#
# # Brzycki (1993)
# def Brzycki_onerepmax( load, reps ):
#     onerepmax = load * 36 / (37 - reps)
#     return onerepmax
# def Brzycki_equivalent( onerepmax, reps ):
#     load = onerepmax * (37 - reps) / 36
#     return load
#
# # Epley (1985)
# def Epley_onerepmax( load, reps ):
#     onerepmax = load * (1 + reps / 30)
#     return onerepmax
# def Epley_equivalent( onerepmax, reps ):
#     load = onerepmax / (1 + reps / 30)
#     return load
#
# # Landers (1985)
# def Landers_onerepmax( load, reps ):
#     onerepmax = load / (1 - 0.025 * reps)
#     return onerepmax
# def Landers_equivalent( onerepmax, reps ):
#     load = onerepmax * (1 - 0.025 * reps)
#     return load
#
# # Wathan
# def Wathan_onerepmax( load, reps ):
#     onerepmax = load / (0.488 + 0.538 * m.exp(-0.075 * reps))
#     return onerepmax
# def Wathan_equivalent( onerepmax, reps ):
#     load = onerepmax * (0.488 + 0.538 * m.exp(-0.075 * reps))
#     return load


# Estimator functions
onerepmax_estimators = [ 
    Adams_onerepmax, 
    Lombardi_onerepmax, 
    MayhewEtAlia_onerepmax, 
    OConnorEtAlia_onerepmax
    ]
equivalence_estimators = [ 
    Adams_equivalent, 
    Lombardi_equivalent, 
    MayhewEtAlia_equivalent, 
    OConnorEtAlia_equivalent
    ]
n_estimates   = len( onerepmax_estimators )
normalisation = [
    1 / nmae_Adams,
    1 / nmae_Lombardi,
    1 / nmae_MayhewEtAlia,
    1 / nmae_OConnorEtAlia
    ]
norm_total    = sum( normalisation )
normalisation = [ x / norm_total for x in normalisation ]


# Estimate one rep max
def onerepmax_estimates( load, reps ):
    estimates = [ 0 ] * n_estimates
    for e in range( n_estimates ):
        estimator    = onerepmax_estimators[e]
        estimates[e] = estimator( load, reps )
    return estimates

# Estimate equivalent loads for 1-12 reps
def sets( load, reps ):
    
    # One rep max estimates
    onerepmaxima = onerepmax_estimates( load, reps )

    # Estimates → inverse estimators → average per rep count
    E_loads = dict.fromkeys( reprange, 0 )
    for reps in reprange:
        estimates = [ 0 ] * n_estimates
        for e in range( n_estimates ):
            estimator    = equivalence_estimators[e]
            estimates[e] = estimator( onerepmaxima[e], reps )
        E_load        = sum( n.multiply( n.array( estimates ), n.array( normalisation ) ) )
        E_loads[reps] = float( round( E_load / 1.25, 0 ) * 1.25 )
    return E_loads


# _____________________________________________________________________________