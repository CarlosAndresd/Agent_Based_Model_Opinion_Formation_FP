"""

==============================================================
Command Line Interface, (:mod:`f_abm.src.command_line_interface`)
==============================================================

Description
-----------

    This module contains all the functions to use the program from the command line

Functions
---------

    - create_new_simulations


"""


from ast import literal_eval
from .model_functions import model_evolution
from .auxiliary_functions import modify_opinions_method_1, modify_opinions_method_2, create_random_numbers
import numpy as np
from .digraph_creation import complete_digraph, ring_digraph, small_world_digraph, random_digraph


def read_positive_integer(message, default_input):
	"""

	This function is used to read a positive integer, it is used to ask for the number of agents and the number of time
	steps of the simulation

	Parameters
	----------
	message: message to be displayed to the user
	default_input: default input (in text form)

	Returns
	-------
	the positive integer provided by the user

	Reference
	---------

	This function was modified from the answer in
	https://stackoverflow.com/questions/26198131/check-if-input-is-positive-integer

	"""

	while True:
		number = input(message + ' [' + default_input + ']: ')
		while not number:
			number = default_input
		try:
			val = int(number)
			if val < 0:  # if not a positive int print message and ask for input again
				print("Sorry, input must be a positive integer, try again")
				continue
			break
		except ValueError:
			print("This is not an integer number, try again")

	return number


def get_parameter_value(all_parameters, parameter_name):
	"""

	This function receives two strings, the string 'all_parameters' contains parameters and parameter values separated
	by a semicolon, the string 'parameter_name' contains the name of the parameter. The function returns the evaluation
	of the variable related to the first appearance of the parameter name. See the examples.

	Parameters
	----------
	all_parameters: string containing all the parameter names and parameter values, separated by semicolons
	parameter_name: string containing the name of the parameter

	Returns
	-------
	The first value of the parameter if it is contained in the string 'all_parameters', if it is not contained, then it
	returns None

	Examples
	--------

	all_parameters = 'par_rep=(0.2, 0.3, 0.5); par_tol=0.2; print=True'
	parameter_name = 'par_rep'

	returns (0.2, 0.3, 0.5)

	all_parameters = 'par_rep=(0.2, 0.3, 0.5); par_tol=0.2; print=True'
	parameter_name = 'model_name'

	returns None because 'model_name' is not in all_parameters

	all_parameters = 'par_rep=(0.2, 0.3, 0.5); par_tol=0.2; par_tol=0.5; print=True'
	parameter_name = 'par_tol'

	returns 0.5, because in its first appearance the value 0.2 was given instead of the value 0.5


	"""

	print('\n'*2)

	print('all_parameters = ' + all_parameters)
	print('parameter_name = ' + parameter_name)

	print('\n')

	first_index = all_parameters.find(parameter_name)
	if first_index == -1:
		print('return None')
		print('\n' * 2)
		return None
	first_part = all_parameters[first_index:]
	last_index = first_part.find(';')
	if last_index == -1:
		parameter_value = first_part[first_part.find('=')+1:]
	else:
		parameter_value = first_part[first_part.find('=') + 1:first_part.find(';')]

	print('return ' + parameter_value)
	print('\n' * 2)
	return literal_eval(parameter_value)


def create_new_simulations():
	simulation_parameters = read_user_input()

	# Now that all the information is gathered, we can proceed to execute the simulation

	num_agents = simulation_parameters['num_ag']

	# 1. Create the initial opinions
	abs_mean_op, mean_op = simulation_parameters['io_loc']
	io_tolerance = simulation_parameters['io_tol']
	io_method = simulation_parameters['io_met']
	io_initial_distribution = simulation_parameters['io_dis']
	io_print = simulation_parameters['io_prt']

	initial_opinions = create_random_numbers(num_agents=num_agents, number_parameters=io_initial_distribution)

	if io_method is None:

		rng = np.random.default_rng()  # this is for the random numbers creation

		if rng.random(1)[0] > 0.5:
			initial_opinions = modify_opinions_method_1(initial_opinions, des_mean=mean_op,
											des_abs_mean=abs_mean_op, epsilon=io_tolerance)

		else:
			initial_opinions = modify_opinions_method_2(initial_opinions, des_mean=mean_op,
											des_abs_mean=abs_mean_op, epsilon=io_tolerance)

	else:

		if io_method == 1:
			initial_opinions = modify_opinions_method_1(initial_opinions, des_mean=mean_op,
														des_abs_mean=abs_mean_op, epsilon=io_tolerance)

		else:
			if not io_method == 2:
				print("The method should be a number between 1 and 2")
			initial_opinions = modify_opinions_method_2(initial_opinions, des_mean=mean_op,
														des_abs_mean=abs_mean_op, epsilon=io_tolerance)

	# 2. Create the adjacency matrix
	dig_lab = simulation_parameters['dig_lab']
	dig_par = simulation_parameters['dig_par']
	dig_prt = simulation_parameters['dig_prt']

	if dig_lab == 'cd':  # Complete digraph
		complete_digraph(num_agents=num_agents, row_stochastic=False, positive_edge_ratio=1.0)

	elif dig_lab == 'gr':  # Generalised ring
		ring_digraph(num_agents=num_agents, topology_signature=None, row_stochastic=False, positive_edge_ratio=1.0,
					 num_random_edges_it=0)

	elif dig_lab == 'sw':  # Small-world
		small_world_digraph(num_agents=num_agents, topology_signature=None, row_stochastic=False, positive_edge_ratio=1.0,
							change_probability=0.0, reverse_probability=0.0, bidirectional_probability=0.0,
							num_random_edges_it=0)

	elif dig_lab == 'rd':  # Random digraph
		random_digraph(num_agents=num_agents, row_stochastic=False, positive_edge_ratio=1.0, edge_probability=0.5)

	else:
		print("The selected digraph topology does not exits")

	# model_evolution(initial_opinions=None, adjacency_matrix=None, agent_parameters=None, model_parameters=None,
	# 				model_function=None, num_steps=50, default_type=0)


def read_user_input():
	"""

	This function reads all the necessary input from the user to create a new simulation and returns a dictionary with
	all the information for the simulation(s) to happen

	Returns
	-------
	A dictionary with information on how to run the desired simulation. The dictionary contains the following
	information:

	"""

	welcome_text = 'Creation of a new simulation'
	print('\n'*10)
	print('|' + '*' * (2+len(welcome_text)) + '|')
	print('| ' + welcome_text + ' |')
	print('|' + '*' * (2 + len(welcome_text)) + '|')
	print(' ')

	simulation_data = dict()

	# File name
	default_input = 'date'
	file_name = input('Enter name of the new simulation [' + default_input + ']: ')
	while not file_name:
		file_name = default_input

	simulation_data['file_name'] = file_name

	# Number of agents
	# Options:
	# - number of agents (num_ag)
	default_input = '100'
	message = 'Enter number of agents'
	simulation_data['num_ag'] = read_positive_integer(message, default_input)

	# Initial opinion characterisation
	# Options:
	# - location (io_loc)
	# - tolerance (io_tol) [optional]
	# - method (io_met) [optional]
	# - initial_distribution (io_dis) [optional]
	# - print histogram (io_prt) [optional]

	default_input = 'io_loc=(0.5, 0.1); io_dis=[[0, -1.0, 1.0, 1]]; io_prt=True'
	initial_opinion_char = input('Enter initial opinion characterisation [' + default_input + ']: ')
	while not initial_opinion_char:
		initial_opinion_char = default_input

	simulation_data['io_loc'] = get_parameter_value(initial_opinion_char, 'io_loc')
	simulation_data['io_tol'] = get_parameter_value(initial_opinion_char, 'io_tol')
	simulation_data['io_met'] = get_parameter_value(initial_opinion_char, 'io_met')
	simulation_data['io_dis'] = get_parameter_value(initial_opinion_char, 'io_dis')
	simulation_data['io_prt'] = get_parameter_value(initial_opinion_char, 'io_prt')

	# Model
	# Options:
	# - model label (mod_lab)
	# - model parameters (mod_par) [optional]
	default_input = 'mod_lab="CB"'
	model_id = input('Enter model [' + default_input + ']: ')
	while not model_id:
		model_id = default_input

	simulation_data['mod_lab'] = get_parameter_value(model_id, 'mod_lab')
	simulation_data['mod_par'] = get_parameter_value(model_id, 'mod_par')

	# Agent parameter characterisation
	# Options:
	# - parameter representation (par_rep)
	# - tolerance (par_tol) [optional]
	# - method (par_met) [optional]
	# - print histogram or alternative representation (par_prt) [optional]
	default_input = 'par_rep=(0.2, 0.3, 0.5); par_prt=True'
	agent_parameter_char = input('Enter agent parameter characterisation [' + default_input + ']: ')
	while not agent_parameter_char:
		agent_parameter_char = default_input

	simulation_data['par_rep'] = get_parameter_value(agent_parameter_char, 'par_rep')
	simulation_data['par_tol'] = get_parameter_value(agent_parameter_char, 'par_tol')
	simulation_data['par_met'] = get_parameter_value(agent_parameter_char, 'par_met')
	simulation_data['par_prt'] = get_parameter_value(agent_parameter_char, 'par_prt')

	# Underlying digraph characterisation
	# Options:
	# - digraph label (dig_lab)
	# - digraph parameters (depending on the type) (dig_par) [optional]
	# - print digraph representation (dig_prt) [optional]
	default_input = 'dig_lab="sw"; dig_par="sig=(0, 1, 1, 1), alp=0.5"; print=True'
	underlying_digraph_char = input('Enter underlying digraph characterisation [' + default_input + '] ')
	while not underlying_digraph_char:
		underlying_digraph_char = default_input

	simulation_data['dig_lab'] = get_parameter_value(underlying_digraph_char, 'dig_lab')
	simulation_data['dig_par'] = get_parameter_value(underlying_digraph_char, 'dig_par')
	simulation_data['dig_prt'] = get_parameter_value(underlying_digraph_char, 'dig_prt')

	# Number of steps
	# Options:
	# - number of time steps (num_ts)
	default_input = '50'
	message = 'Enter number of time-step'
	simulation_data['num_ts'] = read_positive_integer(message, default_input)

	print('\n'*5)
	print(simulation_data)

	return simulation_data


if __name__ == '__main__':
	create_new_simulations()
