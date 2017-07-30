import graphlab as gl
import models
import util
import json
import flatten_json
import os
import random
from pandas.io.json import json_normalize
from . import logger


MODEL_LOCATION = "user_model"

if "graphlab_key" in os.environ:
    # gl.set_runtime_config("product_key",os.environ["graphlab_key"])
    gl.product_key.set_product_key(os.environ["graphlab_key"])

try:
    gl.get_dependencies()
except:
    logger.error("weird dependency thing that I can't figure out", exc_info=True)
    pass



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
    # TODO: optimize to load direct from database (look into connect_odbc())
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
    logger.info("model quality: ", my_features_model.evaluate_rmse(test_data, target="opinion_opinion"))

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

    if "user" in options[0] and "content_id" in options[0]:
        temp_users = []
        temp_content = []
        for option in options:
            temp_users.append(option["user"])
            temp_content.append(option["content_id"])
        users = gl.SArray(temp_users)
        content = gl.SArray(temp_content)
        frame = gl.SFrame({"user": users, "content_id": content}, format="dict")
        prediction = model.predict(frame)
        logger.info("prediction: ", str(prediction))
    else:
        logger.error("options not in the correct format, expected key 'user' and key 'content_id'")
        prediction = None

    return list(prediction)


def pick_option(choices):
    """
    Pick an option from the list using recommendation score or random if rec scores all too low
    :param choices: an array of videos formatted in format_results()
    :return: A single video option
    """
    # random choice (default)
    final_choice = choices[random.randint(0, len(choices) - 1)]

    # use recommendation engine
    options = []
    user = util.get_user()
    for v in choices:
        option = {
            "user": user,
            "content_id": v["id"]
        }
        options.append(option)
    predictions = predict_options(options)
    if max(predictions) is not 0:
        # pick the highest predicted value, otherwise if no prediction available do random
        final_choice = choices[predictions.index(max(predictions))]

    return final_choice
