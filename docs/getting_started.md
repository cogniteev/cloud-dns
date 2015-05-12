# Getting started

This page described the step-by-step intructions to use Cloud DNS.

Cloud DNS leverages [Apache LibCloud](https://libcloud.apache.org/) library to retrieve IP addresses of the nodes you connect to on the cloud.

Accessing clouds APIs requires authentication. Cloud DNS uses GPG encryption to share and publish your clouds profiles configuration.

As of now, it is only possible to store configuration on Google Storage.

## Prerequisites

You may have:
* a [keybase](https://keybase.io) account properly configured with at least one key defined.
* A Google Storage bucket with public permissions

## Installation

Install the Cloud DNS Python module:

```shell
pip install cloud-dns
```

## Bootstrap

### Somebody already setup a profile for my crew

In this situation, a profile has already been pushed to a Google Storage bucket by one of your co-worker. There is no need to create a profile by end. You just need to pull it. To do so:

1. Provider your co-worker with your keybase identity so that he can push an encrypted version of the profile on Google Storage. say `github://john.doe`
1. Ask your co-worker to give you:
    * The Google Storage **bucket name**, say *acme-cloud-dns*
    * The **profile name** to pull, say *acme*
1. Run the following command:

    ```shell
    cloud-dns config pull my-company my-company-cloud-dns github://john.doe
    ```

That's it!!! The profile should be available in `~/.config/cloud-dns/my-company`

### I have to create a new profile

FIXME :)

## Main operations

### Listing all nodes

To see list of nodes available in your profiles:

```shell
cloud-dns etc-hosts list
```

### Update your `/etc/hosts`

To patch your `/etc/hosts` file with IP addresses your all nodes of your cloud:

```
cloud-dns etc-hosts update
```

Note that your can specify an alternate file with the `--output` option.

### Push an updated configuration

When you modify your profiles (in `~/.config/cloud-dns`), you might want to publish them so that your co-workers can take benefits of it:

```shell
cloud-dns config push <profile> <gstorage-bucket>
```

Note: this does not support concurrent modifications for now: the last one pushing wins!

### Share a profile with a co-worker

To allow another user to *pull* a profile, add its keybase identity to the `~/.config/cloud-dns/<PROFILE>/users.yml` and *push* the profile. This will push to Google Storage an encrypted version of the profile for this user.
