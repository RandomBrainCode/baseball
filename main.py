#!python3.13

from pybaseball import statcast
import pandas as pd
import tabulate


def main():
	df: pd.DataFrame = statcast(start_dt='2025-06-26')
	dfs: pd.DataFrame = pd.concat([df.head(10), df.tail(10)])
	print(tabulate.tabulate(dfs, headers=dfs.columns))
	print(len(df))


if __name__ == "__main__":
	main()
