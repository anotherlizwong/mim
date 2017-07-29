import graphlab as gl
import models
import util
import json
import flatten_json
import os
from pandas.io.json import json_normalize
from . import logger

gl.get_dependencies()

MODEL_LOCATION = "user_model"

if "graphlab_key" in os.environ:
    # gl.set_runtime_config("product_key",os.environ["graphlab_key"])
    gl.product_key.set_product_key(os.environ["graphlab_key"])


def load_training_data(all_users=True):
    """
    Pulls the historical ratings from the database into the ML library
    :param all_users: Optional Boolean flag to train on all users or the current user
    :return: train_data, test_data split
    """
    if all_users:
        user = None
        filename = "data_all.txt"
    else:
        user = util.get_user()
        filename = "data_"+user+".txt"


    # write the latest database value
    # TODO: optimize to load direct from database
    json_string = models.get_user_history(user, True)
    user_history_json = json.loads(json_string)
    file_content = []
    for history_dict in user_history_json:
        file_content.append(flatten_json.flatten(history_dict))
    with open(filename, "w") as outfile:
        json.dump(file_content, outfile)

    # load training data into graphlab
    training_data = gl.SFrame.read_json(url=filename, orient="records")

    # kill temporary file now that data is loaded
    # TODO: when the recommender trains once daily, don't delete the file
    try:
        os.remove(filename)
    except OSError:
        pass

    return training_data.random_split(.8)


def train():
    train_data, test_data = load_training_data()
    my_features_model = gl.recommender.item_similarity_recommender.create(
        train_data, user_id="user", item_id="content_id", target="opinion_opinion")
    logger.info("model quality: "+my_features_model.evaluate_rmse(test_data, target="opinion_opinion"))

    try:
        my_features_model.save(MODEL_LOCATION)
    except:
        logger.error("couldn't save model", exc_info=True)
        pass

    return my_features_model


def predict_options(options):
    """
    Run predictions on potential options
    :param options: array of dictionary, expected format [{"user": __, "content.id": __}]
    :return: an array with predicted scores for each option; None if invalid
    """
    # TODO - Need to format option in a way that makes sense for the predictor
    if os.path.exists(MODEL_LOCATION):
        model = gl.load_model(MODEL_LOCATION)
    else:
        logger.warn("couldn't load module, re-training", exc_info=True)
        model = train()

    if "user" in options and "content_id" in options:
        prediction = model.predict(options)
        logger.info("prediction: " + prediction)
    else:
        logger.error("options not in the correct format, expected key 'user' and key 'content_id' got: "
                     + options.keys())
        prediction = None

    return prediction

