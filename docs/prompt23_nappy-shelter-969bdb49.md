# prompt23 Replicable Simulation Outcomes nappy-shelter 969bdb49

random codename: nappy-shelter 969bdb49

#prompt 

***



write a function in helpers which generates a seed given a uuid string. 

modify this codebase so that this seed, i.e. the seed gotten (and 1:1 connected to) a uuid; this seed fixes the simulation so that the exact same thing happens every time. 

then, write a test that is hooked to pytest. run a simulation, collect about 30 sets of example data points from the simulation. re-run the simulation and assert that same outcome is reproduced. the 30 sets of data should be combinations of agent and data related to an agent. especially focus on `agent_state`, i.e. output of agent.get_state. 


