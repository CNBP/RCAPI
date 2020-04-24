import click



@click.command()
@click.option('--url', '-u', help="The url to attempt the retrieval from.")
@click.argument('cnbpid')
def run(cnbpid, url):
	import sys
	from pathlib import Path

	str_path_project = str(Path(__file__).resolve().absolute())
	sys.path.append(str_path_project)
	from API import CNNCNFUN_data_retrieval
	retrieval = CNNCNFUN_data_retrieval(cnbpid, url=url)
	retrieval.write_all_csv()



if __name__=="__main__":
	run()
