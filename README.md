# Reserves

Check market availability for doctrine fits

## Setup

1. Clone this repository
    ```
    git clone https://github.com/mobiusxs/reserves.git
    ```
1. Create an application at https://developers.eveonline.com/ and grant the following scopes
    ```
    esi-markets.structure_markets.v1
    ```
1. cd in the `reserves/` directory and create a file called `.env` with the following contents
    ```
    CLIENT_ID = <your client id>
    CALLBACK_URL = <your callback url>
    SCOPE = <your scope>
    ```
1. Setup up the database by running the following scripts
    ```
    python3 data/tables.py
    python3 data/static.py
    python3 data/orders.py
    ```
