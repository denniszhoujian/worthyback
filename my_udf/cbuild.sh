
gcc -bundle -o udf_median.so udf_median.cc -I/usr/local/mysql/include/ -m64 -stdlib=libstdc++ -lstdc++

gcc -bundle -o udf_min_ratio.so udf_min_ratio.cc -I/usr/local/mysql/include/ -m64 -stdlib=libstdc++ -lstdc++

gcc -bundle -o udf_LPDR.so udf_LPDR.cc -I/usr/local/mysql/include/ -m64 -stdlib=libstdc++ -lstdc++

gcc -bundle -o udf_percentile_minx.so udf_percentile_minx.cc -I/usr/local/mysql/include/ -m64 -stdlib=libstdc++ -lstdc++