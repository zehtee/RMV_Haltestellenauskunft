#!/usr/bin/python3

import asyncio
import aiohttp
from RMVtransport import RMVtransport
import sys, os, time, tqdm, datetime

# RMV Haltestellen Documentation
# https://opendata.rmv.de/site/files/rmv01/RMV_Haltestellen_Tarifperiode_2022_23_Stand_2023-04-19.zip

# where to write the logfile?
dir=os.path.dirname(__file__)
logfile=str(dir) + "/rmv.log"

# how many results to collect
results = 4
# how many seconds to wait between two api requests
refresh = 60

# The main part of the example script
async def main(id, results):
    async with aiohttp.ClientSession():
        rmv = RMVtransport()

        # Get the data
        try:
            data = await rmv.get_departures(station_id=id, products=["Tram"], max_journeys=results)
            #print(data)
            # or pretty print
            rmv.print()
            print("######################################")
                
        except TypeError:
            pass

# writing logfile
def logger(message):
    with open(logfile,'a') as lf:
        lf.write(str(datetime.datetime.now()) + "   :   " + message + "\n")
    print(message)
        

#####################################################
loop = asyncio.get_event_loop()

os.system('cls' if os.name=='nt' else 'clear')
logger("Session started")

while True:
    for id in ["3001607"]:
    #for id in ["3001607","3002698"]:
    # 3001607 = Flaschenburgstrasse
    # 3002698 = Offenbach Stadtgrenze
        try:
            # Collecting data
            loop.run_until_complete(main(id, results))
            logger("Collected data, refreshing every " + str(refresh) + " seconds, got " + str(results) + " results for station id " + str(id))
            # wait
            time.sleep(refresh)
            # clear screen
            os.system('cls' if os.name=='nt' else 'clear')
        except KeyboardInterrupt:
            # CTRL+C
            logger("Session aborted by user (exit 0)")
            sys.exit(0)
        except:
            # in case of error: waiting and trying again to collect data
            print("Error: Trying again in " + str(5*refresh) + " seconds")
            logger("ERROR: An error occured; waiting....")
            # progress bar over waiting time
            for i in tqdm.tqdm(range(5*refresh)):
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    # CTRL+C aborts program
                    logger("ERROR: Session aborted by user (exit 1)")
                    sys.exit(1)
                except:
                    logger("ERROR: Session aborted (exit 2)")
                    sys.exit(2)
            # clear screen
            os.system('cls' if os.name=='nt' else 'clear')