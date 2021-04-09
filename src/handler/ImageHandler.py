# -*- coding: utf-8 -*-

from PIL import Image, ImageFilter

class ImageHandler:

    IMAGE_SIZE: tuple = (1280, 720)
    ZOOM_RATIO: tuple = (0, 0, 128, 128)

    ratioOriginalToInterface: tuple
    interfaceImage: Image
    originalImage: Image
    tempImage: Image = None
    in_zoom: bool = False

    def __init__(self, filename: str):
        with Image.open(filename) as image:
            self.originalImage = image.copy()
            self.normalize(image)

    def get_image(self, original: bool = False) -> Image:
        return self.originalImage if original else self.interfaceImage 

    def normalize(self, image: Image):
        ratio = (
            image.width // self.IMAGE_SIZE[0],
            image.height // self.IMAGE_SIZE[1]
        )
        self.ratioOriginalToInterface = (
            1 if ratio[0] < 1 else ratio[0],
            1 if ratio[1] < 1 else ratio[1]
        )

        self.interfaceImage = image.resize(
            self.IMAGE_SIZE if ratio[0] > 1 and ratio[1] > 1 else image.size
        )

    def zoom_in(self, region: tuple=(0, 0)) -> Image:
        self.temporary_image(True)
        zoom_region = (
            self.ZOOM_RATIO[0] + region[0],
            self.ZOOM_RATIO[1] + region[1],
            self.ZOOM_RATIO[2] + region[0],
            self.ZOOM_RATIO[3] + region[1]
        )

        self.interfaceImage = self.interfaceImage.crop(zoom_region).resize(self.IMAGE_SIZE)
        return self.interfaceImage

    def zoom_out(self) -> Image:
        self.temporary_image(False)
        return self.interfaceImage

    def new_resolution(self, new_size: int) -> Image:
        if new_size == 32 or new_size == 64:
            self.temporary_image(True)
            self.interfaceImage = self.interfaceImage.resize((new_size, new_size))
        return self.interfaceImage

    def temporary_image(self, is_zoom: bool):
        if self.tempImage is None and is_zoom:
            self.tempImage = self.interfaceImage.copy()
            self.in_zoom = True
        else:
            if self.tempImage is not None:
                self.interfaceImage = self.tempImage.copy()
            else:
                self.normalize(self.originalImage)
            self.tempImage = None
            self.in_zoom = False

    def get_info(self):
        print('\nAttributes viewed image\n'
            f'Image resolution:     {self.interfaceImage.size}\n'
            f'Colunms:              {self.interfaceImage.width}\n'
            f'Rows:                 {self.interfaceImage.height}\n'
            f'File type:            {self.interfaceImage.format}\n'
            f'Image type:           {self.interfaceImage.mode}'
        )
        print('\nAttributes original image\n'
            f'Image resolution:     {self.originalImage.size}\n'
            f'Colunms:              {self.originalImage.width}\n'
            f'Rows:                 {self.originalImage.height}\n'
            f'File type:            {self.originalImage.format}\n'
            f'Image type:           {self.originalImage.mode}'
        )
        print('\nRatio among original image and interface image\n'
            f'Width ratio:  {self.ratioOriginalToInterface[0]}\n'
            f'Height ratio: {self.ratioOriginalToInterface[1]}\n')

    def close(self):
        self.interfaceImage.close()
        self.originalImage.close()
        if self.tempImage is not None:
            self.tempImage.close()