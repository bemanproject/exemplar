# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

add_library(beman.{{project-name}} STATIC)
add_library(beman::{{project-name}} ALIAS beman.{{project-name}})

target_sources(beman.{{project-name}} PRIVATE identity.cpp)

target_sources(
    beman.{{project-name}}
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${PROJECT_SOURCE_DIR}/include
        FILES ${PROJECT_SOURCE_DIR}/include/beman/{{project-name}}/identity.hpp
)

set_target_properties(beman.{{project-name}} PROPERTIES VERIFY_INTERFACE_HEADER_SETS ON)

install(
    TARGETS beman.{{project-name}}
    EXPORT beman.{{project-name}}
    DESTINATION
    $<$<CONFIG:Debug>:debug/>${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION $<$<CONFIG:Debug>:debug/>${CMAKE_INSTALL_BINDIR}
    FILE_SET HEADERS DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)
