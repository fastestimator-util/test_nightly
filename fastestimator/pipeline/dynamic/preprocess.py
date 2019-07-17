"""Dynamic preprocessing functions before TFRecord generation.
"""
import os
from abc import ABC, abstractmethod

import numpy as np

EPSILON = 1e-7


class AbstractPreprocessing(ABC):
    """Abstract class for preprocessing.
    """

    @abstractmethod
    def transform(self, data, feature=None):
        """
        Placeholder function that is to be inherited by preprocessing classes.

        Args:
            data: Data to be preprocessed
            feature: Auxiliary decoded data needed for the preprocessing

        Returns:
            Transformed data numpy array
        """
        return data


class NrrdReader(AbstractPreprocessing):
    """
    Class for reading NRRD images

    Args:
        parent_path (str): Parent path that will be added on given path.
    """

    def __init__(self, parent_path=""):
        import nibabel as nib
        self.transform_fn = nib.load
        self.parent_path = parent_path

    def transform(self, path, feature=None):
        """
        Reads from NRRD image path

        Args:
            path: path of the NRRD image
            feature: Auxiliary data that may be used by the image reader

        Returns:
           Image as numpy array
        """
        path = os.path.normpath(os.path.join(self.parent_path, path))
        img = self.transform_fn(path)
        data = img.get_fdata()
        return data


class DicomReader(AbstractPreprocessing):
    """Class for reading dicom images

    Args:
        parent_path (str): Parent path that will be added on given path.
    """

    def __init__(self, parent_path=""):
        import pydicom
        self.transform_fn = pydicom.dcmread
        self.parent_path = parent_path

    def transform(self, path, feature=None):
        """
        Reads from Dicom image path

        Args:
            path: Path of the dicom image.
            feature: Auxiliary data that may be used by the image reader.

        Returns:
           Image as numpy array
        """
        path = os.path.normpath(os.path.join(self.parent_path, path))
        img = self.transform_fn(path, force=True)
        data = img.pixel_array
        return data.T


class ImageReader(AbstractPreprocessing):
    """
    Class for reading png or jpg images

    Args:
        parent_path: Parent path that will be added on given path
        grey_scale: Boolean to indicate whether or not to read image as grayscale
    """

    def __init__(self, parent_path="", grey_scale=False):
        import cv2
        self.transform_fn = cv2.imread
        self.parent_path = parent_path
        self.color_flag = cv2.IMREAD_COLOR
        if grey_scale:
            self.color_flag = cv2.IMREAD_GRAYSCALE

    def transform(self, path, feature=None):
        """
        Reads numpy array from image path

        Args:
            path: path of the image
            feature: Auxiliary data that may be used by the image reader

        Returns:
           Image as numpy array
        """
        path = os.path.normpath(os.path.join(self.parent_path, path))
        data = self.transform_fn(path, self.color_flag)
        if not isinstance(data, np.ndarray):
            raise ValueError('cv2 did not read correctly for file "{}"'.format(path))
        return data


class Zscore(AbstractPreprocessing):
    """
    Standardize data using zscore method
    """

    def transform(self, data, feature=None):
        """
        Standardizes the data

        Args:
            data: Data to be standardized
            feature: Auxiliary data needed for the standardization

        Returns:
            Array containing standardized data
        """
        mean = np.mean(data)
        std = np.std(data)
        data = (data - mean) / np.amax([std, EPSILON])
        data = data.astype(np.float32)
        return data


class Minmax(AbstractPreprocessing):
    """
    Normalize data using the minmax method
    """

    def transform(self, data, feature=None):
        """
        Normalizes the data

        Args:
            data: Data to be normalized
            feature: Auxiliary data needed for the normalization

        Returns:
            Normalized numpy array
        """
        data = data.astype(np.float32)
        data = data - np.amin(data[:])
        data = data / (np.amax(data[:]) + EPSILON)
        return data


class Scale(AbstractPreprocessing):
    """
    Preprocessing class for scaling dataset

    Args:
        scalar: Scalar for scaling the data
    """

    def __init__(self, scalar):
        self.scalar = scalar

    def transform(self, data, feature=None):
        """
        Scales the data tensor

        Args:
            data: Data to be scaled
            feature: Auxiliary data needed for the normalization

        Returns:
            Scaled data array
        """
        data = data.astype(np.float32)
        data = self.scalar * data
        return data


class Onehot(AbstractPreprocessing):
    """
    Preprocessing class for converting categorical labels to onehot encoding

    Args:
        num_dim: Number of dimensions of the labels
    """

    def __init__(self, num_dim):
        self.num_dim = num_dim

    def transform(self, data, feature=None):
        """
        Transforms categorical labels to onehot encodings

        Args:
            data: Data to be preprocessed
            feature: Auxiliary data needed for the preprocessing

        Returns:
            Transformed labels
        """
        data = data.astype(np.int32)
        res = np.zeros((len(data), self.num_dim))
        res[np.arange(len(data)), data] = 1
        return res


class Resize(AbstractPreprocessing):
    """Resize image.

    Args:
        target_size (tuple): Target image size in (height, width) format.
        resize_method (string): `bilinear`, `nearest`, `area`, and `lanczos4` are available.
        keep_ratio (bool): If `True`, the resulting image will be padded to keep the original aspect ratio.

    Returns:
        Resized `np.ndarray`.
    """

    def __init__(self, target_size, resize_method='bilinear', keep_ratio=False):
        import cv2
        self._cv2 = cv2

        self.target_size = target_size
        if resize_method == "bilinear":
            self.resize_method = cv2.INTER_LINEAR
        elif resize_method == "nearest":
            self.resize_method = cv2.INTER_NEAREST
        elif resize_method == "area":
            self.resize_method = cv2.INTER_AREA
        elif resize_method == "lanczos4":
            self.resize_method = cv2.INTER_LANCZOS4
        self.keep_ratio = keep_ratio

    def transform(self, data, feature=None):
        if self.keep_ratio:
            original_ratio = data.shape[1] / data.shape[0]
            target_ratio = self.target_size[1] / self.target_size[0]

            if original_ratio >= target_ratio:
                pad = (data.shape[1] / target_ratio - data.shape[0]) / 2
                pad_boarder = (np.ceil(pad).astype(np.int), np.floor(pad).astype(np.int), 0, 0)
            else:
                pad = (data.shape[0] * target_ratio - data.shape[1]) / 2
                pad_boarder = (0, 0, np.ceil(pad).astype(np.int), np.floor(pad).astype(np.int))

            data = self._cv2.copyMakeBorder(data, *pad_boarder, self._cv2.BORDER_CONSTANT)

        im_resized = self._cv2.resize(data, (self.target_size[1], self.target_size[0]), self.resize_method)
        return im_resized


class Reshape(AbstractPreprocessing):
    """
    Preprocessing class for reshaping the data

    Args:
        shape: target shape
    """

    def __init__(self, shape):
        self.shape = shape

    def transform(self, data, feature=None):
        """
        Reshapes data array

        Args:
            data: Data to be reshaped
            feature: Auxiliary data needed for the reshaping

        Returns:
            Reshaped array
        """
        data = np.reshape(data, self.shape)
        return data
