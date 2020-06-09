#include "conv_net.h"
#include "weights.h"
#include "biases.h"
#include <stdio.h>

void lenet_wrapper(DTYPE *shared_mem) {
#pragma HLS INTERFACE m_axi depth = 1034 \
                      port = shared_mem \
                      offset = slave \
                      bundle = memorybus register
#pragma HLS INTERFACE s_axilite port = return \
                      bundle = axilite register

       DTYPE img[IMG_CHANNELS][IMG_DMNIN][IMG_DMNIN];
       DTYPE p[SFMX_SIZE];

       for (uint8_t l = 0; l < IMG_CHANNELS; l++) { // 1
           for (uint8_t r = 0; r < IMG_DMNIN; r++) { // 32
               for (uint8_t c = 0; c < IMG_DMNIN; c++) { // 32
                 img[l][r][c] = (DTYPE)*shared_mem++;
               }
           }
       }

       predict(img,p);

       for (uint8_t i = 0; i < SFMX_SIZE; i++) { // 10
           *shared_mem++ = (float)p[i];
       }
}

void predict(DTYPE img[IMG_CHANNELS][IMG_DMNIN][IMG_DMNIN], DTYPE p[SFMX_SIZE]) {
    DTYPE nml[IMG_CHANNELS][IMG_DMNIN][IMG_DMNIN];
    DTYPE layer1_out[C1_N_FILTERS][C1_OUT_DMNIN][C1_OUT_DMNIN];
    DTYPE layer2_out[C1_N_FILTERS][A1_ROWS][A1_COLS];
    DTYPE layer3_out[C1_N_FILTERS][P1_DOWNSIZE][P1_DOWNSIZE];
    DTYPE layer4_out[C2_N_FILTERS][C2_OUT_DMNIN][C2_OUT_DMNIN];
    DTYPE layer5_out[C2_N_FILTERS][A2_ROWS][A2_COLS];
    DTYPE layer6_out[C2_N_FILTERS][P2_DOWNSIZE][P2_DOWNSIZE];
    DTYPE layer7_out[FLAT_VEC_SZ];
    DTYPE layer8_out[F1_ROWS];
    DTYPE layer9_out[F1_ROWS];
    DTYPE layer10_out[F2_ROWS];
    DTYPE layer11_out[F2_ROWS];
    DTYPE layer12_out[F3_ROWS];

#if NORMALIZED
    convolution_c1(img, weights_C1, layer1_out, biases_C1);
#else
    normalize(img, nml);
    convolution_c1(nml, weights_C1, layer1_out, biases_C1);
#endif
    relu_a1(layer1_out, layer2_out);
    pooling_p1(layer2_out, layer3_out);

    convolution_c2(layer3_out, weights_C2, layer4_out, biases_C2);
    relu_a2(layer4_out, layer5_out);
    pooling_p2(layer5_out, layer6_out);

    flatten(layer6_out, layer7_out);

    vec_mat_mul_f1(layer7_out, weights_F1, biases_F1, layer8_out);
    relu_a3(layer8_out, layer9_out);

    vec_mat_mul_f2(layer9_out, weights_F2, biases_F2, layer10_out);
    relu_a4(layer10_out, layer11_out);

    vec_mat_mul_f3(layer11_out, weights_F3, biases_F3, layer12_out);

#if defined(FIXED_POINT)
    for (uint8_t i = 0; i < SFMX_SIZE; i++) {
        p[i] = layer12_out[i];
    }
#else
    softmax(layer12_out, p);
#endif
}
