import graphlab as gl
import models
import util
import json
import os
from pandas.io.json import json_normalize
from . import logger

if "graphlab_key" in os.environ:
    gl.product_key.set_product_key(os.environ["graphlab_key"])


def load_training_data(all_users=True):
    """
    Pulls the historical ratings from the database into the ML library
    :param all_users: Optional Boolean flag to train on all users or the current user
    :return: train_data, test_data split
    """
    if all_users:
        user = None
    else:
        user = util.get_user()

    filename = "data_"+user+".txt"

    # write the latest database value
    # TODO: optimize to load direct from database
    file_content = json_normalize(models.get_user_history(user))
    with open(filename, "w") as outfile:
        json.dump(file_content, outfile)

    # load training data into graphlab
    training_data = gl.SFrame.read_json(url=filename, orient="records")

    # kill temporary file now that data is loaded
    try:
        os.remove(filename)
    except OSError:
        pass

    return training_data.random_split(.8)


def train():
    train_data, test_data = load_training_data()
    my_features = ["content.id", "content.content_type"]
    # TODO - I'm not sure that linear_regression is the thing I want to do here, maybe kNN?
    my_features_model = gl.linear_regression.create(train_data, target="opinion", features=my_features, validation_set=None)
    logger.info("model quality: "+my_features_model.evaluate(test_data))
    return my_features_model


def predict_option(option):
    # TODO - Need to format option in a way that makes sense for the predictor
    model = train()
    prediction = model.predict(option)
    logger.info("prediction: "+prediction)
    return prediction

