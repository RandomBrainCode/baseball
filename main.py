#!python3.13

from pybaseball import statcast
import pandas as pd
import tabulate
from pathlib import Path
from datetime import datetime, timedelta


def get_playbyplay(gamedate: str) -> pd.DataFrame:
	folder: Path = Path(__file__).parent.joinpath('.data')
	if not folder.exists():
		folder.mkdir(parents=True)

	if not (folder / f'pbp_{gamedate}.parquet').exists():
		print(f'Downloading {gamedate} playbyplay')
		df: pd.DataFrame = statcast(start_dt=gamedate)
		df.to_parquet(folder / f'pbp_{gamedate}.parquet')
		return df

	print(f'{gamedate} playbyplay already exists, loading from disk')
	df: pd.DataFrame = pd.read_parquet(folder / f'pbp_{gamedate}.parquet')
	return df


def main():
	gamedate: str = '2025-06-25'
	df: pd.DataFrame = get_playbyplay(gamedate)
	df = df.loc[df['player_name'] == 'deGrom, Jacob']
	df = df.sort_values(['inning', 'at_bat_number', 'pitch_number'])
	# dfs: pd.DataFrame = pd.concat([df.head(10), df.tail(10)])
	columns: list[str] = ['pitcher', 'inning', 'at_bat_number', 'pitch_number', 'events', 'description', ]
	print(tabulate.tabulate(df[columns], headers=columns))
	print(len(df))
	print(df['description'].unique())
	print(df['events'].unique())


def get_current_season():
	start_date = datetime(2025, 3, 18)
	target_date = start_date

	while target_date.date() < datetime.now().date():
		target: str = target_date.date().strftime('%Y-%m-%d')
		_ = get_playbyplay(target)
		target_date += timedelta(days=1)


if __name__ == "__main__":
	main()
