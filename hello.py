import click
import ast


class PythonLiteralOption(click.Option):

    def type_cast_value(self, ctx, value):
        try:
            return ast.literal_eval(value)
        except:
            raise click.BadParameter(value)


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--option1', cls=PythonLiteralOption, default=[])
# @click.option('--option2', cls=PythonLiteralOption, default=[])
def cli(option1):
    print(option1)
    # click.echo("Option 1, type: {}  value: {}".format(
    #     type(option1), option1))


# do stuff
if __name__ == '__main__':
    # import shlex
    # cli(shlex.split(
    #     '''--option1 '["o11", "o12", "o13"]'
    # --option2 '["o21", "o22", "o23"]' '''))
    cli()
