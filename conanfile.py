from conans import ConanFile, CMake, tools
import os


class sqlpp11Conan(ConanFile):
    name = 'sqlpp11-connector-mysql'
    version = '0.20'
    license = 'BSD 2-Clause License'
    url = 'https://github.com/csboling/conan-sqlpp11-connector-mysql'
    requires = 'sqlpp11/0.38@memsharded/testing'

    def source(self):
        self.run('git clone https://github.com/rbock/sqlpp11-connector-mysql')
        self.run('cd sqlpp11-connector-mysql && git checkout 0.20')

    def package(self):
        self.copy('*.h', dst='include/sqlpp11/mysql', src='include/sqlpp11/mysql')
