#include <getopt.h>
#include "tiny_dnn/tiny_dnn.h"

using namespace std;
using namespace tiny_dnn;

int main(int argc, char *argv[])
{
    extern int get_args(int argc, char *argv[]);
    if (get_args(argc, argv)!=0) return -1;

    network<sequential> net("XOR");
    net.load("xor_net");

    vec_t in = {(float_t)atof(argv[1]), (float_t)atof(argv[2])};
    vec_t result = net.predict(in);

    cout << result.at(0) << " ==> "
         << ((result.at(0)>0.05) ? "1" :"0")
         << endl;

#ifdef VERBOSE
    // save outputs of each layer
    for (size_t i; i<net.layer_size(); i++ ) {
         cout << "LAYER == " << i << " ==" << endl;
         cout << "num of incoming edges of layer: " << net[i]->in_channels() << endl;
         cout << "num of outgoing edges of layer: " << net[i]->out_channels() << endl;
         cout << "in  data size         of layer: " << net[i]->in_data_size() << endl;
         cout << "out data size         of layer: " << net[i]->out_data_size() << endl;
        //vec_t w = net[i]->weights();
        //for (auto x : net[i]->weights()) {
        //     cout << "weight " << x->at(0) << " " << x->at(1) << endl;
        //}
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
                 printf("   -h         : help\n");
                 printf("   value_pair : a pair of two values, e.g., 1 0\n");
                 exit(0);
                 break;
       }
    }
    if (argc!=3) {
        cout << argv[0] << " needs two arguments: " << argv[0] << " 0 0" << endl;
        exit(0);
    }
     return 0;
}
