import pandas as pd


def main():
    df = pd.read_csv("dataset/csv/POMS.csv")
    # 残すカラムを指定
    df = df[["user_id", "time", "drinking", "caffeine", "T-A"]]

    df["caffeine"] = df["caffeine"].replace({"はい": 1, "いいえ": 0})
    df["drinking"] = df["drinking"].replace({"はい": 1, "いいえ": 0})

    save_path = "dataset/csv/poms_cleaned.csv"
    df.to_csv(save_path, index=False)


if __name__ == "__main__":
    main()
