# prompt26 fix issue with int times fuzzy-let 4ffac1de

random codename: fuzzy-let 4ffac1de

#prompt 

***

rn if I run: 


```python
cfg = {
    "git_commit": "c440da9b1f1dee0556f93d8843a873e5dabc0002",
    "SimulationManager": {
        "__init__": {
            "n_agents": 30,
            "lift_capacity": 2,
            "start_datetime": None,
            "logger": None
        },
        "run": {
            "end_datetime": None,
            "runtime_minutes": None
        }
    },
    "Simulation": {
        "__init__": {
            "simulation_uuid": None
        },
        "run": {
            "stop_time": None,
            "logger": None,
            "full_agent_logging": False,
            "start_datetime": "2025-03-12T09:00:00",
            "random_seed": None
        }
    },
    "Lift": {
        "num_chairs": 15,
        "ride_mean": 7,
        "ride_sd": 1,
        "traverse_mean": 5,
        "traverse_sd": 1.5
    },
    "Agent": {
        "__init__": {
            "logger": None,
            "self_logging": True
        }
    }
}
cfg['Simulation']['run']['random_seed'] = '46344237-3141-4d05-9b8f-4854a7b47c2f'

manager = SimulationManager(cfg)
result = manager.run(runtime_minutes=60*5)
```



... and then 

```python
# get rideloop explogs and agent event log
exp_log_data = manager.retrieve_data()
exp = exp_log_data['exp_rideloop']
log = exp_log_data['agent_log']
```

I get 

```
time                                 datetime64[ns]
exp_id                                       object
return_event_uuid                            object
agent_uuid                                   object
agent_uuid_codename                          object
time_spent_ride_lift                         object
time_spent_traverse_down_mountain            object
time_spent_in_queue                          object
time_spent_total                             object
dtype: object
```

also I get `exp.iloc[227]['time_spent_in_queue']` -> 2. 

this is a problem because agent time in queue is still being tracked in terms of ints. 

in the simulation, all times should be calculated by manipulating datetime objects. there is no need for any other kind of time reference and this cases confusion. 

## update the code 

review the code and make sure that time_spent_ride_lift, time_spent_traverse_down_mountain, time_spent_in_queue, time_spent_total are all tracked via calculation of timestamp differences elsewhere. 

## document 

next, write a document "docs/tutorial-fuzzy-let.md". use this md template: 

```markdown
## time_spent_ride_lift

## time_spent_traverse_down_mountain

## time_spent_in_queue

## time_spent_total

```

for each of those h2, describe how this is being calculated and include code snippets of the zero_liftsim code and files which show how these are calculated i.e. where are the "time markers". 
