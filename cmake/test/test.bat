"%1" -S "%2" -B "%3" ^
       -DCMAKE_PREFIX_PATH="%4" ^
       -DCMAKE_BUILD_TYPE="%5" ^
       -DCMAKE_CXX_STANDARD=17

"%1" --build "%3" --config "%5"
