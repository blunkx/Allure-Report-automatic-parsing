import click
import download
import parse
import output


@click.command()
@click.option(
    "-r", "--reportfile", "url_path", required=True, help="Enter the url or Path"
)
@click.option("-o", "--output", "out_path", default="", help="Enter the Path to output")
def exe(url_path, out_path):
    """
    Args:
        url_path(str)
        output_path(str)
    Returns:
        None
    Execute all flow of download and parsing
    Get url_path and out_path from command line
    Output the csv file to the path from user.
    """
    download.check_input(url_path)
    func_data = parse.create_func_list()
    print("Total test cases: %d" % len(func_data[0]))
    func_list_without_para = parse.merge_para_func(*func_data)
    output.verify(*func_data, func_list_without_para)
    output.write_output(out_path, func_list_without_para)


if __name__ == "__main__":
    exe()
