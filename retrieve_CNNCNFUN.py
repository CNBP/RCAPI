import click



@click.command()
@click.argument('cnbpid')
def run(cnbpid):
	import sys
	from pathlib import Path

	str_path_project = str(Path(__file__).resolve().absolute())
	sys.path.append(str_path_project)
	from API import CNNCNFUN_data_retrieval
	retrieval = CNNCNFUN_data_retrieval(cnbpid)
	retrieval.write_all_csv()



if __name__=="__main__":
	run()
