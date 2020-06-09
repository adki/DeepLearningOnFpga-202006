#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdint.h>
#include <opencv2/opencv.hpp>
using namespace cv;
#if defined(FIXED_POINT)
#include "ap_fixed.h"
#if !defined(DTYPE)
#define DTYPE ap_fixed<32,8>
#endif
#endif

#include "conapi.h"
#include "trx_axi_api.h"

unsigned int card_id=0;
con_Handle_t handle=NULL;

#      define MEM_WRITE(A, B)        BfmWrite(handle, (unsigned int)(A), (unsigned int*)&(B), 4, 1)
#      define MEM_READ(A, B)         BfmRead (handle, (unsigned int)(A), (unsigned int*)&(B), 4, 1)
#      define MEM_WRITE_G(A,D,S,L)   BfmWrite(handle, (A), (D), (S), (L))
#      define MEM_READ_G(A,D,S,L)    BfmRead (handle, (A), (D), (S), (L))

#define NUM_ROWS     32 // IMG_DMNIN
#define NUM_COLS     32 // IMG_DMNIN
#define SIZE_IMG    (NUM_ROWS*NUM_COLS) // num of pixels
#define NUM_CLASSES  10 // SFMX_SIZE
#define ADDR_CSR     0xC0000000
#define ADDR_IMG     0x00000000
#define ADDR_RESULT (ADDR_IMG+4*SIZE_IMG)

int host(char inputFileName[]);
int get_image_data(char inputFileName[], unsigned int greyData[SIZE_IMG]
                  ,int normalize=1, int revert=0);
#if defined(FIXED_POINT)
void softmax(float p[NUM_CLASSES], DTYPE q[NUM_CLASSES]);
#endif
void confmc_info(struct _usb usb, con_MasterInfo_t gpif2mst_info);


int main(int argc, char *argv[])
{
    if (argc!=2) {
        printf("Usage %s input_imapge\n", argv[0]);
        return 0;
    }

    if ((handle=conInit(card_id, CON_MODE_CMD, CONAPI_LOG_LEVEL_INFO))==NULL) {
         printf("cannot initialize CON-FMC\n");
         return 0;
    }
    struct _usb usb;
    conGetUsbInfo( handle, &usb); // Get USB related information
    con_MasterInfo_t gpif2mst_info; // Get GPIF2MST information
    if (conGetMasterInfo(handle, &gpif2mst_info)) {
        printf("cannot get gpif2mst info\n");
        return -1;
    }
    #ifndef SILENCE
    confmc_info(usb, gpif2mst_info);
    #endif //SILENCE

    (void)host(argv[1]);

    return 0;
}

// 1. get image data (gray scale [0-1]
// 2. check IP is ready
// 3. write image data to the IP 
// 4. let IP go and wait for completion
// 5. read results from the IP
// 6. print results
int host(char inputFileName[])
{
    unsigned int greyData[SIZE_IMG]; // note that it carries float bit-pattern
    (void)get_image_data(inputFileName, greyData);
#if defined(FIXED_POINT)
    float *floatPt=(float*)greyData;
    DTYPE greyDataFixed[SIZE_IMG];
    for (int i=0; i<SIZE_IMG; i++) greyDataFixed[i] = (DTYPE)floatPt[i];
    unsigned int greyDataUint[SIZE_IMG];
    for (int i=0; i<SIZE_IMG; i++) greyDataUint[i] = *(unsigned int*)&(greyDataFixed[i]);
#endif

    int ap_idle, ap_idle_r;
    int ap_done, ap_done_r;
    int ap_start, ap_data;
    unsigned int ap_addr;

    ap_addr = ADDR_CSR;
    while (1) {
        MEM_READ(ap_addr, ap_idle_r);
        ap_idle = (ap_idle_r >> 2) && 0x1;
        if (ap_idle)
            break;
    }
    
#if !defined(FIXED_POINT)
    MEM_WRITE_G(ADDR_IMG, &greyData[0], 4, SIZE_IMG);
#else
    MEM_WRITE_G(ADDR_IMG, &greyDataUint[0], 4, SIZE_IMG);
#endif

    ap_addr = ADDR_CSR;
    ap_data = 0x1;
    MEM_WRITE(ap_addr, ap_data);//Start
    while (1) {
        MEM_READ(ap_addr, ap_done_r);
        ap_done = (ap_done_r >> 1) && 0x1;
        if (ap_done) break;
    }

    float resultClasses[NUM_CLASSES];
    MEM_READ_G(ADDR_RESULT, (unsigned int*)&resultClasses[0], 4, NUM_CLASSES);
#if defined(FIXED_POINT)
    // carry out softmax, which is not implemented in RTL
    DTYPE resultFixed[NUM_CLASSES];
    for (int i=0; i<NUM_CLASSES; i++) resultFixed[i] = *(DTYPE *)&(resultClasses[i]);
    softmax(resultClasses, resultFixed);
#endif

    printf("    The probabilities of the digit being 0~9 are:\n");
    float maxVal=0.0;
    int   maxId=0;
    for (int i = 0; i < NUM_CLASSES; i++) {
        float val = *(float*)&resultClasses[i];
        if (maxVal<val) {
            maxVal = val;
            maxId  = i;
        }
    }
    for (int i = 0; i < NUM_CLASSES; i++) {
        float result = *(float*)&resultClasses[i];
        printf("        %d:  %f %s\n", i, result, (i==maxId) ? "*" : "");
    }

    return 0;
}

#if defined(FIXED_POINT)
void softmax(float p[NUM_CLASSES], DTYPE q[NUM_CLASSES])
{
     float denom=0.0f;
     for (int i=0; i<NUM_CLASSES; i++) {
        float fval = (float)q[i];
        denom += exp(fval);
     }
     for (int i=0; i<NUM_CLASSES; i++) {
        float fval = (float)q[i];
        p[i] = exp(fval)/denom;
     }
}
#endif

// 1. Reads image data
// 2. Converts grey scale using color-space conversion RGB to Luminance
// 3. Carries out normalization
// 4. Cast floating to unsigned int without modify bit-pattern
int get_image_data(char inputFileName[], unsigned int greyData[SIZE_IMG]
                  ,int normalize,int revert)
{
    FILE *fin;
#ifndef USE_OPENCV
    float tologic[SIZE_IMG]; // 32x32
    fin = fopen(inputFileName, "r");
    if ((fin==NULL)) {
        printf("Could not open input file.\n");
        exit(0);
    }
    for (i = 0; i < SIZE_IMG; i++) {
        fscanf(fin, "%f\n", &tologic[i]);
        greyData[i] = *(unsigned int*)&tologic[i];
    }
    fclose(fin);
#else // #ifndef USE_OPENCV
  #if 1
  /// Load an image
  cv::Mat image = cv::imread( inputFileName, IMREAD_GRAYSCALE );
  #if defined(DEBUG)
  printf("%s() size of element: %d-byte\n", __func__, (int)image.elemSize());
  printf("%s() depth          : %d\n", __func__, image.depth());
  printf("%s() type           : %d\n", __func__, image.type());
  #endif

  int nRows = image.rows; // height
  int nCols = image.cols; // width

  if ((nRows!=NUM_ROWS)||(nCols!=NUM_COLS)) {
      // this may not work properly
      cv::resize(image, image, cv::Size(NUM_COLS,NUM_ROWS), 0, 0, CV_INTER_AREA);
  }
 
  /// Convert to gray
  float fGray = 0.0f;
  float tdata[SIZE_IMG];
  float scale_min = -0.3635f;
  float scale_max = 3.2558f;
 
  for( int j = 0 ; j < nRows ; j++ ) {
    for( int i = 0 ; i < nCols ; i++ ) { // normaization: make [0-1]
      fGray = image.at<uchar>(j,i);
      tdata[(j*NUM_COLS)+i] = (fGray / 255.0)*(scale_max - scale_min) + scale_min;
    }
  }
  for( int i = 0 ; i < SIZE_IMG ; i++ ) {
      greyData[i]= *(unsigned int*)&tdata[i];
  }
  #else
  /// Load an image
  cv::Mat image = cv::imread( inputFileName, IMREAD_COLOR);

  int nRows = image.rows;
  int nCols = image.cols;

  if ((nRows!=NUM_ROWS)||(nCols!=NUM_COLS)) {
      // this may not work properly
      cv::resize(image, image, cv::Size(NUM_COLS,NUM_ROWS), 0, 0, CV_INTER_AREA);
  }
 
  /// Convert to gray
  float fGray = 0.0f;
  float chBlue, chGreen, chRed;
  float tdata[SIZE_IMG];
  float scale_min = -0.3635f;
  float scale_max = 3.2558f;
  //  float scale_min = -1.0000f;
  //  float scale_max = 1.0000f;
 
  for( int j = 0 ; j < nRows ; j++ ) {
    for( int i = 0 ; i < nCols ; i++ ) {
      chBlue  = (float)( image.at<cv::Vec3b>(j,i)[0] );
      chGreen = (float)( image.at<cv::Vec3b>(j,i)[1] );
      chRed = (float)( image.at<cv::Vec3b>(j,i)[2] );
      fGray = 0.2126f * chRed + 0.7152f * chGreen + 0.0722f * chBlue;
      // normaization: make [0-1]
      tdata[(j*NUM_COLS)+i] = (fGray / 255.0)*(scale_max - scale_min) + scale_min;
    }
  }
  for( int i = 0 ; i < SIZE_IMG ; i++ ) {
      greyData[i]= *(unsigned int*)&tdata[i];
  }
  #endif
#endif // #ifndef USE_OPENCV
  return 0;
}

void confmc_info(struct _usb usb, con_MasterInfo_t gpif2mst_info)
{
    printf("USB information\n");
    printf("    DevSpeed         =%d%cbps\n", (usb.speed>10000) ? usb.speed/10000
                                                                : usb.speed/10
                                            , (usb.speed>10000) ? 'G' : 'M');
    printf("    BulkMaxPktSizeOut=%d\n", usb.bulk_max_pkt_size_out);
    printf("    BulkMaxPktSizeIn =%d\n", usb.bulk_max_pkt_size_in );
    printf("    IsoMaxPktSizeOut =%d\n", usb.iso_max_pkt_size_out );
    printf("    IsoMaxPktSizeIn  =%d\n", usb.iso_max_pkt_size_in  );
    fflush(stdout);

    printf("gpif2mst information\n");
    printf("         version 0x%08X\n", gpif2mst_info.version);
    printf("         pclk_freq %d-Mhz (%s)\n", gpif2mst_info.clk_mhz
                                               , (gpif2mst_info.clk_inv)
                                               ? "inverted"
                                               : "not-inverted");
    printf("         DepthCu2f=%d, DepthDu2f=%d, DepthDf2u=%d\n"
                                 , gpif2mst_info.depth_cmd
                                 , gpif2mst_info.depth_u2f
                                 , gpif2mst_info.depth_f2u);
    fflush(stdout);
}
