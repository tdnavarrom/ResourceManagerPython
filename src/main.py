import click
import process as ps


@click.group()
def cli():
    """A simple Resource Manager written in Python"""
    click.echo("###Simple Resource Manager###")

@cli.command()
@click.argument('disk_partition')
def disk_usage(disk_partition):

    """ Returns the capacity of the partitions. \n
        Insert the name the partition as a parameter to use this option."""

    if disk_partition == 'all':
        d_partitions = ps.get_disk_paritions()
    
        for x in d_partitions:
            d_usage = ps.get_disk_usage(x.mountpoint)
            #help(d_usage)
            click.echo("Disk name: '%s'\n Capacity: %s" % (x.mountpoint, d_usage.percent))

    else:
        d_usage = ps.get_disk_usage(disk_partition.mountpoint)
        click.echo("Disk name: '%s'\n Capacity: %s" % (disk_partition.mountpoint, d_usage.percent))

@cli.command()
def disk_partitions():

    """ Returns all the partitions in the devices"""

    d_partitions = ps.get_disk_paritions()
    
    for x in d_partitions:
        click.echo(x.mountpoint)

@cli.command()
def processes():

    """ Returns all the processes running in the devices"""

    r_processes = ps.get_current_processes()
    
    for x in r_processes:
        click.echo("pid: %s name: %s memory: %s cpu: %s" % (x, r_processes[x]['name'],r_processes[x]['memory_percent'],r_processes[x]['cpu_num']) )

@cli.command()
@click.argument('pid', type=int)
def kill_process(pid):
    """ Kill Process by pid """
    ps.kill_process(pid)
    click.echo('Process %s has been terminated' % pid)

if __name__ == '__main__':
    cli()
