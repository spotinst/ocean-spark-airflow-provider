import pytest
import unittest.mock
import re

from pytest_mock import MockerFixture

from airflow.models.connection import Connection


from requests_mock import Mocker as RequestsMocker


@pytest.fixture(scope="function")
def hook_request_mock(mocker: MockerFixture) -> unittest.mock.MagicMock:
    return mocker.patch(
        "ocean_spark.hooks.OceanSparkHook." "_run_request",
    )


@pytest.fixture(scope="function")
def successful_submission(requests_mock: RequestsMocker) -> None:
    requests_mock.real_http = True
    requests_mock.register_uri(
        "POST",
        re.compile("https://api.spotinst.io/ocean/spark/cluster/.*/app"),
        status_code=200,
        json={
            "request": {
                "id": "e593ff58-067d-4340-92f9-8b1c0bad70d7",
                "url": "string",
                "method": "string",
                "timestamp": "2018-06-20T11:35:01.745Z",
            },
            "response": {
                "status": {"code": 200, "message": "OK"},
                "items": [
                    {
                        "createdAt": "2018-10-10T10:50:29.000+0000",
                        "updatedAt": "2018-11-01T10:50:29.000+0000",
                        "internalId": "fa61bb92-4bb7-49aa-87d3-7823bd263d1e",
                        "id": "new-app-id",
                        "displayName": "Daily Reporting 2021-08-18",
                        "userId": 59438,
                        "clusterId": "test-cluster-id",
                        "controllerClusterId": "my-ocean-cluster",
                        "appState": "RUNNING",
                        "submissionSource": "public-api",
                        "job": {
                            "id": "daily-reporting",
                            "displayName": "Daily Reporting",
                        },
                        "config": {
                            "arguments": ["string"],
                            "deps": {
                                "files": ["string"],
                                "jars": ["string"],
                                "pyFiles": ["string"],
                            },
                            "driver": {
                                "affinity": {
                                    "nodeAffinity": {
                                        "preferredDuringSchedulingIgnoredDuringExecution": []
                                    },
                                    "podAffinity": {
                                        "preferredDuringSchedulingIgnoredDuringExecution": [],
                                        "requiredDuringSchedulingIgnoredDuringExecution": [],
                                    },
                                    "podAntiAffinity": {
                                        "preferredDuringSchedulingIgnoredDuringExecution": [],
                                        "requiredDuringSchedulingIgnoredDuringExecution": [],
                                    },
                                },
                                "annotations": {
                                    "property1": "string",
                                    "property2": "string",
                                },
                                "configMaps": [{}],
                                "coreLimit": "string",
                                "coreRequest": "string",
                                "cores": 0,
                                "envSecretKeyRefs": {
                                    "property1": {},
                                    "property2": {},
                                },
                                "envVars": {
                                    "property1": "string",
                                    "property2": "string",
                                },
                                "hostAliases": [{"hostnames": []}],
                                "image": "string",
                                "instanceType": "string",
                                "javaOptions": "string",
                                "labels": {
                                    "property1": "string",
                                    "property2": "string",
                                },
                                "memory": "string",
                                "memoryOverhead": "string",
                                "podName": "string",
                                "podSecurityContext": {
                                    "fsGroup": 0,
                                    "runAsGroup": 0,
                                    "runAsNonRoot": True,
                                    "runAsUser": 0,
                                    "seLinuxOptions": {},
                                    "supplementalGroups": [],
                                    "sysctls": [],
                                    "windowsOptions": {},
                                },
                                "secrets": [{}],
                                "securityContext": {
                                    "allowPrivilegeEscalation": True,
                                    "capabilities": {"add": [], "drop": []},
                                    "privileged": True,
                                    "procMount": "string",
                                    "readOnlyRootFilesystem": True,
                                    "runAsGroup": 0,
                                    "runAsNonRoot": True,
                                    "runAsUser": 0,
                                    "seLinuxOptions": {},
                                    "windowsOptions": {},
                                },
                                "spot": True,
                                "tolerations": [{}],
                                "volumeMounts": [{}],
                            },
                            "executor": {
                                "affinity": {
                                    "nodeAffinity": {
                                        "preferredDuringSchedulingIgnoredDuringExecution": []
                                    },
                                    "podAffinity": {
                                        "preferredDuringSchedulingIgnoredDuringExecution": [],
                                        "requiredDuringSchedulingIgnoredDuringExecution": [],
                                    },
                                    "podAntiAffinity": {
                                        "preferredDuringSchedulingIgnoredDuringExecution": [],
                                        "requiredDuringSchedulingIgnoredDuringExecution": [],
                                    },
                                },
                                "annotations": {
                                    "property1": "string",
                                    "property2": "string",
                                },
                                "configMaps": [{}],
                                "coreLimit": "string",
                                "coreRequest": "string",
                                "cores": 0,
                                "envSecretKeyRefs": {
                                    "property1": {},
                                    "property2": {},
                                },
                                "envVars": {
                                    "property1": "string",
                                    "property2": "string",
                                },
                                "hostAliases": [{"hostnames": []}],
                                "image": "string",
                                "instanceType": "string",
                                "instances": 0,
                                "javaOptions": "string",
                                "labels": {
                                    "property1": "string",
                                    "property2": "string",
                                },
                                "memory": "string",
                                "memoryOverhead": "string",
                                "podSecurityContext": {
                                    "fsGroup": 0,
                                    "runAsGroup": 0,
                                    "runAsNonRoot": True,
                                    "runAsUser": 0,
                                    "seLinuxOptions": {},
                                    "supplementalGroups": [],
                                    "sysctls": [],
                                    "windowsOptions": {},
                                },
                                "secrets": [{}],
                                "securityContext": {
                                    "allowPrivilegeEscalation": True,
                                    "capabilities": {"add": [], "drop": []},
                                    "privileged": True,
                                    "procMount": "string",
                                    "readOnlyRootFilesystem": True,
                                    "runAsGroup": 0,
                                    "runAsNonRoot": True,
                                    "runAsUser": 0,
                                    "seLinuxOptions": {},
                                    "windowsOptions": {},
                                },
                                "spot": True,
                                "tolerations": [{}],
                                "volumeMounts": [{}],
                            },
                            "hadoopConf": {
                                "property1": "string",
                                "property2": "string",
                            },
                            "hadoopConfigMap": "string",
                            "image": "string",
                            "imagePullPolicy": "string",
                            "imagePullSecrets": ["string"],
                            "initContainerImage": "string",
                            "mainApplicationFile": "string",
                            "mainClass": "string",
                            "memoryOverheadFactor": "string",
                            "pythonVersion": "3",
                            "sparkConf": {
                                "property1": "string",
                                "property2": "string",
                            },
                            "sparkConfigMap": "string",
                            "sparkVersion": "string",
                            "timeToLiveSeconds": 0,
                            "type": "Java",
                            "volumes": [
                                {
                                    "awsElasticBlockStore": {},
                                    "azureDisk": {},
                                    "azureFile": {},
                                    "cephfs": {"monitors": []},
                                    "cinder": {},
                                    "configMap": {"items": []},
                                    "csi": {"volumeAttributes": {}},
                                    "downwardAPI": {"items": []},
                                    "emptyDir": {},
                                    "fc": {"targetWWNs": [], "wwids": []},
                                    "flexVolume": {"options": {}},
                                    "flocker": {},
                                    "gcePersistentDisk": {},
                                    "gitRepo": {},
                                    "glusterfs": {},
                                    "hostPath": {},
                                    "iscsi": {"portals": []},
                                    "name": "string",
                                    "nfs": {},
                                    "persistentVolumeClaim": {},
                                    "photonPersistentDisk": {},
                                    "portworxVolume": {},
                                    "projected": {"sources": []},
                                    "quobyte": {},
                                    "rbd": {"monitors": []},
                                    "scaleIO": {},
                                    "secret": {"items": []},
                                    "storageos": {},
                                    "vsphereVolume": {},
                                }
                            ],
                        },
                        "startedAt": "2021-11-18T17:09:37+00:00",
                        "endedAt": "2021-11-18T17:09:37+00:00",
                        "log": {
                            "logsStreamUrl": "/ocean/spark/cluster/osc-20fac3f1/app/daily-reporting-2021-08-18/logs/live",
                            "kubeEventsStreamUrl": "/ocean/spark/cluster/osc-20fac3f1/app/daily-reporting-2021-08-18/kubeEvents/live",
                        },
                        "metrics": {
                            "cost": {
                                "createdAt": "2018-10-10T10:50:29.000+0000",
                                "updatedAt": "2018-10-10T10:50:29.000+0000",
                                "total": 0,
                            },
                            "spark": {
                                "createdAt": "2018-10-10T10:50:29.000+0000",
                                "updatedAt": "2018-10-10T10:50:29.000+0000",
                                "sparkCoresDurationSeconds": 0,
                                "inputDataBytes": 0,
                                "outputDataBytes": 0,
                                "durationSeconds": 0,
                                "efficiencyPercent": 0,
                            },
                        },
                    }
                ],
                "count": 1,
                "kind": "spotinst:ocean:spark:application",
            },
        },
    )


@pytest.fixture(scope="function")
def failed_submission(requests_mock: RequestsMocker) -> None:
    requests_mock.real_http = True
    requests_mock.register_uri(
        "POST",
        re.compile("https://api.spotinst.io/ocean/spark/cluster/.*/app"),
        status_code=400,
        text="Bad Request",
    )


@pytest.fixture(scope="function")
def successful_kill(requests_mock: RequestsMocker) -> None:
    requests_mock.real_http = True
    requests_mock.register_uri(
        "DELETE",
        re.compile("https://api.spotinst.io/ocean/spark/cluster/.*/app"),
        status_code=200,
        json="",
    )


@pytest.fixture(scope="function")
def successful_get_app(requests_mock: RequestsMocker) -> None:
    requests_mock.real_http = True
    requests_mock.register_uri(
        "GET",
        re.compile("https://api.spotinst.io/ocean/spark/cluster/.*/app/.*"),
        status_code=200,
        json={
            "request": {
                "id": "e593ff58-067d-4340-92f9-8b1c0bad70d7",
                "url": "string",
                "method": "string",
                "timestamp": "2018-06-20T11:35:01.745Z",
            },
            "response": {
                "status": {"code": 200, "message": "OK"},
                "items": [
                    {
                        "createdAt": "2018-10-10T10:50:29.000+0000",
                        "updatedAt": "2018-11-01T10:50:29.000+0000",
                        "internalId": "fa61bb92-4bb7-49aa-87d3-7823bd263d1e",
                        "id": "test-app-id",
                        "displayName": "test app name",
                        "userId": 59438,
                        "clusterId": "test-cluster-id",
                        "controllerClusterId": "my-ocean-cluster",
                        "appState": "RUNNING",
                        "submissionSource": "public-api",
                        "job": {
                            "id": "daily-reporting",
                            "displayName": "Daily Reporting",
                        },
                        "config": {
                            "arguments": ["string"],
                            "deps": {
                                "files": ["string"],
                                "jars": ["string"],
                                "pyFiles": ["string"],
                            },
                            "driver": {
                                "affinity": {
                                    "nodeAffinity": {
                                        "preferredDuringSchedulingIgnoredDuringExecution": []
                                    },
                                    "podAffinity": {
                                        "preferredDuringSchedulingIgnoredDuringExecution": [],
                                        "requiredDuringSchedulingIgnoredDuringExecution": [],
                                    },
                                    "podAntiAffinity": {
                                        "preferredDuringSchedulingIgnoredDuringExecution": [],
                                        "requiredDuringSchedulingIgnoredDuringExecution": [],
                                    },
                                },
                                "annotations": {
                                    "property1": "string",
                                    "property2": "string",
                                },
                                "configMaps": [{}],
                                "coreLimit": "string",
                                "coreRequest": "string",
                                "cores": 0,
                                "envSecretKeyRefs": {
                                    "property1": {},
                                    "property2": {},
                                },
                                "envVars": {
                                    "property1": "string",
                                    "property2": "string",
                                },
                                "hostAliases": [{"hostnames": []}],
                                "image": "string",
                                "instanceType": "string",
                                "javaOptions": "string",
                                "labels": {
                                    "property1": "string",
                                    "property2": "string",
                                },
                                "memory": "string",
                                "memoryOverhead": "string",
                                "podName": "string",
                                "podSecurityContext": {
                                    "fsGroup": 0,
                                    "runAsGroup": 0,
                                    "runAsNonRoot": True,
                                    "runAsUser": 0,
                                    "seLinuxOptions": {},
                                    "supplementalGroups": [],
                                    "sysctls": [],
                                    "windowsOptions": {},
                                },
                                "secrets": [{}],
                                "securityContext": {
                                    "allowPrivilegeEscalation": True,
                                    "capabilities": {"add": [], "drop": []},
                                    "privileged": True,
                                    "procMount": "string",
                                    "readOnlyRootFilesystem": True,
                                    "runAsGroup": 0,
                                    "runAsNonRoot": True,
                                    "runAsUser": 0,
                                    "seLinuxOptions": {},
                                    "windowsOptions": {},
                                },
                                "spot": True,
                                "tolerations": [{}],
                                "volumeMounts": [{}],
                            },
                            "executor": {
                                "affinity": {
                                    "nodeAffinity": {
                                        "preferredDuringSchedulingIgnoredDuringExecution": []
                                    },
                                    "podAffinity": {
                                        "preferredDuringSchedulingIgnoredDuringExecution": [],
                                        "requiredDuringSchedulingIgnoredDuringExecution": [],
                                    },
                                    "podAntiAffinity": {
                                        "preferredDuringSchedulingIgnoredDuringExecution": [],
                                        "requiredDuringSchedulingIgnoredDuringExecution": [],
                                    },
                                },
                                "annotations": {
                                    "property1": "string",
                                    "property2": "string",
                                },
                                "configMaps": [{}],
                                "coreLimit": "string",
                                "coreRequest": "string",
                                "cores": 0,
                                "envSecretKeyRefs": {
                                    "property1": {},
                                    "property2": {},
                                },
                                "envVars": {
                                    "property1": "string",
                                    "property2": "string",
                                },
                                "hostAliases": [{"hostnames": []}],
                                "image": "string",
                                "instanceType": "string",
                                "instances": 0,
                                "javaOptions": "string",
                                "labels": {
                                    "property1": "string",
                                    "property2": "string",
                                },
                                "memory": "string",
                                "memoryOverhead": "string",
                                "podSecurityContext": {
                                    "fsGroup": 0,
                                    "runAsGroup": 0,
                                    "runAsNonRoot": True,
                                    "runAsUser": 0,
                                    "seLinuxOptions": {},
                                    "supplementalGroups": [],
                                    "sysctls": [],
                                    "windowsOptions": {},
                                },
                                "secrets": [{}],
                                "securityContext": {
                                    "allowPrivilegeEscalation": True,
                                    "capabilities": {"add": [], "drop": []},
                                    "privileged": True,
                                    "procMount": "string",
                                    "readOnlyRootFilesystem": True,
                                    "runAsGroup": 0,
                                    "runAsNonRoot": True,
                                    "runAsUser": 0,
                                    "seLinuxOptions": {},
                                    "windowsOptions": {},
                                },
                                "spot": True,
                                "tolerations": [{}],
                                "volumeMounts": [{}],
                            },
                            "hadoopConf": {
                                "property1": "string",
                                "property2": "string",
                            },
                            "hadoopConfigMap": "string",
                            "image": "string",
                            "imagePullPolicy": "string",
                            "imagePullSecrets": ["string"],
                            "initContainerImage": "string",
                            "mainApplicationFile": "string",
                            "mainClass": "string",
                            "memoryOverheadFactor": "string",
                            "pythonVersion": "3",
                            "sparkConf": {
                                "property1": "string",
                                "property2": "string",
                            },
                            "sparkConfigMap": "string",
                            "sparkVersion": "string",
                            "timeToLiveSeconds": 0,
                            "type": "Java",
                            "volumes": [
                                {
                                    "awsElasticBlockStore": {},
                                    "azureDisk": {},
                                    "azureFile": {},
                                    "cephfs": {"monitors": []},
                                    "cinder": {},
                                    "configMap": {"items": []},
                                    "csi": {"volumeAttributes": {}},
                                    "downwardAPI": {"items": []},
                                    "emptyDir": {},
                                    "fc": {"targetWWNs": [], "wwids": []},
                                    "flexVolume": {"options": {}},
                                    "flocker": {},
                                    "gcePersistentDisk": {},
                                    "gitRepo": {},
                                    "glusterfs": {},
                                    "hostPath": {},
                                    "iscsi": {"portals": []},
                                    "name": "string",
                                    "nfs": {},
                                    "persistentVolumeClaim": {},
                                    "photonPersistentDisk": {},
                                    "portworxVolume": {},
                                    "projected": {"sources": []},
                                    "quobyte": {},
                                    "rbd": {"monitors": []},
                                    "scaleIO": {},
                                    "secret": {"items": []},
                                    "storageos": {},
                                    "vsphereVolume": {},
                                }
                            ],
                        },
                        "startedAt": "2021-11-18T17:09:37+00:00",
                        "endedAt": "2021-11-18T17:09:37+00:00",
                        "log": {
                            "logsStreamUrl": "/ocean/spark/cluster/osc-20fac3f1/app/daily-reporting-2021-08-18/logs/live",
                            "kubeEventsStreamUrl": "/ocean/spark/cluster/osc-20fac3f1/app/daily-reporting-2021-08-18/kubeEvents/live",
                        },
                        "metrics": {
                            "cost": {
                                "createdAt": "2018-10-10T10:50:29.000+0000",
                                "updatedAt": "2018-10-10T10:50:29.000+0000",
                                "total": 0,
                            },
                            "spark": {
                                "createdAt": "2018-10-10T10:50:29.000+0000",
                                "updatedAt": "2018-10-10T10:50:29.000+0000",
                                "sparkCoresDurationSeconds": 0,
                                "inputDataBytes": 0,
                                "outputDataBytes": 0,
                                "durationSeconds": 0,
                                "efficiencyPercent": 0,
                            },
                        },
                    }
                ],
                "count": 1,
                "kind": "spotinst:ocean:spark:application",
            },
        },
    )


@pytest.fixture(scope="function")
def get_app_completed(requests_mock: RequestsMocker) -> None:
    requests_mock.real_http = True
    requests_mock.register_uri(
        "GET",
        re.compile("https://api.spotinst.io/ocean/spark/cluster/.*/app/.*"),
        status_code=200,
        json={
            "request": {
                "id": "e593ff58-067d-4340-92f9-8b1c0bad70d7",
                "url": "string",
                "method": "string",
                "timestamp": "2018-06-20T11:35:01.745Z",
            },
            "response": {
                "status": {"code": 200, "message": "OK"},
                "items": [
                    {
                        "createdAt": "2018-10-10T10:50:29.000+0000",
                        "updatedAt": "2018-11-01T10:50:29.000+0000",
                        "internalId": "fa61bb92-4bb7-49aa-87d3-7823bd263d1e",
                        "id": "test-app-id",
                        "displayName": "test app name",
                        "userId": 59438,
                        "clusterId": "test-cluster-id",
                        "controllerClusterId": "my-ocean-cluster",
                        "appState": "COMPLETED",
                        "submissionSource": "public-api",
                        "job": {
                            "id": "daily-reporting",
                            "displayName": "Daily Reporting",
                        },
                        "config": {
                            "arguments": ["string"],
                            "deps": {
                                "files": ["string"],
                                "jars": ["string"],
                                "pyFiles": ["string"],
                            },
                            "driver": {
                                "affinity": {
                                    "nodeAffinity": {
                                        "preferredDuringSchedulingIgnoredDuringExecution": []
                                    },
                                    "podAffinity": {
                                        "preferredDuringSchedulingIgnoredDuringExecution": [],
                                        "requiredDuringSchedulingIgnoredDuringExecution": [],
                                    },
                                    "podAntiAffinity": {
                                        "preferredDuringSchedulingIgnoredDuringExecution": [],
                                        "requiredDuringSchedulingIgnoredDuringExecution": [],
                                    },
                                },
                                "annotations": {
                                    "property1": "string",
                                    "property2": "string",
                                },
                                "configMaps": [{}],
                                "coreLimit": "string",
                                "coreRequest": "string",
                                "cores": 0,
                                "envSecretKeyRefs": {
                                    "property1": {},
                                    "property2": {},
                                },
                                "envVars": {
                                    "property1": "string",
                                    "property2": "string",
                                },
                                "hostAliases": [{"hostnames": []}],
                                "image": "string",
                                "instanceType": "string",
                                "javaOptions": "string",
                                "labels": {
                                    "property1": "string",
                                    "property2": "string",
                                },
                                "memory": "string",
                                "memoryOverhead": "string",
                                "podName": "string",
                                "podSecurityContext": {
                                    "fsGroup": 0,
                                    "runAsGroup": 0,
                                    "runAsNonRoot": True,
                                    "runAsUser": 0,
                                    "seLinuxOptions": {},
                                    "supplementalGroups": [],
                                    "sysctls": [],
                                    "windowsOptions": {},
                                },
                                "secrets": [{}],
                                "securityContext": {
                                    "allowPrivilegeEscalation": True,
                                    "capabilities": {"add": [], "drop": []},
                                    "privileged": True,
                                    "procMount": "string",
                                    "readOnlyRootFilesystem": True,
                                    "runAsGroup": 0,
                                    "runAsNonRoot": True,
                                    "runAsUser": 0,
                                    "seLinuxOptions": {},
                                    "windowsOptions": {},
                                },
                                "spot": True,
                                "tolerations": [{}],
                                "volumeMounts": [{}],
                            },
                            "executor": {
                                "affinity": {
                                    "nodeAffinity": {
                                        "preferredDuringSchedulingIgnoredDuringExecution": []
                                    },
                                    "podAffinity": {
                                        "preferredDuringSchedulingIgnoredDuringExecution": [],
                                        "requiredDuringSchedulingIgnoredDuringExecution": [],
                                    },
                                    "podAntiAffinity": {
                                        "preferredDuringSchedulingIgnoredDuringExecution": [],
                                        "requiredDuringSchedulingIgnoredDuringExecution": [],
                                    },
                                },
                                "annotations": {
                                    "property1": "string",
                                    "property2": "string",
                                },
                                "configMaps": [{}],
                                "coreLimit": "string",
                                "coreRequest": "string",
                                "cores": 0,
                                "envSecretKeyRefs": {
                                    "property1": {},
                                    "property2": {},
                                },
                                "envVars": {
                                    "property1": "string",
                                    "property2": "string",
                                },
                                "hostAliases": [{"hostnames": []}],
                                "image": "string",
                                "instanceType": "string",
                                "instances": 0,
                                "javaOptions": "string",
                                "labels": {
                                    "property1": "string",
                                    "property2": "string",
                                },
                                "memory": "string",
                                "memoryOverhead": "string",
                                "podSecurityContext": {
                                    "fsGroup": 0,
                                    "runAsGroup": 0,
                                    "runAsNonRoot": True,
                                    "runAsUser": 0,
                                    "seLinuxOptions": {},
                                    "supplementalGroups": [],
                                    "sysctls": [],
                                    "windowsOptions": {},
                                },
                                "secrets": [{}],
                                "securityContext": {
                                    "allowPrivilegeEscalation": True,
                                    "capabilities": {"add": [], "drop": []},
                                    "privileged": True,
                                    "procMount": "string",
                                    "readOnlyRootFilesystem": True,
                                    "runAsGroup": 0,
                                    "runAsNonRoot": True,
                                    "runAsUser": 0,
                                    "seLinuxOptions": {},
                                    "windowsOptions": {},
                                },
                                "spot": True,
                                "tolerations": [{}],
                                "volumeMounts": [{}],
                            },
                            "hadoopConf": {
                                "property1": "string",
                                "property2": "string",
                            },
                            "hadoopConfigMap": "string",
                            "image": "string",
                            "imagePullPolicy": "string",
                            "imagePullSecrets": ["string"],
                            "initContainerImage": "string",
                            "mainApplicationFile": "string",
                            "mainClass": "string",
                            "memoryOverheadFactor": "string",
                            "pythonVersion": "3",
                            "sparkConf": {
                                "property1": "string",
                                "property2": "string",
                            },
                            "sparkConfigMap": "string",
                            "sparkVersion": "string",
                            "timeToLiveSeconds": 0,
                            "type": "Java",
                            "volumes": [
                                {
                                    "awsElasticBlockStore": {},
                                    "azureDisk": {},
                                    "azureFile": {},
                                    "cephfs": {"monitors": []},
                                    "cinder": {},
                                    "configMap": {"items": []},
                                    "csi": {"volumeAttributes": {}},
                                    "downwardAPI": {"items": []},
                                    "emptyDir": {},
                                    "fc": {"targetWWNs": [], "wwids": []},
                                    "flexVolume": {"options": {}},
                                    "flocker": {},
                                    "gcePersistentDisk": {},
                                    "gitRepo": {},
                                    "glusterfs": {},
                                    "hostPath": {},
                                    "iscsi": {"portals": []},
                                    "name": "string",
                                    "nfs": {},
                                    "persistentVolumeClaim": {},
                                    "photonPersistentDisk": {},
                                    "portworxVolume": {},
                                    "projected": {"sources": []},
                                    "quobyte": {},
                                    "rbd": {"monitors": []},
                                    "scaleIO": {},
                                    "secret": {"items": []},
                                    "storageos": {},
                                    "vsphereVolume": {},
                                }
                            ],
                        },
                        "startedAt": "2021-11-18T17:09:37+00:00",
                        "endedAt": "2021-11-18T17:09:37+00:00",
                        "log": {
                            "logsStreamUrl": "/ocean/spark/cluster/osc-20fac3f1/app/daily-reporting-2021-08-18/logs/live",
                            "kubeEventsStreamUrl": "/ocean/spark/cluster/osc-20fac3f1/app/daily-reporting-2021-08-18/kubeEvents/live",
                        },
                        "metrics": {
                            "cost": {
                                "createdAt": "2018-10-10T10:50:29.000+0000",
                                "updatedAt": "2018-10-10T10:50:29.000+0000",
                                "total": 0,
                            },
                            "spark": {
                                "createdAt": "2018-10-10T10:50:29.000+0000",
                                "updatedAt": "2018-10-10T10:50:29.000+0000",
                                "sparkCoresDurationSeconds": 0,
                                "inputDataBytes": 0,
                                "outputDataBytes": 0,
                                "durationSeconds": 0,
                                "efficiencyPercent": 0,
                            },
                        },
                    }
                ],
                "count": 1,
                "kind": "spotinst:ocean:spark:application",
            },
        },
    )


@pytest.fixture(scope="function")
def get_connection_mock(mocker: MockerFixture) -> unittest.mock.MagicMock:
    mock = mocker.patch(
        "ocean_spark.hooks.OceanSparkHook." "get_connection",
    )
    mock.return_value = Connection(
        conn_id="test-conn-id",
        conn_type="ocean_spark",
        host="test-cluster-id",
        login="account-id",
        password="test-api-key",
    )
    return mock
