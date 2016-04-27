# This is a fork that is meant to work in AWS environment
# Governor: A Template for PostgreSQL HA with etcd

*There are many ways to run high availability with PostgreSQL; here we present a template for you to create your own custom fit high availability solution using etcd and python for maximum accessibility.*

Compose runs a a [Postgresql as a service platform](https://www.compose.io/postgresql), which is highly-available from creation.  This is a coded example from our prior blog post: [High Availability for PostgreSQL, Batteries Not Included](https://blog.compose.io/high-availability-for-postgresql-batteries-not-included/).

## Getting Started
To get started, do the following from different terminals:

```
> etcd --data-dir=data/etcd
> ./governor.py postgres.yml
```

From there, you will see a high-availability cluster start up. Test
different settings in the YAML files to see how behavior changes.  Kill
some of the different components to see how the system behaves.

Add more `postgres*.yml` files to create an even larger cluster.

## How Governor works

For a diagram of the high availability decision loop, see the included a PDF: [postgres-ha.pdf](https://github.com/compose/template-etcd-based-postgres-ha/blob/master/postgres-ha.pdf)

## Requirements on a Mac

Run the following on a Mac to install requirements:

```
brew install postgresql etcd haproxy libyaml python
pip install psycopg2 pyyaml
```

## Notice

There are many different ways to do HA with PostgreSQL, see [the
PostgreSQL documentation](https://wiki.postgresql.org/wiki/Replication,_Clustering,_and_Connection_Pooling) for a complete list.

We call this project a "template" because it is far from a one-size fits
all, or a plug-and-play replication system.  It will have it's own
caveats.  Use wisely. 
