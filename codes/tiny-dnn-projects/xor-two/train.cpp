// XOR problem
// X Y ==> X^Y
// 0 0     0
// 0 1     1
// 1 0     1
// 1 1     0

#include <getopt.h>
#include "tiny_dnn/tiny_dnn.h"

using namespace std;
using namespace tiny_dnn;

size_t  batch_size=1;
size_t  epochs    =3000; // num of iterations
char    weight[128]="xor_net";
char    json[128]="xor_net_json";

int main(int argc, char *argv[])
{
    extern int get_args(int argc, char *argv[]);
    if (get_args(argc, argv)!=0) return -1;

    network<sequential> net("XOR net");
    net << layers::fc(2,2) << activation::tanh()
        << layers::fc(2,1) << activation::tanh();
           // layers: two fully-connected nets
           // activation function: tan hyperbolic
           //
           //  X -->()  ()
           //                () --> x^Y
           //  Y -->()  ()
           //

    vector<vec_t> input_data  { {0,0}, {0,1}, {1,0}, {1,1} };
    vector<vec_t> desired_out { {  0}, {  1}, {  1}, {  0} };

    gradient_descent opt; // optimizer algorithm

    // Train net using command 'fit', which deals with fitting problem.
    // Use 'train' command for classification problem.
    net.fit<mse>(opt, input_data, desired_out, batch_size, epochs);

    // Figure out how good the net is.
    double loss = net.get_loss<mse>(input_data, desired_out);
    cout << "mse : " << loss << endl;

    // Save our result as 'xor_net'.
    net.save(weight);
    net.save(json, content_type::weights_and_model, file_format::json);
    return 0;
}

int get_args(int argc, char *argv[])
{
     int option;
     optind = 1;
     while ((option=getopt(argc, argv, "b:e:w:h"))!=-1) {
        switch (option&0xFF) {
        case 'b': batch_size = (size_t)atoll(optarg);
                  break;
        case 'e': epochs = (size_t)atoll(optarg);
                  break;
        case 'w': strcpy(weight, optarg);
                  sprintf(json, "%s_json", optarg);
                  break;
        case 'h':
        default : printf("%s [options]\n", argv[0]);
                  printf("   -b batch_size   : Batch size (%zu)\n", batch_size);
                  printf("   -e iterations   : Num of iterations (%zu)\n", epochs);
                  printf("   -w file_name    : Weight file (%s)\n", weight);
                  printf("   -h              : help\n");
                  exit(0);
                  break;
        }
     }
     return 0;
}
