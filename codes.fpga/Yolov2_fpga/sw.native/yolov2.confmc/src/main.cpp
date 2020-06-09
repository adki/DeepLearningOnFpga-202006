
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <math.h>
#include <fcntl.h>
#include <string.h>
#include <time.h>
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <signal.h>
#include <libgen.h>
#include <errno.h>
#if defined(_MSC_VER)
#include "my_getopt.h"
#else
#include <getopt.h>
#endif
#include <termios.h>

#ifdef USE_CON_FMC
#include "conapi.h"
#include "trx_axi_api.h"
unsigned int card_id=0;
con_Handle_t handle=NULL;
#endif

#include "yolov2.h"

static void get_info_confmc(struct _usb usb, con_MasterInfo_t gpif2mst_info);

int  camera_mode=0;
struct termios initial_settings;

char *fname_config   = const_cast<char*>("params/yolov2.cfg");
char *fname_bias     = const_cast<char*>("params/biasv2_comb_ap16.bin");
char *fname_weight   = const_cast<char*>("params/weightsv2_comb_reorg_ap16.bin");
char *result_files   = const_cast<char*>("predictions.png");
char *captured_files = const_cast<char*>("captured_image.jpg");

#define NUM_OF_IMAGE_FILES 5
const char *image_files[] = {
       "images/dog.jpg"
     , "images/eagle.jpg"
     , "images/giraffe.jpg"
     , "images/horses.jpg"
     , "images/person.jpg"
     , ""
};

int main( int argc, char *argv[])
{
    extern int  arg_parser(int, char **);
    if (arg_parser(argc, argv)) return 1;

    unsigned int WEIGHT_BASE = 0x10000000;
    unsigned int BETA_BASE = 0x1C25F000;
    unsigned int MEM_BASE  = 0x1C26A000;// 49770*1024*4 = 203857920 = C26A000

    #ifdef USE_CON_FMC
    if ((handle=conInit(card_id, CON_MODE_CMD, CONAPI_LOG_LEVEL_INFO))==NULL) {
         printf("cannot initialize CON-FMC\n");
         return 0;
    }
    // Get USB related information
    struct _usb usb;
    conGetUsbInfo( handle, &usb);
    // Get GPIF2MST information
    con_MasterInfo_t gpif2mst_info;
    if (conGetMasterInfo(handle, &gpif2mst_info)) {
        printf("cannot get gpif2mst info\n");
        return 0;
    }
    #ifndef SILENCE
    get_info_confmc(usb, gpif2mst_info);
    #endif
    #endif //CON_FMC

    printf("YOLOv2 TEST Begin\n");
    char **names = get_labels(const_cast<char*>("params/coco.names"));

    #ifndef SILENCE
    int x;
    for (x=0;x<80;x++) { //80 classe labels
        printf("[%d]%s\n",x,names[x]);
    }
    #endif //SILENCE
    image **alphabet = load_alphabet();
    network *net = load_network(fname_config, fname_weight, 0);
    set_batch_network(net, 1);

    #ifdef USE_CON_FMC
    unsigned int w_cnt = 203767168/4;
    unsigned int b_cnt = 43048/4;
    FILE *fp_weight = NULL;
    FILE *fp_bias = NULL;
    unsigned int *wbuf = (unsigned int*)malloc( w_cnt * sizeof(unsigned int*) );
    unsigned int *bbuf = (unsigned int*)malloc( b_cnt * sizeof(unsigned int*) );
    
    fp_weight = fopen(fname_weight, "rb");
    fp_bias = fopen(fname_bias, "rb");
    if ( (fp_weight==NULL) | (fp_bias==NULL) ) {
        printf("Could not open weights or bias.\n");
        exit(0);
    }
    if (fread(wbuf, sizeof(unsigned int), w_cnt, fp_weight)!=w_cnt) {
    }
    if (fread(bbuf, sizeof(unsigned int), b_cnt, fp_bias)!=b_cnt) {
    }
    
    unsigned int tcnt = w_cnt / burst_cnt;
    unsigned int trem = w_cnt % burst_cnt;
    unsigned int waddr;
    int i;
    
    for (i=0;i<tcnt;i++) {
        waddr = WEIGHT_BASE + (i*4*burst_cnt);
        MEM_WRITE_G(waddr, &wbuf[i*burst_cnt], 4, burst_cnt);
    }
    if (trem!=0) {
        waddr = WEIGHT_BASE + (tcnt*4*burst_cnt);
        MEM_WRITE_G(waddr, &wbuf[tcnt*burst_cnt], 4, trem);
    }

    #ifdef DEBUG_CONFMC
    unsigned int *rbuf = (unsigned int*) malloc(sizeof(unsigned int) * w_cnt);
    for (i=0;i<tcnt;i++) {
        waddr = WEIGHT_BASE + (i*4*burst_cnt);
        MEM_READ_G(waddr, &rbuf[i*burst_cnt], 4, burst_cnt);
    }
    if (trem!=0) {
        waddr = WEIGHT_BASE + (tcnt*4*burst_cnt);
        MEM_READ_G(waddr, &rbuf[tcnt*burst_cnt], 4, trem);
    }
    
    int cmp_result = memcmp((void *)wbuf, (void *)rbuf, w_cnt);
    printf("weight compare = %d \n", cmp_result);        
    for (i=0;i<w_cnt/4;i++) {
        if (wbuf[i]!=rbuf[i]) printf("0x%x, 0x%x \n", wbuf[i], rbuf[i]);
    }
    #endif //DEBUG_CONFMC

    tcnt = b_cnt / burst_cnt;
    trem = b_cnt % burst_cnt;
    
    for (i=0;i<tcnt;i++) {
        waddr = BETA_BASE + (i*4*burst_cnt);
        MEM_WRITE_G(waddr, &bbuf[i*burst_cnt], 4, burst_cnt);
    }
    if (trem!=0) {
        waddr = BETA_BASE + (tcnt*4*burst_cnt);
        MEM_WRITE_G(waddr, &bbuf[tcnt*burst_cnt], 4, trem);
    }

    #ifdef DEBUG_CONFMC
    unsigned int *cbuf = (unsigned int*) malloc(sizeof(unsigned int) * b_cnt);
    for (i=0;i<tcnt;i++) {
        waddr = BETA_BASE + (i*4*burst_cnt);
        MEM_READ_G(waddr, &cbuf[i*burst_cnt], 4, burst_cnt);
    }
    if (trem!=0) {
        waddr = BETA_BASE + (tcnt*4*burst_cnt);
        MEM_READ_G(waddr, &cbuf[tcnt*burst_cnt], 4, trem);
    }
    
    cmp_result = memcmp((void *)bbuf, (void *)cbuf, b_cnt);
    printf("bias compare = %d \n", cmp_result);        
    for (i=0;i<b_cnt/4;i++) {
        if (bbuf[i]!=cbuf[i]) printf("0x%x, 0x%x \n", bbuf[i], cbuf[i]);
    }
    #endif //DEBUG_CONFMC

    free(wbuf);    
    free(bbuf);    
    #ifdef DEBUG_CONFMC
    free(rbuf);    
    free(cbuf);    
    #endif //DEBUG_CONFMC
    #endif //CON_FMC

    //load_weights_hls(net, "yolov2.weights", 0, net->n);//write weight to file
    ////////////////////load img resize img begin
    char buff[256];
    char *input_imgfn = buff;

    int xx = 0;
    strncpy(input_imgfn, image_files[xx], 256);

    cv::Mat img_now;
    cv::Mat img_res;
    cv::Mat img_con;
    cv::VideoCapture cap(0);

    if (camera_mode) {
        if (!cap.isOpened()) 
        printf("Can not find USB camera \n");
        cap >> img_now;
        img_res = cv::imread(result_files, CV_LOAD_IMAGE_COLOR);

        //cv::hconcat(img_now, img_res, img_con);
        cv::namedWindow("Image", cv::WINDOW_AUTOSIZE);
        cv::imshow("Image", img_now);

    } else {
        img_now = cv::imread(input_imgfn, CV_LOAD_IMAGE_COLOR);

        cv::namedWindow("Image", cv::WINDOW_AUTOSIZE);
        cv::imshow("Image", img_now);
    }

    while (1) {
        printf("Input img:%s\n",input_imgfn);
        if (camera_mode) {
            cap >> img_now;
            cv::imwrite(captured_files, img_now);
            img_res = cv::imread(result_files, CV_LOAD_IMAGE_COLOR);
            //cv::hconcat(img_now, img_res, img_con);
            cv::imshow("Image", img_res);
            if (cv::waitKey(100)==27) { break;}
            strncpy(input_imgfn, captured_files, 256);
        } else {
            strncpy(input_imgfn, image_files[xx], 256);
            img_now = cv::imread(input_imgfn, CV_LOAD_IMAGE_COLOR);
            cv::imshow("Image", img_now);
            if (cv::waitKey(100)==27) { break;}
        }
        image im = load_image_stb(input_imgfn, 3);//3 channel img
        printf("img w=%d,h=%d,c=%d\n",im.w,im.h,im.c);
        image sized = letterbox_image(im, 416, 416);
        save_image_png(sized, "sized");// convert to yolov3 net input size 416x416x3
        ////////////////////load img resize img end
        double time;
        layer l = net->layers[net->n-1];
        float *X = sized.data;
        time = what_time_is_it_now();
        yolov2_hls_ps(net, X, WEIGHT_BASE,BETA_BASE,MEM_BASE);
        printf("Predicted in %f seconds.\n",what_time_is_it_now()-time);
        
        time = what_time_is_it_now();
        int nboxes = 0;
        float nms=.45;
        float thresh = .5;
        float hier_thresh = .5;
        detection *dets = get_network_boxes(net, im.w, im.h, thresh, hier_thresh, 0, 1, &nboxes);
        printf("%d\n", nboxes);
        if (nms) do_nms_sort(dets, nboxes, l.classes, nms);
        draw_detections(im, dets, nboxes, thresh, names, alphabet, l.classes);
        free_detections(dets, nboxes);
        
        ///////////////////write predictions img
        save_image_png(im, "predictions");// output
        printf("Save Image in %f seconds.\n",what_time_is_it_now()-time);
        
        free_image(im);
        free_image(sized);
        if (camera_mode) {
            cap >> img_now;
            img_res = cv::imread(result_files, CV_LOAD_IMAGE_COLOR);
            //cv::hconcat(img_now, img_res, img_con);
            cv::imshow("Image", img_res);
            if (cv::waitKey(100)==27) { break;}
        } else {
            img_now = cv::imread(result_files, CV_LOAD_IMAGE_COLOR);
            cv::imshow("Image", img_now);
            if (cv::waitKey(100)==27) { break;}
        }
        if (xx==(NUM_OF_IMAGE_FILES-1)) {xx=0;}
        else {xx++;}
    } // while (1)

    printf("YOLOv2 TEST End\n");

    return 0;
}

/*
 * command line argument parsing
 */
int arg_parser(int argc, char **argv)
{
   int   opt;
   opterr = 0; // in order to use '?'
   optind = 1; // make re-enterant
   char *cpt;
   extern int help(int argc, char *argv[]);

   static struct option long_options[] = {
          {"config" , required_argument, 0, 'c'},
          {"bias"   , required_argument, 0, 'b'},
          {"weights", required_argument, 0, 'w'},
          {"camera" , required_argument, 0, 'm'},
          {"help"   , no_argument      , 0, 'h'},
          {0        , 0                , 0,  0 }
   };

   int long_index = 0;
   while ((opt=getopt_long(argc, argv, "c:b:w:m:h",
                           long_options, &long_index))!=-1) {
        switch (opt) {
        case 'c': strcpy(fname_config ,optarg); break;
        case 'b': strcpy(fname_bias   ,optarg); break;
        case 'w': strcpy(fname_weight ,optarg); break;
        case 'm': camera_mode = atoi(optarg); break;
        case 'h': help(argc, argv); return -1;
        case '?': if (optopt=='c') {
                      printf("%c requires an argument.\n", optopt);
                  } else if (isprint(optopt)) {
                      printf("%c unknown\n", optopt);
                  } else {
                      printf("0x%x unknown character\n", optopt);
                  }
                  break;
        default: printf("unknown option %c\n", opt);
        }
   }
   return 0;
}

int help(int argc, char **argv)
{
    printf("[Usage] %s [options]\n", argv[0]);
    printf("   -c,--config=file    configuration file: %s\n", fname_config);
    printf("   -b,--bias=file      bias file: %s\n", fname_bias);
    printf("   -w,--weight=file    weights file: %s\n", fname_weight);
    printf("   -m,--camera=0|1     camera-mode whne 1\n");
    printf("   -h,--help           Print help\n");
    printf("\n");
    return 0;
}

static void get_info_confmc(struct _usb usb, con_MasterInfo_t gpif2mst_info)
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
