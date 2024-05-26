import pandas as pd
import argparse
import os


def analyze(args):
    dataset_dir_path = args.dataset_dir_path
    output_dir_path = args.output_dir_path

    output_df = pd.DataFrame()

    # list up the files in the dataset directory
    files = os.listdir(dataset_dir_path)

    # read the data
    for file in files:
        user_id = file.replace(".xlsx", "").replace("sleep", "")
        file_path = os.path.join(dataset_dir_path, file)
        data = pd.read_excel(file_path)
        data["user_id"] = user_id
        # 1列目をインデックスにする
        data = data.set_index(data.columns[0])
        # データを結合する
        output_df = pd.concat([output_df, data])

    # save the data
    output_file_path = os.path.join(output_dir_path, "sleep.csv")
    output_df.to_csv(output_file_path, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze sleep data")
    parser.add_argument(
        "--dataset_dir_path", type=str, help="Path to the dataset directory"
    )
    parser.add_argument(
        "--output_dir_path", type=str, help="Path to the output directory"
    )
    args = parser.parse_args()
    analyze(args)
