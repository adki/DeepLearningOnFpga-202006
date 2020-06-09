//#include <cstdlib>
#include <getopt.h>
#include "tiny_dnn/tiny_dnn.h"

using namespace std;
using namespace tiny_dnn;

int main(int argc, char *argv[])
{
    extern int get_args(int argc, char *argv[]);
    if (get_args(argc, argv)!=0) return -1;

    network<sequential> net("Four Pixels");
    net.load("pixel_net");

    vec_t in = {(float_t)atof(argv[1]),
                (float_t)atof(argv[2]),
                (float_t)atof(argv[3]),
                (float_t)atof(argv[4])};
    vec_t result = net.predict(in);
    float_t sum = 0;
    for (auto& n : result) sum += n;

#if 1
    string val[] = { "solid", "vertical", "diagonal", "horizontal"};
    for (int i=0; i<4; i++) {
         cout << "[" << val[i] << "] " << result[i] << endl;
    }
    cout << "sum: " << sum << endl;
#else
    // list highest first
    std::vector<std::pair<float_t, int>> scores;
    for (int i=0; i<4; i++) {
         scores.emplace_back(result[i], i);
    }
    sort(scores.begin(), scores.end(), std::greater<std::pair<float_t, int>>());

    string val[] = { "solid", "vertical", "diagonal", "horizontal"};
    for (int i=0; i<4; i++) {
         cout << "[" << setw(10) << left << val[scores[i].second] << "] " << scores[i].first << endl;
    }
#endif

    return 0;
}

int get_args(int argc, char *argv[])
{
    int option;
    optind = 1;
    while ((option=getopt(argc, argv, "h"))!=-1) {
       switch (option&0xFF) {
       case 'h':
       default : printf("%s [options] value_pair\n", argv[0]);
                 printf("   -h        : help\n");
                 printf("   values    : four values, e.g., 0 1 1 0\n");
                 printf("               from upper-left to lower-right\n");
                 exit(0);
                 break;
       }
    }
    if (argc!=5) {
        cout << argv[0] << " needs four arguments: " << argv[0] << " 0 0 0 0" << endl;
        exit(0);
    }
     return 0;
}

