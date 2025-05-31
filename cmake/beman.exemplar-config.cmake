include(${CMAKE_CURRENT_LIST_DIR}/beman.exemplar-targets.cmake)

foreach(comp IN LISTS beman.exemplar_FIND_COMPONENTS)
    if(beman.exemplar_FIND_REQUIRED_${comp})
        set(beman.exemplar_FOUND FALSE)
        return()
    endif()
endforeach()
