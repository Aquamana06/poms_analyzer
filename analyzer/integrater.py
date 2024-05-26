import pandas as pd
import argparse
import os


def integrater(args):
    dataset_dir_path = args.dataset_dir_path
    output_dir_path = args.output_dir_path
    dataset_name = args.dataset_name
    delete_first_column = args.delete_first_column
    replace_column_name = args.replace_column_name

    output_df = pd.DataFrame()

    # データセットディレクトリ内のファイルを列挙する
    files = os.listdir(dataset_dir_path)

    # データを読み込む
    for file in files:
        user_id = file.replace(".xlsx", "").replace(dataset_name, "")
        file_path = os.path.join(dataset_dir_path, file)
        data = pd.read_excel(file_path)
        data["user_id"] = user_id
        if delete_first_column:
            data = data.iloc[:, 1:]
        if replace_column_name:
            from_column_name, to_column_name = replace_column_name.split("-")
            data = data.rename(columns={from_column_name: to_column_name})
        # データを結合する前にチェックする
        if not data.empty and not data.isna().all().all():
            output_df = pd.concat([output_df, data])

    # データを保存する
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
    parser.add_argument(
        "--replace_column_name", type=str, help="Replace the column name"
    )
    args = parser.parse_args()
    integrater(args)
