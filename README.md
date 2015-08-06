# Herqles CLI

The CLI is a plugin based tool to interact with the APIs made available by the Herqles system. This tool can be
expanded by making simple plugins to interact with new frameworks.

## Requirements

* Herqles System
* Python 2.7 - Not tested with newer python versions

## Quick Start Guide

## Usage

```
herq --help
```

### Installation

Install the base command line client

```
pip install hq-cli
```

Install any additional command line plugins

```
pip install mycliplugin
```

### Configuration

#### Base Configuration

##### File

```
~/.herq/config.yaml  
```

##### Config Parameters

Name | Type | Description | Default | Required
-----|------|-------------|---------|---------
manager_url | URL | the url for the herqles manager | None | [X]
framework_url | URL | the url for the herqles framework | None | [X]
username | String | the username to authenticate as | logged in user | [O]
password | String | the password of the user to authenticate | will prompt if not given | [O]

##### Example

```
manager_url: 'https://hq-manager.example.com'
framework_url: 'https://hq-framework.example.com'
```

#### Plugin Configuration

Auto Loaded Plugins:

* Job
* Task
* User
* Worker

##### File

```
~/.herq/plugins/myplugin.yaml
```

##### Config Parameters

Name | Type | Description | Default | Required
-----|------|-------------|---------|---------
module | string | the module where the plugin is located | None | [X]
framework_url | URL | the framework url to use instead of the default | framework_url from main config | [O]
manager_url | string | the manager url to use instead of the default  | manager_url from main config | [O]

**More configuration parameters my be needed depending on the plugins used**

##### Example

```
module: 'my.awesome.plugin'
```

