"""
This test can run only after overcloud cloud provider created and linked to
undercloud infra provider, need to compare the cloud providers with the
results of the relationships
"""
import pytest

from cfme.infrastructure.provider.openstack_infra import OpenstackInfraProvider
from cfme.utils.appliance.implementations.ui import navigate_to


pytestmark = [
    pytest.mark.meta(server_roles='+smartproxy +smartstate'),
    pytest.mark.usefixtures("setup_provider_modscope"),
    pytest.mark.provider([OpenstackInfraProvider], scope='module'),
]


def test_assigned_roles(provider):
    view = navigate_to(provider, 'Details')
    try:
        res = view.entities.summary('Relationships').get_text_of('Deployment Roles')
    except NameError:
        res = view.entities.summary('Relationships').get_text_of('Clusters / Deployment Roles')
    assert int(res) > 0


def test_nodes(provider):
    view = navigate_to(provider, 'Details')
    nodes = len(provider.mgmt.list_node())

    assert int(view.entities.summary('Relationships').get_text_of('Nodes')) == nodes


def test_templates(provider, soft_assert):
    view = navigate_to(provider, 'Details')
    images = [i.name for i in provider.mgmt.images]

    ui_images = view.entities.view.entities.relationships.get_text_of('Templates')
    assert int(ui_images) == len(images)

    templates_view = navigate_to(provider, 'ProviderTemplates')
    template_names = templates_view.entities.entity_names

    for image in images:
        soft_assert(image not in template_names, 'Missing template: {}'.format(image))


def test_stacks(provider):
    view = navigate_to(provider, 'Details')
    """
    todo get the list of tenants from external resource and compare
    it with result - currently not 0
    """

    assert int(view.entities.summary('Relationships').get_text_of('Orchestration stacks')) > 0
