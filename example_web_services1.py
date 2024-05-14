#! pip install diagrams

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import Route53, ELB
from diagrams.aws.compute import ECS
from diagrams.aws.database import RDS
from diagrams.aws.database import Elasticache

# Create the diagram
with Diagram("Clustered Web Services", show=False):
    # DNS and Load Balancer
    dns = Route53("dns")
    lb = ELB("lb")

    # Services Cluster
    with Cluster("Services"):
        svc_group = [
            ECS("web1"),
            ECS("web2"),
            ECS("web3")
        ]

    # Database Cluster
    with Cluster("DB Cluster"):
        db_primary = RDS("userdb")
        db_replicas = RDS("userdb ro")

        # Define the replication relationship
        db_primary >> Edge(label="replication") >> db_replicas

    # ElastiCache
    memcached = Elasticache("memcached")

    # Define connections
    dns >> lb
    lb >> svc_group
    svc_group >> db_primary
    svc_group >> memcached
