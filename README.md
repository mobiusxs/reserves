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
1. Copy token from `jwt.json` on local machine tp `jwt.json` on server.
1. Add `reserves/` to path
    ```
    export PATH=$PATH:$(pwd)
    ```
1. Install dependencies
    ```
    python3 -m pip install -r requirements.txt
    ```
1. Setup up the database by running the following scripts
    ```
    python3 -m data.tables
    python3 -m data.static
    python3 -m data.orders
    python3 -m data.doctrines
    ```
1. Set crontab to fetch orders
    ```
    crontab -e
    * * * * * cd <path/to/reserves/> && python3 -m data.orders
    ```
1. Start the server
    ```
    python3 -m gunicorn --bind 0.0.0.0 "core.app:create_app()"
    ```
