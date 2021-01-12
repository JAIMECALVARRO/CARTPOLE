from src.CartClass import *
from src.utilis import *

# User defined simulation settings - check the effect first in GUI before you launch big data generation
csv = 'do-mpc'  # Name with which data is saved, consecutive experiments will be save with increasing index attached
number_of_experiments = 10  # How many experiments will be generated
length_of_experiment = 4000.0  # Length of each experiment in s
dt_main_simulation = dt_main_simulation_globals  # simulation timestep
track_relative_complexity = 0.5  # randomly placed target points/s
controller = 'do-mpc'  # Controller which should be used in generated experiment
# Possible options for controller:
# 'manual-stabilization', 'do-mpc', 'do-mpc-discrete', 'lqr', 'rnn_as_mpc_tf'
interpolation_type = '0-derivative-smooth'  # Sets how to interpolate between turning points of random trace
# Possible choices: '0-derivative-smooth', 'linear', 'previous'
turning_points_period = 'regular'  # How turning points should be distributed
# Possible choices: 'regular', 'random'
# Where the target position of the random experiment starts and end
start_random_target_position_at = 0.0
end_random_target_position_at = 0.0
# The list of turning points is set to None, no matter what is in globals.py

# [position, positionD, angle, angleD]
initial_state = [None, None, None, None]

save_data_online = True  # It was intended to save memory usage, but it doesn't seems to help. Leave it false.

print(controller)

# initial_positions = np.arange(-40.0, 40.0, 5.0)
# initial_positionsD = np.arange(-2.0, 2.0, 1.0)
# initial_angle = np.arange(-90.0,90.0, 30.0)/57.3
# initial_angleD = np.arange(-90.0,90.0, 30.0)/57.3

# states = list(list((position, positionD, angle, angleD)) for position in initial_positions
#                                          for positionD in initial_positionsD
#                                             for angle in initial_angle
#                                                 for angleD in initial_angleD)
#
# states = [[0.0, 0.0, 0.01, 0.1]]

for i in range(number_of_experiments):
# for i in range(len(states)):

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # You may also specify some of the variables from above here, to make them change at each iteration.#
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    print(i)
    initial_state = [0.0, 0.1, 1.0*i/57.3, 0.0]
    # initial_state = states[i]
    sleep(0.1)
    MyCart = Cart()
    gen_start = timeit.default_timer()
    Generate_Experiment(MyCart,
                        initial_state=initial_state,
                        controller=controller,
                        exp_len=length_of_experiment,
                        dt=dt_main_simulation,
                        track_relative_complexity=track_relative_complexity,
                        interpolation_type=interpolation_type,
                        turning_points_period=turning_points_period,
                        start_random_target_position_at=start_random_target_position_at,
                        end_random_target_position_at=end_random_target_position_at,
                        csv=csv,
                        save_data_online=save_data_online)

    gen_end = timeit.default_timer()
    gen_dt = (gen_end-gen_start)*1000.0
    print('time to generate data: {} ms'.format(gen_dt))