function(beman_add_install_test name)
    cmake_parse_arguments(PARSE_ARGV 1 _arg "" "HEADER" "")

    string(TOUPPER "${name}" _pkg_upper)
    string(REPLACE "." "_" _pkg_prefix "${_pkg_upper}")

    if(${_pkg_prefix}_INSTALL_CONFIG_FILE_PACKAGE
       AND NOT CMAKE_SKIP_INSTALL_RULES)

        # Derive target name: beman.exemplar -> beman::exemplar
        string(REPLACE "." "::" _target "${name}")

        # Derive default header: beman.exemplar -> beman/exemplar/exemplar.hpp
        if(_arg_HEADER)
            set(_header "${_arg_HEADER}")
        else()
            string(REPLACE "." "/" _header_path "${name}")
            # Extract last component for the filename.
            string(REGEX REPLACE ".*\\." "" _leaf "${name}")
            set(_header "${_header_path}/${_leaf}.hpp")
        endif()

        # Generate a minimal downstream consumer project at configure time.
        set(_fpt_src_dir "${CMAKE_CURRENT_BINARY_DIR}/find-package-test-src")
        set(_fpt_bin_dir "${CMAKE_CURRENT_BINARY_DIR}/find-package-test-build")

        file(WRITE "${_fpt_src_dir}/CMakeLists.txt"
            "cmake_minimum_required(VERSION 3.25)\n"
            "project(find-package-test LANGUAGES CXX)\n"
            "find_package(${name} REQUIRED)\n"
            "add_executable(main main.cpp)\n"
            "target_link_libraries(main PRIVATE ${_target})\n"
        )
        file(WRITE "${_fpt_src_dir}/main.cpp"
            "#include <${_header}>\n"
            "int main() {}\n"
        )

        # Determine config: for single-config generators, fall back to CMAKE_BUILD_TYPE.
        if(CMAKE_CONFIGURATION_TYPES)
            set(_config_arg "$<CONFIG>")
        elseif(CMAKE_BUILD_TYPE)
            set(_config_arg "${CMAKE_BUILD_TYPE}")
        else()
            set(_config_arg "Release")
        endif()

        add_test(
            NAME install-to-stagedir
            COMMAND
                ${CMAKE_COMMAND} --install ${CMAKE_BINARY_DIR} --prefix
                ${CMAKE_BINARY_DIR}/stagedir --config ${_config_arg}
        )

        # Build the --build-and-test command incrementally.
        set(_fpt_cmd
            ${CMAKE_CTEST_COMMAND}
            --output-on-failure -C ${_config_arg}
            --build-and-test
            "${_fpt_src_dir}"
            "${_fpt_bin_dir}"
            --build-generator ${CMAKE_GENERATOR}
        )

        if(CMAKE_MAKE_PROGRAM)
            list(APPEND _fpt_cmd --build-makeprogram ${CMAKE_MAKE_PROGRAM})
        endif()

        list(APPEND _fpt_cmd
            --build-options
            "-DCMAKE_BUILD_TYPE=${_config_arg}"
            "-DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}"
            "-DCMAKE_CXX_EXTENSIONS=${CMAKE_CXX_EXTENSIONS}"
            "-DCMAKE_CXX_STANDARD=${CMAKE_CXX_STANDARD}"
            "-DCMAKE_PREFIX_PATH=${CMAKE_BINARY_DIR}/stagedir"
        )

        if(CMAKE_TOOLCHAIN_FILE)
            list(APPEND _fpt_cmd "-DCMAKE_TOOLCHAIN_FILE=${CMAKE_TOOLCHAIN_FILE}")
        endif()

        add_test(
            NAME find-package-test
            COMMAND ${_fpt_cmd}
        )
        set_tests_properties(find-package-test PROPERTIES DEPENDS install-to-stagedir)
    endif()
endfunction()
