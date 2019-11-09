# Hatchet Pick'em
| Python back-end for College Football sports-betting analytics

[![Build Status](https://travis-ci.org/exleym/Hatchet.svg?branch=master)](https://travis-ci.org/exleym/Hatchet)
[![Coverage Status](https://coveralls.io/repos/github/exleym/Hatchet/badge.svg?branch=master)](https://coveralls.io/github/exleym/Hatchet?branch=master)

Hatchet is a web application for centralizing college football data from 
a variety of sources, managing the "golden-source" of that data, and providing 
it in a usable form for analysis. 

> Does economically-driven bias in sports media induce unsophisticated gamblers 
> to push spreads to a detectable degree?

This project was born out of that single question and the need for a robust, 
powerful dataset to support research on the topic. To that end, we aim to 
simplify the data-cleaning and wrangling process surrounding general purpose 
college football analysis. 

### Components

The Hatchet College Football toolkit is made up of several key components 
designed to work together and in conjunction with external tools. 


| Component Name       | Framework | Description                              |
| -------------------- | --------- | ---------------------------------------- |
| [Hatchet API][H1]    | Flask     | Python web API for core data model       |
| [Hatchet Client][H2] | Python    | Python client for Hatchet Web API        |
| [Axe UI][H3]         | Angular   | Web front-end for managing app data      |
| [CFB Client][H4]     | Python    | Client for fetching [CFB Data][CFBD]     |
 
#### Hatchet API
The [Hatchet Web API][H1] provides a model of the college football landscape. 
It seeks to model as many data points about each game as possible, and make 
them available in an easy to use and reliable format. 

![Swagger](docs/static/swagger.png)

See the [Data Model][DM] section of our full documentation for a complete list 
of the entities we model and their attributes.

* Organization Entities:
  * *Subdivision* (FBS / FCS - formerly I-A, I-AA) - just for categorizing
  * *Conference* "perceived power" could affect spread @ the margin
  * *Division* sub-conference organization (don't confuse with *Subdivision*)
  * *Team* 
* Human Entities
  * *Player* associated with plays, key individuals may be worth points
  * *Coach*
* Gameplay Entities
  * *Game* - information about who played when where
  * *Drive* - drive level data with outcomes, length, ball control, etc
  * *Play* - individual plays for creating custom advanced statistics
* Gambling Entities
  * *Bookmaker* - track and interact with various bookies
  * *Line* - betting lines for each game, includes spreads, O/U & vig data
  * *Bet* (not implemented) - track bets, outcomes, and P&L
  
![Schema-Diagram](docs/static/schema-diagram.png)

#### Hatchet Client
Python client for interacting with the API. Abstrcts the HTTP / JSON 
components, but provides the data in the same schema as the Hatchet core data 
model.

```python
from hatchet.client.hatchet_client import HatchetClient

hat = HatchetClient()
bama = hat.get_team(code="BAMA")
games = hat.get_team_games(team_id=bama.id, season=2019)
```

The Hatchet Client can also be configured to bind objects instantiated by the 
client with references back to the client. This allows client objects to 
query the API for additional information, rather than acting as simple data 
containers. We recommend using this feature when interacting with the 
hatchet client directly, but the analytics client (whose purpose is to convert 
large data response objects into Pandas DataFrames for analysis) disables 
binding to ensure lightweight objects and performant queries.

```python
from hatchet.client.hatchet_client import HatchetClient

hat = HatchetClient(use_databinding=True)
clem = hat.get_team(code="CLEM")
print(clem.get_losses(season=2018))
[]
```

### Technical Architecture
 

Go Tigers!


[ESPN-API]: http://www.espn.com/apis/devcenter/overview.html#api-consumer-tiers
[REDDIT-PLAYDUMP]: https://www.reddit.com/r/CFBAnalysis/comments/6htfc6/play_by_play_data_dump_20012016/
[REDDIT-CFBANALYSIS]: https://www.reddit.com/r/CFBAnalysis/
[CFBD]: https://api.collegefootballdata.com/api/docs/?url=/api-docs.json#/
[SWAGGER]: http://localhost:5000/api/v1/


[H1]: http://localhost:5000/api/v1
[H2]: #
[h3]: http://localhost:4200/
[h4]: #
