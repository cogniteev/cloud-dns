# Getting started

This page described the step-by-step intructions to use Cloud DNS.

Cloud DNS leverages [Apache LibCloud](https://libcloud.apache.org/) library to retrieve IP addresses of nodes you can reach from your cloud providers.

Accessing clouds APIs requires authentication. Cloud DNS uses GPG encryption to share and publish your clouds profiles configuration.

As of now, it is only possible to store profile configurations on Google Storage.

## Prerequisites

You may have:

* a [keybase](https://keybase.io) account properly configured with at least one key defined.
* A Google Storage bucket with read public permissions

## Installation

Install Cloud DNS Python module:

```shell
pip install cloud-dns==0.1b
```

As Cloud DNS has many dependencies, it is recommended to install it in a virtualenv.

## Bootstrap

### Somebody already setup a profile for my crew

In this situation, a profile has already been pushed to a Google Storage bucket by one of your co-worker. There is no need to create a profile by end. You just need to pull it. To do so:

1. Provide your co-worker with your keybase identity so that he can push an encrypted version of the profile on Google Storage. say `github://john.doe`
1. In return, ask your co-worker to provide you:
    * The Google Storage **bucket name**, say *acme-cloud-dns*
    * The **profile name** to pull, say *acme*
1. Run the following command:

    ```
    cloud-dns config -v pull my-company my-company-cloud-dns github://john.doe
    ```

That's it!
The profile should be available in `~/.config/cloud-dns/my-company`

### I have to create a new profile

FIXME :)

## Main operations

### Listing all nodes

To see list of nodes available in the cloud providers specified in your profiles:

```shell
cloud-dns etc-hosts list
```

### Update your `/etc/hosts`

To patch your `/etc/hosts` file with IP addresses your nodes specified in your profiles:

```
cloud-dns etc-hosts update
```

Note that your can specify an alternate file with the `--output` option.

### Push an updated configuration

When you modify a profile (in `~/.config/cloud-dns/<PROFILE>`), you might want to publish it afterward so that your co-workers can take benefits of this change:

```shell
cloud-dns config push -v <profile> <gstorage-bucket>
```

Note: this does not support concurrent modifications for now: the last one pushing wins!

### Share a profile with a co-worker

To allow another user to *pull* a profile, add its keybase identity to the `~/.config/cloud-dns/<PROFILE>/users.yml` and *push* the profile. This will push to Google Storage an encrypted version of the profile for this user.
