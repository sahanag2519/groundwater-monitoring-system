
import sqlite3
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import os


def create_graphs(village=None, well=None):

    conn = sqlite3.connect("groundwater.db")


    # -----------------------------------------
    # Get data for selected village and well
    # -----------------------------------------

    if village is not None and well is not None:

        df = pd.read_sql_query("""
            SELECT *
            FROM sensor_data
            WHERE village = ?
            AND well = ?
            ORDER BY id ASC
        """, conn, params=(village, well))

    else:

        df = pd.read_sql_query("""
            SELECT *
            FROM sensor_data
            ORDER BY id ASC
        """, conn)


    conn.close()


    if df.empty:

        return


    # -----------------------------------------
    # Convert time
    # -----------------------------------------

    df["time"] = pd.to_datetime(
        df["time"]
    )


    # -----------------------------------------
    # Create static folder
    # -----------------------------------------

    os.makedirs(
        "static",
        exist_ok=True
    )


    # -----------------------------------------
    # Safe filename
    # -----------------------------------------

    if village is not None:

        village_name = (
            village
            .replace(" ", "_")
            .lower()
        )

    else:

        village_name = "all"


    if well is not None:

        well_name = (
            well
            .replace(" ", "_")
            .lower()
        )

    else:

        well_name = "all"


    # =========================================
    # WATER LEVEL GRAPH
    # =========================================

    plt.figure(
        figsize=(10, 5)
    )


    plt.plot(
        df["time"],
        df["water_level"],
        marker="o"
    )


    plt.xlabel(
        "Time"
    )


    plt.ylabel(
        "Water Level (m)"
    )


    plt.title(
        f"Water Level - {village} - {well}"
    )


    plt.xticks(
        rotation=45
    )


    plt.tight_layout()


    water_filename = (
        f"static/water_level_"
        f"{village_name}_"
        f"{well_name}.png"
    )


    plt.savefig(
        water_filename
    )


    plt.close()


    # =========================================
    # TDS GRAPH
    # =========================================

    plt.figure(
        figsize=(10, 5)
    )


    plt.plot(
        df["time"],
        df["tds"],
        marker="o"
    )


    plt.xlabel(
        "Time"
    )


    plt.ylabel(
        "TDS (ppm)"
    )


    plt.title(
        f"TDS Variation - {village} - {well}"
    )


    plt.xticks(
        rotation=45
    )


    plt.tight_layout()


    tds_filename = (
        f"static/tds_"
        f"{village_name}_"
        f"{well_name}.png"
    )


    plt.savefig(
        tds_filename
    )


    plt.close()


    # Return filenames so Flask can use them

    return {

        "water_graph":
            water_filename
            .replace(
                "static/",
                ""
            ),

        "tds_graph":
            tds_filename
            .replace(
                "static/",
                ""
            )
    }


# =========================================
# TEST
# =========================================

if __name__ == "__main__":

    create_graphs()

    print(
        "Graphs updated successfully."
    )

