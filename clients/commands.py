import click
from clients.services import ClientServices
from clients.models import Client

@click.group()
def clients():
    """manages the client's lifecycle"""
    pass


@clients.command()
@click.option(
    '-n', '--name',
    type=str,
    prompt=True,
    help='The client name'
)
@click.option(
    '-c', '--company',
    type=str,
    prompt=True,
    help='The client company'
)
@click.option(
    '-e', '--email',
    type=str,
    prompt=True,
    help='The client email'
)
@click.option(
    '-p', '--position',
    type=str,
    prompt=True,
    help='The client position'
)
@click.pass_context
def create(ctx, name, company, email, position):
    """Creates a new client"""
    client = Client(name, company, email, position)
    client_service = ClientServices(ctx.obj['clients_table'])

    client_service.create_client(client)


@clients.command()
@click.pass_context
def list(ctx):
    """List all cients"""
    client_service = ClientServices(ctx.obj['clients_table'])
   
    clients_list = client_service.list_clients()

    click.echo('ID  |  Name  |  Company  |  Email  |  Position')
    click.echo('-' * 100)
    
    for client in clients_list:
        click.echo(f"{client['uid']} | {client['name']} | {client['company']} | {client['email']} | {client['position']}")


@clients.command()
@click.argument('client_uid', type=str)
@click.pass_context
def update(ctx, client_uid):
    """Updates the client's data"""
    client_service = ClientServices(ctx.obj['clients_table'])

    client = [client for client in client_service.list_clients() if client['uid'] == client_uid]

    if client:
        client = _update_client_flow(Client(**client[0]))
        client_service.update_client(client)

        click.echo('CLient updated!!')
    else:
        click.echo('Client not found!!')

    
def _update_client_flow(client):
    click.echo('Leave empty if you don want to modify the value')

    client.name = click.prompt('New name:', type=str, default=client.name)
    client.company = click.prompt('New company:', type=str, default=client.company)
    client.email = click.prompt('New email:', type=str, default=client.email)
    client.position = click.prompt('New position:', type=str, default=client.position)

    return client


@clients.command()
@click.argument('client_uid', type=str)
@click.pass_context
def delete(ctx, client_uid):
    """ Delete a client """
    client_service = ClientServices(ctx.obj['clients_table'])

    client = [client for client in client_service.list_clients() if client['uid'] == client_uid]
    
    if client:
        client_service.delete_client(client)

        click.echo('Cliente deleted')
    else:
        click.echo('Client not found')


all = clients