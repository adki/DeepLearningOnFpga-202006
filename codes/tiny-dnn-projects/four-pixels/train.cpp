// ref: https://www.youtube.com/watch?v=ILsA4nyG7I0
// Four pixel problem

//#include <iostream>
//#include <sstream>
//#include <string>
//#include <memory>
//#include <chrono>
#include <getopt.h>
#include "tiny_dnn/tiny_dnn.h"

using namespace tiny_dnn;
//using namespace tiny_dnn::activation;
//using namespace tiny_dnn::layers;

using namespace std;

size_t  batch_size = 1;
size_t  epochs     = 10000; // num of iteration
char    weight[128]="pixel_net";
char    json[128]="pixel_net_json";

int main(int argc, char *argv[])
{
    extern int get_args(int argc, char *argv[]);
    if (get_args(argc, argv)!=0) return -1;

    network<sequential> net("Four Pixels");
    net << layers::fc(4,4) << activation::sigmoid()
        << layers::fc(4,4) << activation::sigmoid()
        << layers::fc(4,8) << activation::relu()
        << layers::fc(8,4) << activation::tanh();

    vector<vec_t> input_data  { {0,0, 0,0}, // solid
                                {1,1, 1,1}, // solid
                                {1,0, 1,0}, // vertical
                                {0,1, 0,1}, // vertical
                                {1,0, 0,1}, // diagonal
                                {0,1, 1,0}, // diagonal
                                {1,1, 0,0}, // horizontal
                                {0,0, 1,1}};// horizontal
    vector<vec_t> desired_out { {1,0,0,0}, // solid
                                {1,0,0,0}, // solid
                                {0,1,0,0}, // vertical
                                {0,1,0,0}, // vertical
                                {0,0,1,0}, // diagonal
                                {0,0,1,0}, // diagonal
                                {0,0,0,1}, // horizontal
                                {0,0,0,1}};// horizontal
    gradient_descent opt; // optimizer algorithm

    // Train net using command 'fit', which deals with fitting problem.
    // Use 'train' command for classification problem.
    net.fit<mse>(opt, input_data, desired_out, batch_size, epochs);
  //net.train<mse>(opt, input_data, desired_out, batch_size, epochs);

    // Figure out how good the net is.
    float_t loss = net.get_loss<mse>(input_data, desired_out);
    cout << "mse : " << loss << endl;

    // Save our result as 'pixel_net'.
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
