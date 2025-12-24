import logging

import click

from app.cli_runner import run_cli_mode
from app.tui_runner import run_tui_mode
from config import load_config
from util.logger import setup_logger

logger = logging.getLogger("iot_home")


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--mode', type=click.Choice(['cli', 'tui']), default='tui', 
              help='Interface mode (default: tui)')
@click.option(
    '--config',
    default='./config.json',
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help='Config file path'
)
@click.option('--debug', is_flag=True, help='Enable debug logging')
def cli(ctx: click.Context, mode: str, config: str, debug: bool) -> None:
    log_level = logging.DEBUG if debug else logging.INFO
    setup_logger(mode=mode, level=log_level)

    ctx.ensure_object(dict)
    ctx.obj['config'] = config

    if ctx.invoked_subcommand is None:
        if mode == 'cli':
            ctx.invoke(run_cli)
        else:
            ctx.invoke(run_tui)


@cli.command()
@click.pass_context
def run_cli(ctx: click.Context) -> None:
    run_cli_mode(ctx.obj['config'])


@cli.command()
@click.pass_context
def run_tui(ctx: click.Context) -> None:
    run_tui_mode(ctx.obj['config'])


@cli.command()
@click.pass_context
def status(ctx: click.Context) -> None:
    try:
        config = load_config(ctx.obj['config'])
        
        click.echo("\n" + "="*40)
        click.echo("  IoT Home System Status")
        click.echo("="*40 + "\n")
        
        click.echo("Component Configuration:")
        click.echo(f"  DS1:  {'Simulated' if config.ds1_config.simulated else 'Hardware'}")
        click.echo(f"  DUS1: {'Simulated' if config.dus1_config.simulated else 'Hardware'}")
        click.echo(f"  DPIR1: {'Simulated' if config.dpir1_config.simulated else 'Hardware'}")
        click.echo(f"  DMS: {'Simulated' if config.dms_config.simulated else 'Hardware'}")
        click.echo(f"  DB: {'Simulated' if config.db_config.simulated else 'Hardware'}")
        click.echo(f"  DL:   {'Simulated' if config.dl_config.simulated else 'Hardware'}")
        
        click.echo()
        
    except Exception as e:
        click.echo(f"Error loading configuration: {e}", err=True)
        raise click.Abort()
