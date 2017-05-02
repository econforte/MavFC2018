# API Documentation
### Updated 5/2/2017

Here is the documentation for the 'Pi Send' and 'Server Push' API's that are used
for communication between the food-computers and the Web Application.

JSON is used universally.

From this point on, FC will be used synonymously with the term food-computer.

## Pi Send

#### initPi (POST)

This is the FC initialization API that is used when a new food
computer is setup to interact with the web application. The web application
uses the name and the serial number to create a new user account for the FC. It
then sets a temporary password for the FC's account using a generated string and
the serial number. From here, it generates a token, and sets the password to the
token key for the user. It both saves this and returns this to the FC in the
response.

Sent from FC
```
{
   "name": "FoodComputer1",
   "pi_SN": "1234567890",
   "manual_control": true
}
```

Response from Web Application
```
{
    "pi": {
        "id": 36,
        "name": "FoodComputerAuthTest14",
        "pi_SN": "084478247902047",
        "manual_control": false,
        "address": null,
        "user": null
    },
    "token": "a783c3f9aebc56f44f988dad7beae4da658dd94b"
}
```

#### initDevices (POST)

This is the device initialization API that is used by an FC to initialize
each of its devices.

```
[
   {
       "pi": 1,
       "device_type": "Temperature Sensor",
       "device_ID": 123,
       "residual_threshold": 3.14
   }
]
```

#### deviceData (POST)

This is the device data API that is used by an FC to send up the data from each of
its devices (sensors).

```
[
   {
       "device": 1,
       "data_value": 13,
       "timestamp": "2017-02-07T15:00:00Z",
       "is_anomaly": true
   }
]
```

#### getDeviceTypes (GET)

This API returns all of the device types available to the FC.

#### anomalyEmail (POST)

This is the API that is used by the FC to send an email when an anomaly is detected.
The FC can specify the message and send the email to each of three levels of users:

Level 1: All admins and anyone associated to the FC
Level 2: All admins an the FC user
Level 3: All admins

```
{
   "pi": 1,
   "level": 1,
   "message": "It was Sean and his team of dolphins."
}
```

## Server Push

#### ServerPushAPI (POST)
This is the long-polling mechanism that is implemented due to the non-static
nature of the IP addresses of the FCs. The FCs continually poll this API for
updates to the manual controls as well as the experiments.

With each request, the FC identifies itself as well as tells the server whether
or not it thinks it is being manually controlled. It also gives the time last
updated and active instance so that the server knows which commands have already
been sent, and thus if there are commands in the queue to be sent and executed.

The server responds with arrays of started, active, and ended instances of experiments
so that the FC can execute the necessary actions to meet the requirements of the
various experiments based on the input of the users. The response also contains
an updated manual-control field as well as updates for each of the controllers on the
interface, to be implemented when the FC is in manual control mode. 

Sent to Server
```
{
	"pi":{  // required
		"pk":1,
		"pi_SN":"049581740987343573",
		"manual_control":false
	}
	"lastControllerUpdateTime":"2017-3-24T05:00:10Z"
	"activeInstance":4   // tells server to update the active instance from the pi.
}
```

Returned from Server
```
{
    "endInstance": [ //tells pi to end this instance only added if execution required
        {
            "id": 3,
            "start": "2017-03-22T05:00:00Z",
            "end": "2017-03-24T05:00:00Z",
            "active": true,
            "experiment": {
                "id": 1,
                "name": "Basil",
                "pi": 1,
                "collection_interval": 5,
                "experiment_rules": [
                    {
                        "id": 3,
                        "device": 6,
                        "hour": 10,
                        "minute": 15,
                        "baseline_target": 1.0,
                        "days": [
                            {
                                "id": 1,
                                "name": "Monday"
                            },
                            {
                                "id": 2,
                                "name": "Tuesday"
                            },
                            {
                                "id": 3,
                                "name": "Wednesday"
                            },
                            {
                                "id": 4,
                                "name": "Thursday"
                            },
                            {
                                "id": 5,
                                "name": "Friday"
                            }
                        ],
                        "get_threshold": 2.0
                    },
                    {
                        "id": 4,
                        "device": 5,
                        "hour": 18,
                        "minute": 45,
                        "baseline_target": 65.0,
                        "days": [
                            {
                                "id": 1,
                                "name": "Monday"
                            },
                            {
                                "id": 2,
                                "name": "Tuesday"
                            },
                            {
                                "id": 3,
                                "name": "Wednesday"
                            },
                            {
                                "id": 4,
                                "name": "Thursday"
                            },
                            {
                                "id": 5,
                                "name": "Friday"
                            },
                            {
                                "id": 6,
                                "name": "Saturday"
                            },
                            {
                                "id": 7,
                                "name": "Sunday"
                            }
                        ],
                        "get_threshold": 2.1
                    }
                ]
            }
        }
    ],
    "activeInstance": [  //tells pi that this is what is currently set as the current instance always sent, to update rule info.
        {
            "id": 3,
            "start": "2017-03-22T05:00:00Z",
            "end": "2017-03-24T05:00:00Z",
            "active": true,
            "experiment": {
                "id": 1,
                "name": "Basil",
                "pi": 1,
                "collection_interval": 5,
                "experiment_rules": [
                    {
                        "id": 3,
                        "device": 6,
                        "hour": 10,
                        "minute": 15,
                        "baseline_target": 1.0,
                        "days": [
                            {
                                "id": 1,
                                "name": "Monday"
                            },
                            {
                                "id": 2,
                                "name": "Tuesday"
                            },
                            {
                                "id": 3,
                                "name": "Wednesday"
                            },
                            {
                                "id": 4,
                                "name": "Thursday"
                            },
                            {
                                "id": 5,
                                "name": "Friday"
                            }
                        ],
                        "get_threshold": 2.0
                    },
                    {
                        "id": 4,
                        "device": 5,
                        "hour": 18,
                        "minute": 45,
                        "baseline_target": 65.0,
                        "days": [
                            {
                                "id": 1,
                                "name": "Monday"
                            },
                            {
                                "id": 2,
                                "name": "Tuesday"
                            },
                            {
                                "id": 3,
                                "name": "Wednesday"
                            },
                            {
                                "id": 4,
                                "name": "Thursday"
                            },
                            {
                                "id": 5,
                                "name": "Friday"
                            },
                            {
                                "id": 6,
                                "name": "Saturday"
                            },
                            {
                                "id": 7,
                                "name": "Sunday"
                            }
                        ],
                        "get_threshold": 2.1
                    }
                ]
            }
        }
    ],
    "startInstance": [  //tells pi to start this instance only added if execution required
        {
            "id": 4,
            "start": "2017-03-27T13:00:00Z",
            "end": "2017-10-03T13:00:00Z",
            "active": false,
            "experiment": {
                "id": 1,
                "name": "Basil",
                "pi": 1,
                "collection_interval": 5,
                "experiment_rules": [
                    {
                        "id": 3,
                        "device": 6,
                        "hour": 10,
                        "minute": 15,
                        "baseline_target": 1.0,
                        "days": [
                            {
                                "id": 1,
                                "name": "Monday"
                            },
                            {
                                "id": 2,
                                "name": "Tuesday"
                            },
                            {
                                "id": 3,
                                "name": "Wednesday"
                            },
                            {
                                "id": 4,
                                "name": "Thursday"
                            },
                            {
                                "id": 5,
                                "name": "Friday"
                            }
                        ],
                        "get_threshold": 2.0
                    },
                    {
                        "id": 4,
                        "device": 5,
                        "hour": 18,
                        "minute": 45,
                        "baseline_target": 65.0,
                        "days": [
                            {
                                "id": 1,
                                "name": "Monday"
                            },
                            {
                                "id": 2,
                                "name": "Tuesday"
                            },
                            {
                                "id": 3,
                                "name": "Wednesday"
                            },
                            {
                                "id": 4,
                                "name": "Thursday"
                            },
                            {
                                "id": 5,
                                "name": "Friday"
                            },
                            {
                                "id": 6,
                                "name": "Saturday"
                            },
                            {
                                "id": 7,
                                "name": "Sunday"
                            }
                        ],
                        "get_threshold": 2.1
                    }
                ]
            }
        }
    ],
    "pi": { // always sent to confirm recipient and update pi manual_control
        "name": "MAVCF",
        "pi_SN": "049581740987343573",
        "manual_control": true
    },
    "controllerUpdates": [  // contains controller updates, only sent if manuall control = true
        {
            "id": 2,
            "turn_on": true,
            "timestamp": "2017-04-03T17:50:46Z",
            "executed": false,
            "device": 26
        }
    ]
}
```
