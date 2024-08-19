import pandas as pd

def main():
    file = input()
    func = input()

    scores_df = pd.read_csv(str(file))

    if func == 'Q1':
        print(scores_df.shape)
    elif func == 'Q2':
        print(scores_df['score'].max())
    elif func == 'Q3':
        filter = scores_df.score >= 80
        print(scores_df[filter].id.count())
    else:
        print("No Output")

if __name__ == "__main__":
    main()