# Tutorial - Validate that Simulation is Reproducible good-subject 76ac56de

random codename: good-subject 76ac56de

***




```python
def sim_reprod(random_seed='d7a0baf7-61aa-484d-a48e-e7f9b3fb4a6d'):

    # Run Simulation

    x = """
    {
        "git_commit": "d5591c363075a9fa932ba8be140caa96690c7f0d",
        "SimulationManager": {
            "__init__": {
                "n_agents": 3,
                "lift_capacity": 2,
                "start_datetime": null,
                "logger": null
            },
            "run": {
                "end_datetime": null,
                "runtime_minutes": null
            }
        },
        "Simulation": {
            "__init__": {
                "simulation_uuid": null
            },
            "run": {
                "stop_time": null,
                "logger": null,
                "full_agent_logging": false,
                "start_datetime": "2025-03-12T09:00:00",
                "random_seed": null
            }
        },
        "Lift": {
            "num_chairs": 50,
            "ride_mean": 7,
            "ride_sd": 1,
            "traverse_mean": 5,
            "traverse_sd": 1.5
        },
        "Agent": {
            "__init__": {
                "logger": null,
                "self_logging": true
            }
        }
    }
    """
    cfg = json.loads(x)

    cfg['Simulation']['run']['random_seed'] = random_seed


    # this runs the same seed twice (or should at least)
    manager1 = SimulationManager(copy(cfg))
    result1 = manager1.run(runtime_minutes=60)
    print(result1)
    print(result1['average_wait'])

    manager2 = SimulationManager(copy(cfg))
    result2 = manager2.run(runtime_minutes=60)
    print(result2)
    print(result2['average_wait'])

    items = {'result1':result1['average_wait'],
             'result2':result2['average_wait'], 'manager1':manager1,
             'manager2':manager2, 'config':cfg}

    return items
```


