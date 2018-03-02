from . import algorithms
from .base import BaseWorkoutDataFrame
from .helpers import requires
from vmpy.metrics import normalized_power, power_duration_curve
from vmpy.streams import compute_zones, wpk


class WorkoutDataFrame(BaseWorkoutDataFrame):
    _metadata = ['athlete']

    @requires(columns=['power'])
    def compute_power_zones(self, **kwargs):
        if kwargs.get('ftp', None):
            return compute_zones(self.power, ftp=kwargs.get('ftp'))
        elif kwargs.get('zones', None):
            return compute_zones(self.power, zones=kwargs.get('zones'))
        else:
            return compute_zones(self.power, ftp=self.athlete.ftp)

    @requires(columns=['power'])
    def compute_mean_max_power(self):
        return power_duration_curve(self.power)
        # return algorithms.mean_max_power(self.power)

    @requires(columns=['power'])
    def compute_weighted_average_power(self):
        return normalized_power(self.power, type='NP')
        # return algorithms.weighted_average_power(self.power)

    @requires(columns=['power'], athlete=['weight'])
    def compute_power_per_kg(self):
        return wpk(self.power, self.athlete.weight)
        # return algorithms.power_per_kg(self.power, self.athlete.weight)

    @requires(columns=['power'], athlete=['cp', 'w_prime'])
    def compute_w_prime_balance(self, algorithm=None, *args, **kwargs):
        return algorithms.w_prime_balance(self.power, self.athlete.cp,
            self.athlete.w_prime, algorithm, *args, **kwargs)

    @requires(columns=['power'])
    def compute_mean_max_bests(self, duration, amount):
        return algorithms.mean_max_bests(self.power, duration, amount)

    @requires(columns=['power', 'heartrate'])
    def compute_heartrate_model(self):
        return algorithms.heartrate_model(self.heartrate, self.power)


class Athlete:
    def __init__(self, name=None, sex=None, weight=None, dob=None, ftp=None,
            cp=None, w_prime=None):
        self.name = name
        self.sex = sex
        self.weight = weight
        self.dob = dob
        self.ftp = ftp
        self.cp = cp
        self.w_prime = w_prime
