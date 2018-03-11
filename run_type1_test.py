from type_1_dataset import  get_PU_data
from train import get_PU_model
import utils
from visual_results import generate_and_save_visualizations
import copy
import Config
import datetime
import numpy as np

def run():
    # cross validation ratio change
    include_class_list = Config.type_1_include_class_list
    for pos_class in include_class_list:
        neg_class_list = copy.copy(list(set(include_class_list)))
        neg_class_list.remove(pos_class)
        if len(neg_class_list) > 0:
            for ratio in [1, 0.82, 0.67, 0.54, 0.43, 0.33, 0.25, 0.18]:
                test_name = 'type_1_train_cross_'+str(ratio)
                if not utils.check_if_test_done(pos_class, test_name, ",".join([str(i) for i in neg_class_list])):
                # if pos_class == 2:
                    data_img, labelled_img = utils.load_preprocessed_data()
                    n_class = np.max(labelled_img) + 1
                    exclude_list = list(set([i for i in range(n_class)]) - set(include_class_list))
                    (XYtrain, XYtest, prior, testX, testY, trainX, trainY, crossX, crossY), \
                    (train_lp_pixels, train_up_pixels, train_un_pixels, test_pos_pixels, test_neg_pixels, shuffled_test_pixels) = get_PU_data([pos_class] , neg_class_list, data_img, labelled_img, ratio, Config.type_1_cross_pos_percentage, ratio)
                    print("training", trainX.shape)
                    print("training split: labelled positive ->", len(train_lp_pixels[0]), "unlabelled positive ->", len(train_up_pixels[0]), "unlabelled negative ->", len(train_un_pixels[0]))
                    print("test", testX.shape)
                    model = get_PU_model(XYtrain, XYtest, prior)

                    # generate predicted and groundtooth image
                    exclude_pixels = utils.get_excluded_pixels(labelled_img, train_lp_pixels, train_up_pixels, train_un_pixels, test_pos_pixels, test_neg_pixels)
                    gt_img = utils.get_binary_gt_img(labelled_img, train_lp_pixels, train_up_pixels, train_un_pixels, test_pos_pixels, test_neg_pixels, exclude_pixels)
                    threshold = utils.get_threshold(model, crossX, crossY)
                    print("threshold ->", threshold)
                    predicted_img, predicted_output = utils.get_binary_predicted_image(labelled_img, model, testX, train_lp_pixels, train_up_pixels, train_un_pixels, shuffled_test_pixels, exclude_pixels)

                    # get model stats
                    precision, recall, (tn, fp, fn, tp) = utils.get_model_stats(predicted_output, testY)
                    visual_result_filename = "result/type_1_cross_test_" + str(pos_class) + "_pos_"+ str(datetime.datetime.now().timestamp() * 1000) +".png"
                    generate_and_save_visualizations(gt_img, predicted_img, train_lp_pixels, train_up_pixels, train_un_pixels, test_pos_pixels, test_neg_pixels, \
                                                     exclude_pixels, visual_result_filename)
                    utils.save_data_in_PUstats((
                                         str(pos_class), ",".join([str(i) for i in neg_class_list]), precision, recall, tp,
                                         tn, fp, fn, test_name, ",".join([str(i) for i in exclude_list]), int(len(train_lp_pixels[0])),
                                         int(len(train_up_pixels[0])), int(len(train_un_pixels[0])), visual_result_filename, ratio, threshold))
    # without threshold
    include_class_list = Config.type_1_include_class_list
    for pos_class in include_class_list:
        neg_class_list = copy.copy(list(set(include_class_list)))
        neg_class_list.remove(pos_class)
        if len(neg_class_list) > 0:
            for ratio in [1, 0.82, 0.67, 0.54, 0.43, 0.33, 0.25, 0.18]:
                test_name = 'type_1_no_threshold_' + str(ratio)
                if not utils.check_if_test_done(pos_class, test_name, ",".join([str(i) for i in neg_class_list])):
                    # if pos_class == 2:
                    data_img, labelled_img = utils.load_preprocessed_data()
                    n_class = np.max(labelled_img) + 1
                    exclude_list = list(set([i for i in range(n_class)]) - set(include_class_list))
                    (XYtrain, XYtest, prior, testX, testY, trainX, trainY, crossX, crossY), \
                    (train_lp_pixels, train_up_pixels, train_un_pixels, test_pos_pixels, test_neg_pixels,
                     shuffled_test_pixels) = get_PU_data([pos_class], neg_class_list, data_img, labelled_img, ratio,
                                                         Config.type_1_cross_pos_percentage,
                                                         Config.type_1_pos_neg_ratio_in_cross)
                    print("training", trainX.shape)
                    print("training split: labelled positive ->", len(train_lp_pixels[0]), "unlabelled positive ->",
                          len(train_up_pixels[0]), "unlabelled negative ->", len(train_un_pixels[0]))
                    print("test", testX.shape)
                    model = get_PU_model(XYtrain, XYtest, prior)

                    # generate predicted and groundtooth image
                    exclude_pixels = utils.get_excluded_pixels(labelled_img, train_lp_pixels, train_up_pixels,
                                                               train_un_pixels, test_pos_pixels, test_neg_pixels)
                    gt_img = utils.get_binary_gt_img(labelled_img, train_lp_pixels, train_up_pixels, train_un_pixels,
                                                     test_pos_pixels, test_neg_pixels, exclude_pixels)
                    # threshold = utils.get_threshold(model, crossX, crossY)
                    # print("threshold ->", threshold)
                    predicted_img, predicted_output = utils.get_binary_predicted_image(labelled_img, model, testX,
                                                                                       train_lp_pixels, train_up_pixels,
                                                                                       train_un_pixels,
                                                                                       shuffled_test_pixels,
                                                                                       exclude_pixels)

                    # get model stats
                    precision, recall, (tn, fp, fn, tp) = utils.get_model_stats(predicted_output, testY)
                    visual_result_filename = "result/type_1_cross_test_" + str(pos_class) + "_pos_" + str(
                        datetime.datetime.now().timestamp() * 1000) + ".png"
                    generate_and_save_visualizations(gt_img, predicted_img, train_lp_pixels, train_up_pixels,
                                                     train_un_pixels, test_pos_pixels, test_neg_pixels, \
                                                     exclude_pixels, visual_result_filename)
                    utils.save_data_in_PUstats((
                        str(pos_class), ",".join([str(i) for i in neg_class_list]), precision, recall, tp,
                        tn, fp, fn, test_name, ",".join([str(i) for i in exclude_list]), int(len(train_lp_pixels[0])),
                        int(len(train_up_pixels[0])), int(len(train_un_pixels[0])), visual_result_filename, ratio,
                        None))
    # cross validation pixels increase with cross validation ratio change
    include_class_list = Config.type_1_include_class_list
    type_1_cross_pos_percentage = 30
    for pos_class in include_class_list:
        neg_class_list = copy.copy(list(set(include_class_list)))
        neg_class_list.remove(pos_class)
        if len(neg_class_list) > 0:
            for ratio in [1, 0.82, 0.67, 0.54, 0.43, 0.33, 0.25, 0.18]:
                test_name = 'type_1_train_cross_' + str(ratio) + '_and_'+ str(type_1_cross_pos_percentage) +'_in_cross'
                if not utils.check_if_test_done(pos_class, test_name, ",".join([str(i) for i in neg_class_list])):
                    # if pos_class == 2:
                    data_img, labelled_img = utils.load_preprocessed_data()
                    n_class = np.max(labelled_img) + 1
                    exclude_list = list(set([i for i in range(n_class)]) - set(include_class_list))
                    (XYtrain, XYtest, prior, testX, testY, trainX, trainY, crossX, crossY), \
                    (train_lp_pixels, train_up_pixels, train_un_pixels, test_pos_pixels, test_neg_pixels,
                     shuffled_test_pixels) = get_PU_data([pos_class], neg_class_list, data_img, labelled_img, ratio,
                                                         type_1_cross_pos_percentage,
                                                         ratio)
                    print("training", trainX.shape)
                    print("training split: labelled positive ->", len(train_lp_pixels[0]), "unlabelled positive ->",
                          len(train_up_pixels[0]), "unlabelled negative ->", len(train_un_pixels[0]))
                    print("test", testX.shape)
                    model = get_PU_model(XYtrain, XYtest, prior)

                    # generate predicted and groundtooth image
                    exclude_pixels = utils.get_excluded_pixels(labelled_img, train_lp_pixels, train_up_pixels,
                                                               train_un_pixels, test_pos_pixels, test_neg_pixels)
                    gt_img = utils.get_binary_gt_img(labelled_img, train_lp_pixels, train_up_pixels, train_un_pixels,
                                                     test_pos_pixels, test_neg_pixels, exclude_pixels)
                    # threshold = utils.get_threshold(model, crossX, crossY)
                    # print("threshold ->", threshold)
                    predicted_img, predicted_output = utils.get_binary_predicted_image(labelled_img, model, testX,
                                                                                       train_lp_pixels, train_up_pixels,
                                                                                       train_un_pixels,
                                                                                       shuffled_test_pixels,
                                                                                       exclude_pixels)

                    # get model stats
                    precision, recall, (tn, fp, fn, tp) = utils.get_model_stats(predicted_output, testY)
                    visual_result_filename = "result/type_1_cross_test_" + str(pos_class) + "_pos_" + str(
                        datetime.datetime.now().timestamp() * 1000) + ".png"
                    generate_and_save_visualizations(gt_img, predicted_img, train_lp_pixels, train_up_pixels,
                                                     train_un_pixels, test_pos_pixels, test_neg_pixels, \
                                                     exclude_pixels, visual_result_filename)
                    utils.save_data_in_PUstats((
                        str(pos_class), ",".join([str(i) for i in neg_class_list]), precision, recall, tp,
                        tn, fp, fn, test_name, ",".join([str(i) for i in exclude_list]), int(len(train_lp_pixels[0])),
                        int(len(train_up_pixels[0])), int(len(train_un_pixels[0])), visual_result_filename, ratio,
                        None))


if __name__ == '__main__':
    run()


