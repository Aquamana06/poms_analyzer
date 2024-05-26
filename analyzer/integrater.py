import pandas as pd
import argparse
import os


def integrater(args):
    dataset_dir_path = args.dataset_dir_path
    output_dir_path = args.output_dir_path
    dataset_name = args.dataset_name
    delete_first_column = args.delete_first_column

    output_df = pd.DataFrame()

    # list up the files in the dataset directory
    files = os.listdir(dataset_dir_path)

    # read the data
    for file in files:
        user_id = file.replace(".xlsx", "").replace(dataset_name, "")
        file_path = os.path.join(dataset_dir_path, file)
        data = pd.read_excel(file_path)
        data["user_id"] = user_id
        if delete_first_column:
            data = data.iloc[:, 1:]
        # データを結合する
        output_df = pd.concat([output_df, data])

    # save the data
    output_file_path = os.path.join(output_dir_path, f"{dataset_name}.csv")
    output_df.to_csv(output_file_path, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="convert xlsx files to csv file.")
    parser.add_argument(
        "--dataset_dir_path", type=str, help="Path to the dataset directory"
    )
    parser.add_argument(
        "--output_dir_path", type=str, help="Path to the output directory"
    )
    parser.add_argument(
        "--dataset_name", type=str, help="Name of the dataset", default="sleep"
    )
    parser.add_argument(
        "--delete_first_column",
        action="store_true",
        help="Delete the first column of the data",
    )
    args = parser.parse_args()
    integrater(args)
