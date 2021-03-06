import gzip
import io

import docker

from .api_test import DockerClientTest


class BuildTest(DockerClientTest):
    def test_build_container(self):
        script = io.BytesIO('\n'.join([
            'FROM busybox',
            'MAINTAINER docker-py',
            'RUN mkdir -p /tmp/test',
            'EXPOSE 8080',
            'ADD https://dl.dropboxusercontent.com/u/20637798/silence.tar.gz'
            ' /tmp/silence.tar.gz'
        ]).encode('ascii'))

        self.client.build(fileobj=script)

    def test_build_container_pull(self):
        script = io.BytesIO('\n'.join([
            'FROM busybox',
            'MAINTAINER docker-py',
            'RUN mkdir -p /tmp/test',
            'EXPOSE 8080',
            'ADD https://dl.dropboxusercontent.com/u/20637798/silence.tar.gz'
            ' /tmp/silence.tar.gz'
        ]).encode('ascii'))

        self.client.build(fileobj=script, pull=True)

    def test_build_container_stream(self):
        script = io.BytesIO('\n'.join([
            'FROM busybox',
            'MAINTAINER docker-py',
            'RUN mkdir -p /tmp/test',
            'EXPOSE 8080',
            'ADD https://dl.dropboxusercontent.com/u/20637798/silence.tar.gz'
            ' /tmp/silence.tar.gz'
        ]).encode('ascii'))

        self.client.build(fileobj=script, stream=True)

    def test_build_container_custom_context(self):
        script = io.BytesIO('\n'.join([
            'FROM busybox',
            'MAINTAINER docker-py',
            'RUN mkdir -p /tmp/test',
            'EXPOSE 8080',
            'ADD https://dl.dropboxusercontent.com/u/20637798/silence.tar.gz'
            ' /tmp/silence.tar.gz'
        ]).encode('ascii'))
        context = docker.utils.mkbuildcontext(script)

        self.client.build(fileobj=context, custom_context=True)

    def test_build_container_custom_context_gzip(self):
        script = io.BytesIO('\n'.join([
            'FROM busybox',
            'MAINTAINER docker-py',
            'RUN mkdir -p /tmp/test',
            'EXPOSE 8080',
            'ADD https://dl.dropboxusercontent.com/u/20637798/silence.tar.gz'
            ' /tmp/silence.tar.gz'
        ]).encode('ascii'))
        context = docker.utils.mkbuildcontext(script)
        gz_context = gzip.GzipFile(fileobj=context)

        self.client.build(
            fileobj=gz_context,
            custom_context=True,
            encoding="gzip"
        )

    def test_build_remote_with_registry_auth(self):
        self.client._auth_configs = {
            'https://example.com': {
                'user': 'example',
                'password': 'example',
                'email': 'example@example.com'
            }
        }

        self.client.build(path='https://github.com/docker-library/mongo')

    def test_build_container_with_named_dockerfile(self):
        self.client.build('.', dockerfile='nameddockerfile')

    def test_build_container_with_container_limits(self):
        self.client.build('.', container_limits={
            'memory': 1024 * 1024,
            'cpusetcpus': 1,
            'cpushares': 1000,
            'memswap': 1024 * 1024 * 8
        })

    def test_build_container_invalid_container_limits(self):
        self.assertRaises(
            docker.errors.DockerException,
            lambda: self.client.build('.', container_limits={
                'foo': 'bar'
            })
        )
