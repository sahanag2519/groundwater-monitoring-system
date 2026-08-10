
from flask import Flask, request, render_template
import sqlite3
import os

from database import insert_data
from alert import check_overall_status
from prediction import get_prediction
from analysis import create_graphs


app = Flask(__name__)


# =========================================================
# HOME / DASHBOARD
# =========================================================

@app.route("/")
def home():

    db_path = os.path.abspath("groundwater.db")

    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()


    # -----------------------------------------------------
    # Get village and well selected by user
    # -----------------------------------------------------

    selected_village = request.args.get(
        "village"
    )

    selected_well = request.args.get(
        "well"
    )


    # -----------------------------------------------------
    # Get all villages
    # -----------------------------------------------------

    cursor.execute("""
        SELECT DISTINCT village
        FROM sensor_data
        WHERE village IS NOT NULL
        ORDER BY village
    """)

    villages = [
        row[0]
        for row in cursor.fetchall()
    ]


    # -----------------------------------------------------
    # If no village selected, use first village
    # -----------------------------------------------------

    if not selected_village:

        if villages:

            selected_village = villages[0]

        else:

            selected_village = "Village A"


    # -----------------------------------------------------
    # Get wells for selected village
    # -----------------------------------------------------

    cursor.execute("""
        SELECT DISTINCT well
        FROM sensor_data
        WHERE village = ?
        AND well IS NOT NULL
        ORDER BY well
    """, (selected_village,))


    wells = [
        row[0]
        for row in cursor.fetchall()
    ]


    # -----------------------------------------------------
    # If no well selected, use first well
    # -----------------------------------------------------

    if not selected_well:

        if wells:

            selected_well = wells[0]

        else:

            selected_well = "Well 1"


    # -----------------------------------------------------
    # Get latest reading for selected village + well
    # -----------------------------------------------------

    cursor.execute("""
        SELECT water_level, tds, time
        FROM sensor_data
        WHERE village = ?
        AND well = ?
        ORDER BY id DESC
        LIMIT 1
    """, (
        selected_village,
        selected_well
    ))


    row = cursor.fetchone()


    # -----------------------------------------------------
    # Get latest reading from every village
    # -----------------------------------------------------

    overview = []


    for village in villages:

        cursor.execute("""
            SELECT well, water_level, tds, time
            FROM sensor_data
            WHERE village = ?
            ORDER BY id DESC
            LIMIT 1
        """, (village,))


        village_row = cursor.fetchone()


        if village_row:

            well, water_level, tds, time = village_row


            status = check_overall_status(
                water_level,
                tds
            )


            overview.append({

                "village": village,

                "well": well,

                "water_level":
                    round(water_level, 2),

                "tds":
                    tds,

                "status":
                    status,

                "time":
                    time
            })


    connection.close()


    # -----------------------------------------------------
    # No data available
    # -----------------------------------------------------

    if row is None:

        return render_template(
            "index.html",

            village=selected_village,

            well=selected_well,

            villages=villages,

            wells=wells,

            overview=overview,

            water_level=None,

            tds=None,

            time="No data",

            status="NO DATA",

            prediction={
                "current_level": None,
                "predicted_level": None,
                "slope": None,
                "status": "Not enough data",
                "risk_level": "UNKNOWN",
                "readings_remaining": None,
                "estimated_time": "Not enough data"
            },

            water_graph=None,

            tds_graph=None
        )


    # -----------------------------------------------------
    # Selected reading
    # -----------------------------------------------------

    water_level, tds, time = row


    # -----------------------------------------------------
    # Water quality status
    # -----------------------------------------------------

    status = check_overall_status(
        water_level,
        tds
    )


    # -----------------------------------------------------
    # Village-specific prediction
    # -----------------------------------------------------

    prediction = get_prediction(
        selected_village,
        selected_well
    )


    # -----------------------------------------------------
    # Village-specific graphs
    # -----------------------------------------------------

    graphs = create_graphs(
        selected_village,
        selected_well
    )


    # -----------------------------------------------------
    # Send everything to dashboard
    # -----------------------------------------------------

    return render_template(

        "index.html",

        village=selected_village,

        well=selected_well,

        villages=villages,

        wells=wells,

        overview=overview,

        water_level=water_level,

        tds=tds,

        time=time,

        status=status,

        prediction=prediction,

        water_graph=graphs["water_graph"],

        tds_graph=graphs["tds_graph"]
    )


# =========================================================
# RECEIVE SENSOR DATA
# =========================================================

@app.route("/data", methods=["POST"])
def receive_data():

    data = request.get_json()


    village = data["village"]

    well = data["well"]

    water_level = data["water_level"]

    tds = data["tds"]


    # Store data
    insert_data(
        village,
        well,
        water_level,
        tds
    )


    print(
        "Data received:",
        data
    )


    return {
        "message":
            "Data received successfully"
    }


# =========================================================
# RUN FLASK
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
