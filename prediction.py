
import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression


def get_prediction(village=None, well=None):

    connection = sqlite3.connect("groundwater.db")


    # -----------------------------------------
    # Get readings for selected village and well
    # -----------------------------------------

    if village is not None and well is not None:

        df = pd.read_sql_query("""
            SELECT water_level, tds, time
            FROM sensor_data
            WHERE village = ?
            AND well = ?
            ORDER BY id DESC
            LIMIT 20
        """, connection, params=(village, well))

    else:

        df = pd.read_sql_query("""
            SELECT water_level, tds, time
            FROM sensor_data
            ORDER BY id DESC
            LIMIT 20
        """, connection)


    connection.close()


    # Reverse data so it is chronological
    df = df.iloc[::-1].reset_index(drop=True)


    # -----------------------------------------
    # Need at least 5 readings
    # -----------------------------------------

    if len(df) < 5:

        return {

            "current_level": None,

            "predicted_level": None,

            "slope": None,

            "status": "Not enough data",

            "risk_level": "UNKNOWN",

            "readings_remaining": None,

            "estimated_time": "Not enough data"

        }


    # -----------------------------------------
    # Convert time
    # -----------------------------------------

    df["time"] = pd.to_datetime(
        df["time"]
    )


    # Create reading numbers
    df["reading_number"] = range(
        1,
        len(df) + 1
    )


    # -----------------------------------------
    # Linear Regression
    # -----------------------------------------

    X = df[["reading_number"]]

    y = df["water_level"]


    model = LinearRegression()

    model.fit(X, y)


    # -----------------------------------------
    # Current water level
    # -----------------------------------------

    current_level = float(
        df["water_level"].iloc[-1]
    )


    # -----------------------------------------
    # Rate of change
    # -----------------------------------------

    slope = float(
        model.coef_[0]
    )


    # -----------------------------------------
    # Predict next water level
    # -----------------------------------------

    next_reading_number = (
        len(df) + 1
    )


    next_reading = pd.DataFrame({

        "reading_number":
            [next_reading_number]

    })


    predicted_level = float(
        model.predict(next_reading)[0]
    )


    # -----------------------------------------
    # Critical level
    # -----------------------------------------

    critical_level = 2.0


    # -----------------------------------------
    # Average time between readings
    # -----------------------------------------

    time_difference = (
        df["time"].iloc[-1]
        -
        df["time"].iloc[0]
    ).total_seconds()


    number_of_intervals = (
        len(df) - 1
    )


    if number_of_intervals > 0:

        average_seconds_per_reading = (
            time_difference /
            number_of_intervals
        )

    else:

        average_seconds_per_reading = 0


    # -----------------------------------------
    # Trend status
    # -----------------------------------------

    if slope < -0.01:

        status = "DECREASING"

    elif slope > 0.01:

        status = "INCREASING"

    else:

        status = "STABLE"


    # -----------------------------------------
    # Time until critical level
    # -----------------------------------------

    if slope < 0:

        readings_remaining = (
            (current_level - critical_level)
            /
            abs(slope)
        )


        # Prevent negative values
        readings_remaining = max(
            0,
            readings_remaining
        )


        estimated_seconds = (
            readings_remaining
            *
            average_seconds_per_reading
        )


        estimated_minutes = (
            estimated_seconds / 60
        )


        estimated_hours = (
            estimated_seconds / 3600
        )


        if estimated_hours >= 1:

            estimated_time = (
                f"{estimated_hours:.2f} hours"
            )

        else:

            estimated_time = (
                f"{estimated_minutes:.2f} minutes"
            )


    else:

        readings_remaining = None

        estimated_time = "Not applicable"


    # -----------------------------------------
    # Groundwater Risk Assessment
    # -----------------------------------------

    if current_level <= 2.0:

        risk_level = "HIGH"

    elif predicted_level <= 2.0:

        risk_level = "HIGH"

    elif current_level <= 2.5:

        risk_level = "MODERATE"

    elif predicted_level <= 2.5:

        risk_level = "MODERATE"

    elif slope < -0.01:

        risk_level = "MODERATE"

    else:

        risk_level = "LOW"


    # -----------------------------------------
    # Return prediction
    # -----------------------------------------

    return {

        "current_level":
            round(
                current_level,
                2
            ),

        "predicted_level":
            round(
                predicted_level,
                2
            ),

        "slope":
            round(
                slope,
                4
            ),

        "status":
            status,

        "risk_level":
            risk_level,

        "readings_remaining":

            (
                round(
                    readings_remaining,
                    2
                )

                if readings_remaining is not None

                else None
            ),

        "estimated_time":
            estimated_time
    }


# -----------------------------------------
# Test
# -----------------------------------------

if __name__ == "__main__":

    print(
        get_prediction(
            "Village A",
            "Well 1"
        )
    )

