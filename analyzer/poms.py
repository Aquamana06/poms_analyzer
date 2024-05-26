import pandas as pd
import os
import argparse


def main(args):
    data_dir = args.data_dir
    output_file = args.output_file
    if not os.path.exists(data_dir):
        print("Data directory does not exist")
        return

    poms_df = pd.read_csv(os.path.join(data_dir, "poms_cleaned.csv"))
    poms_df["time"] = pd.to_datetime(poms_df["time"])
    if args.activity:
        activity_df = pd.read_csv(os.path.join(data_dir, "activity.csv"))
        activity_df["time"] = pd.to_datetime(activity_df["time"])
    if args.calender:
        calender_df = pd.read_csv(os.path.join(data_dir, "calender.csv"))
        calender_df["start"] = pd.to_datetime(calender_df["start"])
        calender_df["end"] = pd.to_datetime(calender_df["end"])
    if args.cloud:
        cloud_df = pd.read_csv(os.path.join(data_dir, "cloud.csv"))
        cloud_df["time"] = pd.to_datetime(cloud_df["time"])
    if args.heart:
        heart_df = pd.read_csv(os.path.join(data_dir, "heart.csv"))
        heart_df["time"] = pd.to_datetime(heart_df["time"])
    if args.sleep:
        sleep_df = pd.read_csv(os.path.join(data_dir, "sleep.csv"))
        sleep_df["start"] = pd.to_datetime(sleep_df["start"])
        sleep_df["end"] = pd.to_datetime(sleep_df["end"])
        sleep_df["sleep_date"] = pd.to_datetime(sleep_df["sleep_date"])
    if args.weather:
        weather_df = pd.read_csv(os.path.join(data_dir, "weather.csv"))
        weather_df["time"] = pd.to_datetime(weather_df["time"])

    poms_user_id_list = poms_df["user_id"].unique()
    output_rows = []

    for user_id in poms_user_id_list:
        user_poms_df = poms_df[poms_df["user_id"] == user_id]
        # user_poms_dfの各行に対して処理を行う
        for index, row in user_poms_df.iterrows():
            row_data = row.to_dict()
            if args.heart:
                user_heart_df = heart_df[heart_df["user_id"] == user_id]
                if not user_heart_df.empty:
                    closest_heart_row = user_heart_df.iloc[
                        (user_heart_df["time"] - row["time"]).abs().argsort()[:1]
                    ]
                    row_data["heart"] = closest_heart_row["heart"].values[0]
            if args.activity:
                user_activity_df = activity_df[activity_df["user_id"] == user_id]
                if not user_activity_df.empty:
                    closest_activity_row = user_activity_df.iloc[
                        (user_activity_df["time"] - row["time"]).abs().argsort()[:1]
                    ]
                    row_data["floors"] = closest_activity_row["floors"].values[0]
                    row_data["steps"] = closest_activity_row["steps"].values[0]
            output_rows.append(row_data)

    output_df = pd.DataFrame(output_rows)
    output_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process POMS data")
    parser.add_argument(
        "--data_dir", type=str, default="data", help="Directory containing POMS data"
    )
    parser.add_argument(
        "--output_file", type=str, default="output/result.csv", help="Output file name"
    )
    parser.add_argument("--activity", action="store_true", help="Process activity data")
    parser.add_argument("--calender", action="store_true", help="Process calender data")
    parser.add_argument("--cloud", action="store_true", help="Process cloud data")
    parser.add_argument("--heart", action="store_true", help="Process heart data")
    parser.add_argument("--sleep", action="store_true", help="Process sleep data")
    parser.add_argument("--weather", action="store_true", help="Process weather data")
    args = parser.parse_args()
    main(args)
