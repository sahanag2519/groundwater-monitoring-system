
import requests
import random
import time


# Flask server
url = "http://127.0.0.1:5000/data"


# =========================================================
# VILLAGE + WELL SETTINGS
# =========================================================

locations = {

    ("Village A", "Well 1"): {
        "level": 4.5,
        "change": (-0.01, 0.02),
        "tds": (280, 450)
    },

    ("Village A", "Well 2"): {
        "level": 3.9,
        "change": (-0.04, 0.01),
        "tds": (300, 500)
    },


    ("Village B", "Well 1"): {
        "level": 2.8,
        "change": (-0.05, 0.01),
        "tds": (400, 650)
    },

    ("Village B", "Well 2"): {
        "level": 4.2,
        "change": (-0.01, 0.02),
        "tds": (280, 450)
    },


    ("Village C", "Well 1"): {
        "level": 2.3,
        "change": (-0.06, -0.02),
        "tds": (450, 700)
    },

    ("Village C", "Well 2"): {
        "level": 3.6,
        "change": (-0.02, 0.02),
        "tds": (300, 500)
    },


    ("Village D", "Well 1"): {
        "level": 1.8,
        "change": (-0.03, 0.01),
        "tds": (600, 900)
    },

    ("Village D", "Well 2"): {
        "level": 3.1,
        "change": (-0.04, 0.01),
        "tds": (450, 700)
    },


    ("Village E", "Well 1"): {
        "level": 4.6,
        "change": (-0.01, 0.02),
        "tds": (280, 450)
    },

    ("Village E", "Well 2"): {
        "level": 2.6,
        "change": (-0.04, 0.01),
        "tds": (400, 650)
    }
}
# =========================================================
# SEND DATA
# =========================================================

while True:

    for location, settings in locations.items():

        village, well = location


        # ---------------------------------------------
        # Change water level
        # ---------------------------------------------

        change = random.uniform(
            settings["change"][0],
            settings["change"][1]
        )


        settings["level"] += change


        # Keep water level realistic
        settings["level"] = max(
            1.0,
            min(
                settings["level"],
                5.0
            )
        )


        # ---------------------------------------------
        # Generate TDS
        # ---------------------------------------------

        tds = random.randint(
            settings["tds"][0],
            settings["tds"][1]
        )


        # ---------------------------------------------
        # Create sensor data
        # ---------------------------------------------

        data = {

            "village":
                village,

            "well":
                well,

            "water_level":
                round(
                    settings["level"],
                    2
                ),

            "tds":
                tds
        }


        # ---------------------------------------------
        # Send to Flask
        # ---------------------------------------------

        try:

            response = requests.post(
                url,
                json=data
            )


            print(
                f"{village} | "
                f"{well} | "
                f"Water Level: "
                f"{data['water_level']} m | "
                f"TDS: "
                f"{data['tds']} ppm"
            )


        except requests.exceptions.RequestException as error:

            print(
                "Could not connect to Flask:",
                error
            )


        # Small delay between wells
        time.sleep(2)


    print()
    print(
        "========== NEW CYCLE =========="
    )
    print()


    # Wait before next cycle
    time.sleep(5)

