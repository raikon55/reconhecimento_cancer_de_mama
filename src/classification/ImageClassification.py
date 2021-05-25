# -*- coding: utf-8 -*-

import os
import random

import cv2
import numpy as np
from skimage.feature import greycomatrix, greycoprops
from skimage.measure import shannon_entropy


class ImageClassification:
    __imagesTrain: list[list]
    __imagesAttributes: list[list]
    __imagesAttributesTest: list[list]

    __mean: list[list]
    __accuracy: float
    __confusionMatrix: list[list]
    __matrix_covariance: list[list]
    __inverse_covariance: list[list]

    __entropyMean: list[list]
    __contrastMean: list[list]
    __homogeneityMean: list[list]

    def __init__(self):
        self.__imagesTrain = [
            [],
            [],
            [],
            []
        ]

        self.__confusionMatrix = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        self.__mean = [
            [],
            [],
            [],
            []
        ]

        self.__matrix_covariance = [
            [],
            [],
            [],
            []
        ]

        self.__matrix_covariance = [
            [],
            [],
            [],
            []
        ]

        self.__inverse_covariance = [
            [],
            [],
            [],
            []
        ]

        self.__imagesAttributes = [
            [],
            [],
            [],
            []
        ]

        self.__imagesAttributesTest = [
            [],
            [],
            [],
            []
        ]

        self.__entropyMean = [
            [0],
            [0],
            [0],
            [0]
        ]

        self.__contrastMean = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]

        self.__homogeneityMean = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]

    def load_images(self, directory_path: str) -> None:
        for directory in os.listdir(directory_path):

            image_files: str = os.path.join(directory_path, directory)
            if os.path.isfile(image_files) is False:

                for img in os.listdir(image_files):

                    if img.endswith(u'.png') or img.endswith(u'.tif'):
                        image_full_path: str = str(image_files + '/' + img).replace('\\', '/')
                        self.__imagesTrain[int(directory) - 1].append(
                            (image_full_path, cv2.imread(image_full_path, cv2.IMREAD_GRAYSCALE)))

    def train(self) -> None:
        image_list: list = []
        image_list_test: list = []

        for path in self.__imagesTrain:
            random.shuffle(path)

            self.get_attributes_mean(path, test=False)

            self.__contrastMean[self.__imagesTrain.index(path)] /= round(len(path) * 0.75)
            self.__homogeneityMean[self.__imagesTrain.index(path)] /= round(len(path) * 0.75)
            self.__entropyMean[self.__imagesTrain.index(path)] /= round(len(path) * 0.75)

            for imageAttribute in self.__imagesAttributes[self.__imagesTrain.index(path)]:
                imageAttribute[0] = np.subtract(imageAttribute[0], self.__contrastMean[self.__imagesTrain.index(path)])
                imageAttribute[1] = np.subtract(imageAttribute[1],
                                                self.__homogeneityMean[self.__imagesTrain.index(path)])
                imageAttribute[2] = np.subtract(imageAttribute[2], self.__entropyMean[self.__imagesTrain.index(path)])

            attributes_group = []

            for attributes in self.__imagesAttributes[self.__imagesTrain.index(path)]:
                image_attribute = np.ndarray(shape=(0, 0))

                for attribute in attributes:
                    image_attribute = np.concatenate((image_attribute, attribute), axis=None)

                attributes_group.append(image_attribute)

            image_list.append(attributes_group)

        self.__matrix_covariance = [
            np.cov(np.array(image_list[0]).T),
            np.cov(np.array(image_list[1]).T),
            np.cov(np.array(image_list[2]).T),
            np.cov(np.array(image_list[3]).T)
        ]

        self.__inverse_covariance = [
            np.linalg.inv(self.__matrix_covariance[0]),
            np.linalg.inv(self.__matrix_covariance[1]),
            np.linalg.inv(self.__matrix_covariance[2]),
            np.linalg.inv(self.__matrix_covariance[3])
        ]

        self.__mean = [
            np.concatenate((self.__contrastMean[0], self.__homogeneityMean[0], self.__entropyMean[0]), axis=None),
            np.concatenate((self.__contrastMean[1], self.__homogeneityMean[1], self.__entropyMean[1]), axis=None),
            np.concatenate((self.__contrastMean[2], self.__homogeneityMean[2], self.__entropyMean[2]), axis=None),
            np.concatenate((self.__contrastMean[3], self.__homogeneityMean[3], self.__entropyMean[3]), axis=None)
        ]

        for path in self.__imagesTrain:

            self.get_attributes_mean(path, test=True)

            attributes_test_dir = []

            for attributes in self.__imagesAttributesTest[self.__imagesTrain.index(path)]:
                images_attributes_test = np.ndarray(shape=(0, 0))

                for attribute_test in attributes:
                    images_attributes_test = np.concatenate((images_attributes_test, attribute_test), axis=None)

                attributes_test_dir.append(images_attributes_test)

            image_list_test.append(attributes_test_dir)

            for i in range(75, 100):
                diff_attributes_test: list = [
                    np.subtract(attributes_test_dir[i - 75], self.__mean[0]),
                    np.subtract(attributes_test_dir[i - 75], self.__mean[1]),
                    np.subtract(attributes_test_dir[i - 75], self.__mean[2]),
                    np.subtract(attributes_test_dir[i - 75], self.__mean[3])
                ]

                distance: list = [
                    np.dot(np.dot(np.array(diff_attributes_test[0]).T, self.__inverse_covariance[0]),
                           np.array(diff_attributes_test[0])),
                    np.dot(np.dot(np.array(diff_attributes_test[1]).T, self.__inverse_covariance[1]),
                           np.array(diff_attributes_test[1])),
                    np.dot(np.dot(np.array(diff_attributes_test[2]).T, self.__inverse_covariance[2]),
                           np.array(diff_attributes_test[2])),
                    np.dot(np.dot(np.array(diff_attributes_test[3]).T, self.__inverse_covariance[3]),
                           np.array(diff_attributes_test[3])),
                ]

                self.__confusionMatrix[self.__imagesTrain.index(path)][distance.index(min(distance))] += 1

        self.__accuracy = 0.0
        for i in range(0, 4):
            self.__accuracy += self.__confusionMatrix[i][i]

    def get_attributes_mean(self, path: list, test: bool) -> None:
        for images in path[:round(len(path) * 0.75)]:
            image = images[1]
            data = np.array((image / 8), 'int')
            g = greycomatrix(data, [1, 2, 4, 8, 16], [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4], levels=32,
                             normed=True,
                             symmetric=True)

            contrast = greycoprops(g, 'contrast')
            contrast = [sum(i) for i in contrast]
            self.__contrastMean[self.__imagesTrain.index(path)] = np.add(
                self.__contrastMean[self.__imagesTrain.index(path)],
                contrast)

            entropy = shannon_entropy(data)
            self.__entropyMean[self.__imagesTrain.index(path)] = np.add(
                self.__entropyMean[self.__imagesTrain.index(path)],
                entropy)

            homogeneity = greycoprops(g, 'homogeneity')
            homogeneity = [sum(i) for i in homogeneity]
            self.__homogeneityMean[self.__imagesTrain.index(path)] = np.add(
                self.__homogeneityMean[self.__imagesTrain.index(path)], homogeneity)

            if test:
                self.__imagesAttributesTest[self.__imagesTrain.index(path)].append([contrast, homogeneity, entropy])
            else:
                self.__imagesAttributes[self.__imagesTrain.index(path)].append([contrast, homogeneity, entropy])

    def classify_single_image(self, filename: str) -> str:
        image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        data = np.array((image / 8), 'int')
        grey_matrix = greycomatrix(data, [1, 2, 4, 8, 16], [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4], levels=32,
                                   normed=True,
                                   symmetric=True)

        contrast = greycoprops(grey_matrix, 'contrast')
        contrast = [sum(i) for i in contrast]

        entropy = shannon_entropy(data)

        homogeneity = greycoprops(grey_matrix, 'homogeneity')
        homogeneity = [sum(i) for i in homogeneity]

        attributes_image = np.concatenate((contrast, homogeneity, entropy), axis=None)

        diff_attributes: list = [
            np.subtract(attributes_image, self.__mean[0]),
            np.subtract(attributes_image, self.__mean[1]),
            np.subtract(attributes_image, self.__mean[2]),
            np.subtract(attributes_image, self.__mean[3])
        ]

        distance: list[list] = [
            np.dot(np.dot(np.array(diff_attributes[0]).T, self.__inverse_covariance[0]), np.array(diff_attributes[0])),
            np.dot(np.dot(np.array(diff_attributes[1]).T, self.__inverse_covariance[1]), np.array(diff_attributes[1])),
            np.dot(np.dot(np.array(diff_attributes[2]).T, self.__inverse_covariance[2]), np.array(diff_attributes[2])),
            np.dot(np.dot(np.array(diff_attributes[3]).T, self.__inverse_covariance[3]), np.array(diff_attributes[3]))
        ]

        return f'\n\nClass BIRADS: {distance.index(min(distance))+1:.0f}\n\n'

    def show_confusion_matrix(self) -> str:
        matrix: list[list] = self.__confusionMatrix.copy()
        return (
            f"""| {matrix[0][0]:02} | {matrix[0][1]:02} | {matrix[0][2]:02} | {matrix[0][3]:02} |\n"""
            f"""| {matrix[1][0]:02} | {matrix[1][1]:02} | {matrix[1][2]:02} | {matrix[1][3]:02} |\n"""
            f"""| {matrix[2][0]:02} | {matrix[2][1]:02} | {matrix[2][2]:02} | {matrix[2][3]:02} |\n"""
            f"""| {matrix[3][0]:02} | {matrix[3][1]:02} | {matrix[3][2]:02} | {matrix[3][3]:02} |\n"""
            f"""\nAcurácia: {self.__accuracy:.2f} %\n"""
            f"""Especificidade: {((100 - self.__accuracy) / 300):.6f}"""
        )
