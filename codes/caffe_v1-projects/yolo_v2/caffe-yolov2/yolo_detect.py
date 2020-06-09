""" YOLO detection demo in Caffe """
from __future__ import print_function, division

import argparse
from datetime import datetime

import numpy as np

import cv2
import caffe


USE_GPU = False

if USE_GPU:
    GPU_ID = 0 # Switch between 0 and 1 depending on the GPU you want to use.
    caffe.set_mode_gpu()
    caffe.set_device(GPU_ID)
else:
    caffe.set_mode_cpu()


def load_names(filename):
    """ load names from a text file (one per line) """
    with open(filename, 'r') as fid:
        names = [l.strip() for l in fid]
    return names


PRESETS = {
    'coco': { 'classes': [
        "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
        "truck", "boat", "traffic light", "fire hydrant", "stop sign",
        "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
        "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
        "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
        "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
        "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
        "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
        "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
        "couch", "potted plant", "bed", "dining table", "toilet", "tv",
        "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave",
        "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
        "scissors", "teddy bear", "hair drier", "toothbrush"
    ], 'anchors': [[0.738768, 2.42204, 4.30971, 10.246, 12.6868],
                   [0.874946, 2.65704, 7.04493, 4.59428, 11.8741]]
    },
    'voc': { 'classes': [
        "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car",
        "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike",
        "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"],
        'anchors':  [[1.08, 3.42, 6.63, 9.42, 16.62],
                    [1.19, 4.41, 11.38, 5.11, 10.52]]
    },
    'darknet': { 'classes': load_names('imagenet.shortnames'), 'anchors': []}
}


def get_boxes(output, img_size, grid_size, num_boxes):
    """ extract bounding boxes from the last layer """

    w_img, h_img = img_size[1], img_size[0]
    boxes = np.reshape(output, (grid_size, grid_size, num_boxes, 4))

    offset = np.tile(np.arange(grid_size)[:, np.newaxis],
                     (grid_size, 1, num_boxes))

    boxes[:, :, :, 0] += offset
    boxes[:, :, :, 1] += np.transpose(offset, (1, 0, 2))
    boxes[:, :, :, 0:2] /= 7.0
    # the predicted size is the square root of the box size
    boxes[:, :, :, 2:4] *= boxes[:, :, :, 2:4]

    boxes[:, :, :, [0, 2]] *= w_img
    boxes[:, :, :, [1, 3]] *= h_img

    return boxes


def parse_yolo_output_v1(output, img_size, num_classes):
    """ convert the output of the last fully connected layer (Darknet v1) """

    n_coord_box = 4    # number of coordinates in each bounding box
    grid_size = 7

    sc_offset = grid_size * grid_size * num_classes

    # autodetect num_boxes
    num_boxes = int((output.shape[0] - sc_offset) /
                    (grid_size*grid_size*(n_coord_box+1)))
    box_offset = sc_offset + grid_size * grid_size * num_boxes

    class_probs = np.reshape(output[0:sc_offset], (grid_size, grid_size, num_classes))
    confidences = np.reshape(output[sc_offset:box_offset], (grid_size, grid_size, num_boxes))

    probs = np.zeros((grid_size, grid_size, num_boxes, num_classes))
    for i in range(num_boxes):
        for j in range(num_classes):
            probs[:, :, i, j] = class_probs[:, :, j] * confidences[:, :, i]

    boxes = get_boxes(output[box_offset:], img_size, grid_size, num_boxes)

    return boxes, probs


def logistic(val):
    """ compute the logistic activation """
    return 1.0 / (1.0 + np.exp(-val))


def softmax(val, axis=-1):
    """ compute the softmax of the given tensor, normalizing on axis """
    exp = np.exp(val - np.amax(val, axis=axis, keepdims=True))
    return exp / np.sum(exp, axis=axis, keepdims=True)


def get_boxes_v2(output, img_size, anchors):
    """ extract bounding boxes from the last layer (Darknet v2) """
    bias_w, bias_h = anchors

    w_img, h_img = img_size[1], img_size[0]
    grid_w, grid_h, num_boxes = output.shape[:3]

    # tweak: add a 0.5 offset to improve localization accuracy
    offset_x = \
        np.tile(np.arange(grid_w)[:, np.newaxis], (grid_h, 1, num_boxes)) - 0.5
    offset_y = np.transpose(offset_x, (1, 0, 2))

    boxes = output.copy()
    boxes[:, :, :, 0] = (offset_x + logistic(boxes[:, :, :, 0])) / grid_w
    boxes[:, :, :, 1] = (offset_y + logistic(boxes[:, :, :, 1])) / grid_h
    boxes[:, :, :, 2] = np.exp(boxes[:, :, :, 2]) * bias_w / grid_w
    boxes[:, :, :, 3] = np.exp(boxes[:, :, :, 3]) * bias_h / grid_h

    boxes[:, :, :, [0, 2]] *= w_img
    boxes[:, :, :, [1, 3]] *= h_img

    return boxes


def parse_yolo_output_v2(output, img_size, num_classes, anchors):
    """ convert the output of the last convolutional layer (Darknet v2) """
    n_coord_box = 4

    # for each box: coordinates, probs scale, class probs
    num_boxes = output.shape[0] // (n_coord_box + 1 + num_classes)
    output = output.reshape((num_boxes, -1, output.shape[1], output.shape[2]))\
             .transpose((2, 3, 0, 1))

    probs = logistic(output[:, :, :, 4:5]) * softmax(output[:, :, :, 5:], axis=3)
    boxes = get_boxes_v2(output[:, :, :, :4], img_size, anchors)

    return boxes, probs


def parse_yolo_output(output, img_size, num_classes, anchors=None):
    """ convert the output of YOLO's last layer to boxes and confidence in each
    class """
    if len(output.shape) == 1:
        return parse_yolo_output_v1(output, img_size, num_classes)
    elif len(output.shape) == 3 and anchors is not None:
        return parse_yolo_output_v2(output, img_size, num_classes, anchors)
    else:
        raise ValueError(" output format not recognized")


def get_candidate_objects(output, img_size, mode):
    """ convert network output to bounding box predictions """

    threshold = 0.2
    iou_threshold = 0.4

    classes = PRESETS[mode]['classes']
    anchors = PRESETS[mode]['anchors']

    boxes, probs = parse_yolo_output(output, img_size, len(classes), anchors)

    filter_mat_probs = (probs >= threshold)
    filter_mat_boxes = np.nonzero(filter_mat_probs)[0:3]
    boxes_filtered = boxes[filter_mat_boxes]
    probs_filtered = probs[filter_mat_probs]
    classes_num_filtered = np.argmax(probs, axis=3)[filter_mat_boxes]

    idx = np.argsort(probs_filtered)[::-1]
    boxes_filtered = boxes_filtered[idx]
    probs_filtered = probs_filtered[idx]
    classes_num_filtered = classes_num_filtered[idx]

    # too many detections - exit
    if len(boxes_filtered) > 1e3:
        print("Too many detections, maybe an error? : {}".format(
            len(boxes_filtered)))
        return []

    probs_filtered = non_maxima_suppression(boxes_filtered, probs_filtered,
                                            classes_num_filtered, iou_threshold)

    filter_iou = (probs_filtered > 0.0)
    boxes_filtered = boxes_filtered[filter_iou]
    probs_filtered = probs_filtered[filter_iou]
    classes_num_filtered = classes_num_filtered[filter_iou]

    result = []
    for class_id, box, prob in zip(classes_num_filtered, boxes_filtered, probs_filtered):
        result.append([classes[class_id], box[0], box[1], box[2], box[3], prob])

    return result


def non_maxima_suppression(boxes, probs, classes_num, thr=0.2):
    """ greedily suppress low-scoring overlapped boxes """
    for i, box in enumerate(boxes):
        if probs[i] == 0:
            continue
        for j in range(i+1, len(boxes)):
            if classes_num[i] == classes_num[j] and iou(box, boxes[j]) > thr:
                probs[j] = 0.0

    return probs


def iou(box1, box2, denom="min"):
    """ compute intersection over union score """
    int_tb = min(box1[0]+0.5*box1[2], box2[0]+0.5*box2[2]) - \
             max(box1[0]-0.5*box1[2], box2[0]-0.5*box2[2])
    int_lr = min(box1[1]+0.5*box1[3], box2[1]+0.5*box2[3]) - \
             max(box1[1]-0.5*box1[3], box2[1]-0.5*box2[3])

    intersection = max(0.0, int_tb) * max(0.0, int_lr)
    area1, area2 = box1[2]*box1[3], box2[2]*box2[3]
    control_area = min(area1, area2) if denom == "min"  \
                   else area1 + area2 - intersection

    return intersection / control_area


def draw_box(img, name, box, score):
    """ draw a single bounding box on the image """
    xmin, ymin, xmax, ymax = box

    box_tag = '{} : {:.2f}'.format(name, score)
    text_x, text_y = 5, 7

    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
    boxsize, _ = cv2.getTextSize(box_tag, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.rectangle(img, (xmin, ymin-boxsize[1]-text_y),
                  (xmin+boxsize[0]+text_x, ymin), (0, 225, 0), -1)
    cv2.putText(img, box_tag, (xmin+text_x, ymin-text_y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)


def show_results(img, results):
    """ draw bounding boxes on the image """
    img_width, img_height = img.shape[1], img.shape[0]
    disp_console = True
    imshow = True

    for result in results:
        box_x, box_y, box_w, box_h = [int(v) for v in result[1:5]]
        if disp_console:
            print('    class : {}, [x,y,w,h]=[{:d},{:d},{:d},{:d}], Confidence = {}'.\
                format(result[0], box_x, box_y, box_w, box_h, str(result[5])))
        xmin, xmax = max(box_x-box_w//2, 0), min(box_x+box_w//2, img_width)
        ymin, ymax = max(box_y-box_h//2, 0), min(box_y+box_h//2, img_height)

        if imshow:
            draw_box(img, result[0], (xmin, ymin, xmax, ymax), result[5])
    if imshow:
        cv2.imshow('YOLO detection', img)


def crop_max(img, shape):
    """ crop the largest dimension to avoid stretching """
    net_h, net_w = shape
    height, width = img.shape[:2]
    aratio = net_w / net_h

    if width > height * aratio:
        diff = int((width - height * aratio) / 2)
        return img[:, diff:-diff, :]
    else:
        diff = int((height - width / aratio) / 2)
        return img[diff:-diff, :, :]


def detect(model_filename, weight_filename, img_filename, mode):
    """ given a YOLO caffe model and an image, detect the objects in the image
    """
    net = caffe.Net(model_filename, weight_filename, caffe.TEST)
    img = caffe.io.load_image(img_filename) # load the image using caffe.io
    if mode == 'darknet':
        img = crop_max(img, net.blobs['data'].data.shape[-2:])

    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2, 0, 1))

    t_start = datetime.now()
    out = net.forward_all(data=np.asarray([transformer.preprocess('data', img)]))
    t_end = datetime.now()
    print('total time is {:.2f} milliseconds'.format((t_end-t_start).total_seconds()*1e3))

    if mode == 'darknet':
        net_output = out[out.keys()[0]]   # get first out layer
        if len(net_output.shape) > 2:
            net_output = np.squeeze(net_output)[np.newaxis, :]

        ids = np.argsort(net_output[0])[-1:-6:-1]
        print('predicted classes: {}'.format(
            [(PRESETS[mode]['classes'][cls_id], net_output[0][cls_id])
             for cls_id in ids]))
    else:
        img_cv = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        results = get_candidate_objects(out['result'][0], img.shape, mode)
        show_results(img_cv, results)
        cv2.waitKey()


def main():
    """ script entry point """
    parser = argparse.ArgumentParser(description='Caffe-YOLO detection test')
    parser.add_argument('model', type=str, help='model prototxt')
    parser.add_argument('weights', type=str, help='model weights')
    parser.add_argument('image', type=str, help='input image')
    parser.add_argument('--mode', type=str, help='preset to use', default='coco')
    args = parser.parse_args()

    if args.mode not in PRESETS.keys():
        raise ValueError(" Preset not supported: {}".format(args.mode))

    print('model file is {}'.format(args.model))
    print('weight file is {}'.format(args.weights))
    print('image file is {}'.format(args.image))

    detect(args.model, args.weights, args.image, args.mode)


if __name__ == '__main__':
    main()
