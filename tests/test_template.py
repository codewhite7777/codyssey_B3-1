from __future__ import annotations

from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml", reason="install requirements-test.txt to parse CloudFormation YAML")


class CloudFormationLoader(yaml.SafeLoader):
    """Parse intrinsic tags into their long-form mapping equivalents."""


def intrinsic_constructor(loader: CloudFormationLoader, tag_suffix: str, node: yaml.Node) -> dict[str, object]:
    tag_name = tag_suffix or node.tag.rsplit(":", maxsplit=1)[-1]
    key = {"!": "Ref"}.get(tag_name, tag_name)
    if isinstance(node, yaml.ScalarNode):
        value: object = loader.construct_scalar(node)
    elif isinstance(node, yaml.SequenceNode):
        value = loader.construct_sequence(node)
    else:
        value = loader.construct_mapping(node)
    return {key: value}


CloudFormationLoader.add_multi_constructor("!", intrinsic_constructor)

TEMPLATE_PATH = Path(__file__).parents[1] / "infra" / "template.yaml"


@pytest.fixture(scope="module")
def template() -> dict[str, object]:
    with TEMPLATE_PATH.open(encoding="utf-8") as stream:
        loaded = yaml.load(stream, Loader=CloudFormationLoader)
    assert isinstance(loaded, dict)
    return loaded


def test_template_contains_expected_network_shape(template: dict[str, object]) -> None:
    resources = template["Resources"]
    assert isinstance(resources, dict)
    expected = {
        "VPC",
        "PublicSubnet",
        "InternetGateway",
        "VPCGatewayAttachment",
        "PublicRouteTable",
        "DefaultPublicRoute",
        "PublicSubnetRouteTableAssociation",
        "WebSecurityGroup",
        "WebServer",
    }
    assert expected <= resources.keys()
    assert resources["VPC"]["Properties"]["CidrBlock"] == "10.0.0.0/16"
    assert resources["PublicSubnet"]["Properties"]["CidrBlock"] == "10.0.1.0/24"
    assert resources["PublicSubnet"]["Properties"]["MapPublicIpOnLaunch"] is True
    route = resources["DefaultPublicRoute"]["Properties"]
    assert route["DestinationCidrBlock"] == "0.0.0.0/0"
    assert route["GatewayId"] == {"Ref": "InternetGateway"}


def test_security_group_opens_only_http_and_parameterized_ssh(template: dict[str, object]) -> None:
    resources = template["Resources"]
    ingress = resources["WebSecurityGroup"]["Properties"]["SecurityGroupIngress"]
    by_port = {rule["FromPort"]: rule for rule in ingress}
    assert by_port[80]["CidrIp"] == "0.0.0.0/0"
    assert by_port[22]["CidrIp"] == {"Ref": "SSHIngressCidr"}


def test_instance_uses_ssm_al2023_t3_micro_and_eight_gib_root(template: dict[str, object]) -> None:
    parameters = template["Parameters"]
    resources = template["Resources"]
    assert parameters["InstanceType"]["Default"] == "t3.micro"
    assert parameters["SSHIngressCidr"]["Default"].endswith("/32")
    instance = resources["WebServer"]["Properties"]
    assert "al2023-ami-kernel-default-x86_64" in instance["ImageId"]
    root = instance["BlockDeviceMappings"][0]["Ebs"]
    assert root["VolumeSize"] == 8
    assert root["VolumeType"] == "gp3"
    user_data = instance["UserData"]["Fn::Base64"]["Sub"]
    assert "dnf install -y nginx" in user_data
    assert "/usr/share/nginx/html/health" in user_data
    assert "OK" in user_data


def test_required_outputs_and_ssm_role_are_present(template: dict[str, object]) -> None:
    resources = template["Resources"]
    outputs = template["Outputs"]
    assert {"WebInstanceId", "WebPublicIp", "HealthUrl"} <= outputs.keys()
    role = resources["SsmInstanceRole"]["Properties"]
    assert "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore" in role["ManagedPolicyArns"]
