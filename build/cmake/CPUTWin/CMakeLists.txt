SET(EXE_NAME CPUTWin)

SET(CPUTWIN_SOURCE_FILES
	${CPUT_PROJECT_DIR}/src/tools/win/CPU-T.cpp
)

SET(CPUTWIN_HEADER_FILES
	${CPUT_PROJECT_DIR}/src/tools/win/resource.h
)

SET(CPUTWIN_RESOURCE_FILES
	${CPUT_PROJECT_DIR}/src/tools/win/CPU-T.rc
)

SOURCE_GROUP("Source Files" FILES ${CPUTWIN_SOURCE_FILES})
SOURCE_GROUP("Header Files" FILES ${CPUTWIN_HEADER_FILES})
SOURCE_GROUP("Resource Files" FILES ${CPUTWIN_RESOURCE_FILES})

INCLUDE_DIRECTORIES(${CPUT_PROJECT_DIR}/include)
LINK_DIRECTORIES(${CPUT_PROJECT_DIR}/lib/${CPUT_PLATFORM_NAME})

ADD_EXECUTABLE(${EXE_NAME} WIN32
	${CPUTWIN_SOURCE_FILES} ${CPUTWIN_HEADER_FILES} ${CPUTWIN_RESOURCE_FILES}
)
ADD_DEPENDENCIES(${EXE_NAME} CPUTSDK)

SET_TARGET_PROPERTIES(${EXE_NAME} PROPERTIES
	PROJECT_LABEL ${EXE_NAME}
	DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX}
	OUTPUT_NAME ${EXE_NAME}_${CPUT_COMPILER_NAME}${CPUT_COMPILER_VERSION}_${CPUT_ARCH_NAME}
)

TARGET_LINK_LIBRARIES(${EXE_NAME}
	debug CPUTSDK_${CPUT_COMPILER_NAME}${CPUT_COMPILER_VERSION}_${CPUT_ARCH_NAME}${CMAKE_DEBUG_POSTFIX}
	optimized CPUTSDK_${CPUT_COMPILER_NAME}${CPUT_COMPILER_VERSION}_${CPUT_ARCH_NAME}
)


ADD_POST_BUILD(${EXE_NAME} "")


INSTALL(TARGETS ${EXE_NAME}
    RUNTIME DESTINATION ${CPUT_BIN_DIR}
    LIBRARY DESTINATION ${CPUT_BIN_DIR}
    ARCHIVE DESTINATION ${CPUT_OUTPUT_DIR}
)

CPUT_CREATE_VCPROJ_USERFILE(${EXE_NAME})
