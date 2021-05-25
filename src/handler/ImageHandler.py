# -*- coding: utf-8 -*-

from PIL import Image, ImageQt, ImageOps


class ImageHandler:
    ZOOM_RATIO: tuple = (0, 0, 128, 128)

    __ratioOriginalToInterface: tuple
    __tempImage: Image = None
    __in_zoom: bool = False
    __interfaceImage: Image
    __originalImage: Image
    __filename: str
    __imageSize: tuple = (1280, 720)

    def __init__(self, filename: str):
        self.__filename = filename
        with Image.open(filename) as image:
            self.__originalImage = image.copy()
            self.normalize(image)

    def get_image(self, original: bool = False) -> Image:
        return self.__originalImage if original else self.__interfaceImage

    def get_qt_image(self, original: bool = False) -> ImageQt:
        return ImageQt.toqimage(self.normalize(self.__originalImage)) \
            if original else ImageQt.toqimage(self.__interfaceImage)

    def get_file_path(self) -> str:
        return self.__filename

    def set_image_size(self, size: tuple = (1280, 720)) -> None:
        self.__imageSize = size

    def get_image_size(self) -> tuple:
        return self.__interfaceImage.size

    def normalize(self, image: Image) -> Image:
        ratio = (
            image.width // self.__imageSize[0],
            image.height // self.__imageSize[1]
        )
        self.__ratioOriginalToInterface = (
            1 if ratio[0] < 1 else ratio[0],
            1 if ratio[1] < 1 else ratio[1]
        )

        self.__interfaceImage = image.resize(
            self.__imageSize if ratio[0] > 1 and ratio[1] > 1 else image.size
        )

        return self.__interfaceImage

    def zoom_in(self, region: tuple = (0, 0)) -> Image:
        self.temporary_image(True)
        zoom_region = (
            self.ZOOM_RATIO[0] + region[0], self.ZOOM_RATIO[1] + region[1],
            self.ZOOM_RATIO[2] + region[0], self.ZOOM_RATIO[3] + region[1]
        )
        self.__interfaceImage = self.__interfaceImage.crop(zoom_region).resize((128*5, 128*5))

        return self.__interfaceImage

    def zoom_out(self) -> Image:
        self.temporary_image(False)
        return self.__interfaceImage

    def gray_scale(self, scale: int) -> Image:
        self.temporary_image(True)
        self.__interfaceImage = self.__interfaceImage.quantize(scale)
        return self.__interfaceImage

    def new_resolution(self, new_size: int) -> Image:
        if new_size == 32 or new_size == 64:
            self.temporary_image(True)
            self.__interfaceImage = self.__interfaceImage.resize((new_size, new_size))
        return self.__interfaceImage

    def equalize(self) -> Image:
        self.__interfaceImage = ImageOps.equalize(self.__interfaceImage)
        return self.__interfaceImage

    def temporary_image(self, is_zoom: bool) -> None:
        if self.__tempImage is None and is_zoom:
            self.__tempImage = self.__interfaceImage.copy()
            self.__in_zoom = True
        else:
            if self.__tempImage is not None and is_zoom:
                self.__interfaceImage = self.__tempImage.copy()
            else:
                self.normalize(self.__originalImage)
            self.__tempImage = None
            self.__in_zoom = False

    def get_info(self) -> None:
        print('\nAttributes viewed image\n'
              f'Image resolution:     {self.__interfaceImage.size}\n'
              f'Columns:              {self.__interfaceImage.width}\n'
              f'Rows:                 {self.__interfaceImage.height}\n'
              f'File type:            {self.__interfaceImage.format}\n'
              f'Image type:           {self.__interfaceImage.mode}'
              )
        print('\nAttributes original image\n'
              f'Image resolution:     {self.__originalImage.size}\n'
              f'Columns:              {self.__originalImage.width}\n'
              f'Rows:                 {self.__originalImage.height}\n'
              f'File type:            {self.__originalImage.format}\n'
              f'Image type:           {self.__originalImage.mode}'
              )
        print('\nRatio among original image and interface image\n'
              f'Width ratio:  {self.__ratioOriginalToInterface[0]}\n'
              f'Height ratio: {self.__ratioOriginalToInterface[1]}\n'
              )

    def close(self) -> None:
        self.__interfaceImage.close()
        self.__originalImage.close()
        if self.__tempImage is not None:
            self.__tempImage.close()
