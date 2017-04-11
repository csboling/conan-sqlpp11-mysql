from conans import ConanFile, CMake
from conans.tools import replace_in_file

class sqlpp11Conan(ConanFile):
    name = 'sqlpp11-connector-mysql'
    version = '1.0'
    license = 'BSD'
    generators = 'cmake'
    settings = 'os', 'compiler', 'build_type', 'arch'
    requires = 'libmariadb/2.3.1@csboling/conan-libmariadb'
    short_paths = True

    def source(self):
        self.run('git clone https://github.com/rbock/sqlpp11')
        self.run('git clone https://github.com/rbock/sqlpp11-connector-mysql')
        self.run('git clone https://github.com/howardhinnant/date')
        replace_in_file(
            'sqlpp11-connector-mysql/CMakeLists.txt',
            'set(CMAKE_CXX_STANDARD 11)',
            '''
set(CMAKE_CXX_STANDARD 11)
include(${CMAKE_BINARY_DIR}/../../conanbuildinfo.cmake)
conan_basic_setup()
'''
        )

        replace_in_file(
            'sqlpp11-connector-mysql/cmake/FindMySql.cmake',
            'NAMES mysqlclient mysqlclient_r',
            'NAMES mariadb PATHS ${CONAN_LIB_DIRS_LIBMARIADB}'
        )
        replace_in_file(
            'sqlpp11-connector-mysql/cmake/FindMySql.cmake',
            'PATH_SUFFIXES mysql',
            'PATH_SUFFIXES mysql include'
        )


    def build(self):
        cmake = CMake(self.settings)
        self.run('cd sqlpp11-connector-mysql && mkdir build && cd build && cmake .. %s' % (cmake.command_line,))
        self.run('cd sqlpp11-connector-mysql/build && cmake --build . %s' % cmake.build_config)

    def package(self):
        self.copy('*.h', dst='include', src='date')
        self.copy('*.h', dst='include/sqlpp11', src='sqlpp11/include/sqlpp11')
        self.copy('*.h', dst='include/sqlpp11', src='sqlpp11-connector-mysql/include/sqlpp11')
        self.copy('*.lib', dst='lib', src='sqlpp11-connector-mysql', keep_path=False)
        self.copy('*.a', dst='lib', src='sqlpp11-connector-mysql', keep_path=False)
        self.copy('*.so*', dst='lib', src='sqlpp11-connector-mysql', keep_path=False)
        self.copy('*.so*', dst='bin', src='sqlpp11-connector-mysql', keep_path=False)


    def package_info(self):
        self.cpp_info.libs = ['sqlpp-mysql']
