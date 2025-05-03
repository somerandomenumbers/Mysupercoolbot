# SPDX-License-Identifier: BSD-3-Clause

import numpy as np

from supremacy import helpers

# This is your team name
CREATOR = "SimpleAI"


def tank_ai(tank, info, game_map):
    """
    Function to control tanks.
    """
    if not tank.stopped:
        if tank.stuck:
            tank.set_heading(tank.heading - 60)
        elif "target" in info:
            tank.goto(*info["target"])


def ship_ai(ship, info, game_map):
    """
    Function to control ships.
    """
    if not ship.stopped:
        if ship.stuck:
            distances = [ship.get_distance(base.x, base.y) for base in info['bases']]
            if all(d > 45 for d in distances):
#            if ship.get_distance(ship.owner.x, ship.owner.y) > 40:
                if len(info['bases']) < 10:
                    ship.convert_to_base()
                else:
                    ship.stop()

            else:
                ship.set_heading(np.random.random() * 360.0)
                if all(d > 45 for d in distances):
                    if len(info['bases']) < 10:
                        ship.convert_to_base()


def jet_ai(jet, info, game_map):

    if jet.get_distance(jet.owner.x, jet.owner.y) > 80:
        jet.set_heading(jet.heading + 45)
        


    """
    Function to control jets.
    """
  #  if "target" in info:
   #     jet.goto(*info["target"])



class PlayerAi:
    """
    This is the AI bot that will be instantiated for the competition.
    """

    def __init__(self, ):
        self.team = CREATOR  # Mandatory attribute       
        self.build_queue = helpers.BuildQueue(
            ["mine","mine","mine", "jet"], cycle=False)
        self.seen = 0
        self.first = True


    def run(self, t: float, dt: float, info: dict, game_map: np.ndarray):
        """
        This is the main function that will be called by the game engine.
        """

        # Get information about my team
        myinfo = info[self.team]

        if len(info) > 1:
            for name in info:
                if name != self.team:
                    if 'bases' in info[name]:
                        self.seen += len(info[name]['bases'])
                    if 'tanks' in info[name]:
                        self.seen += len(info[name]['tanks'])
                    if 'ships' in info[name]:
                        self.seen += len(info[name]['ships'])
                    if 'jets' in info[name]:
                        self.seen += len(info[name]['jets'])


        if self.seen > 1 and self.first:
            self.build_queue = helpers.BuildQueue(
                ["ship", "ship", "mine", "jet"], cycle=True)
            self.first = False


        # Iterate through all my bases and process build queue
        for base in myinfo["bases"]:
            # Calling the build_queue will return the object that was built by the base.
            # It will return None if the base did not have enough resources to build.
            obj = self.build_queue(base)

        # Try to find an enemy target
        # If there are multiple teams in the info, find the first team that is not mine
        if len(info) > 1:
            for name in info:
                if name != self.team:
                    # Target only bases
                    if "bases" in info[name]:
                        # Simply target the first base
                        t = info[name]["bases"][0]
                        myinfo["target"] = [t.x, t.y]
                        break

        # Control all my vehicles
        helpers.control_vehicles(
            info=myinfo, game_map=game_map, tank=tank_ai, ship=ship_ai, jet=jet_ai
        )
