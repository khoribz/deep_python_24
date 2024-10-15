"""
This module contains a simple sentiment analysis model and
a function to predict the mood of a message based on random
scoring and predefined thresholds.

Classes:
    SomeModel: A model that predicts a score based on message length.
    GradeName: An enumeration for different message mood grades.

Functions:
    predict_message_mood: Predicts the mood of a message
    as 'BAD', 'GOOD', or 'EXCELLENT'.
"""

from enum import Enum


class SomeModel:  # pylint: disable=R0903
    """
        This model predicts a sentiment score based on message length.
        The prediction is a random float between 0 and 1, normalized
        by the message length.
    """

    def predict(self, message: str) -> float:
        """
                Predict a score based on the input message.

                Args:
                    message (str): The input text to analyze.

                Returns:
                    float: A sentiment score between 0 and 1.
        """
        alpha_count = 0
        for letter in message:
            if letter.isalpha():
                alpha_count += 1
        return alpha_count / len(message)


class GradeName(str, Enum):
    """
        Enum representing possible mood grades.
        """
    BAD = 'неуд'
    EXCELLENT = 'отл'
    GOOD = 'норм'


def predict_message_mood(
    message: str,
    bad_threshold: float = 0.3,
    good_threshold: float = 0.8,
) -> str:
    """
        Predict the mood of a message based on predefined thresholds.

        Args:
            message (str): The input message to analyze.

            bad_threshold (float): Threshold below which the
            mood is considered bad.

            good_threshold (float): Threshold above which the
            mood is considered excellent.

        Returns:
            str: One of 'BAD', 'EXCELLENT', or 'GOOD' based on the
            predicted sentiment.
        """
    model = SomeModel()
    predict_threshold = model.predict(message)
    if predict_threshold < bad_threshold:
        return GradeName.BAD
    if predict_threshold > good_threshold:
        return GradeName.EXCELLENT
    return GradeName.GOOD
