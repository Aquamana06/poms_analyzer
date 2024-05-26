import pandas as pd


def main():
    df = pd.read_csv("dataset/csv/POMS.csv")
    profile_df = pd.read_excel("dataset/xlsx/profile.xlsx")
    bigfive_df = pd.read_excel("dataset/xlsx/BigFive.xlsx")

    # 残すカラムを指定
    df = df[["user_id", "time", "drinking", "caffeine", "T-A"]]

    # labeling
    df["caffeine"] = df["caffeine"].replace({"はい": 1, "いいえ": 0})
    df["drinking"] = df["drinking"].replace({"はい": 1, "いいえ": 0})

    # profile_df["参加者番号"]とdf["user_id"]を結合. dfにprofile_dfの情報を追加
    df = pd.merge(df, profile_df, left_on="user_id", right_on="参加者番号", how="left")
    df = df.drop(columns=["参加者番号"])

    # bigfive_df["参加者番号"]とdf["user_id"]を結合. dfにbigfive_dfの情報を追加
    df = pd.merge(df, bigfive_df, left_on="user_id", right_on="参加者番号", how="left")
    df = df.drop(columns=["参加者番号"])

    save_path = "dataset/csv/poms_cleaned.csv"
    df.to_csv(save_path, index=False)


if __name__ == "__main__":
    main()
