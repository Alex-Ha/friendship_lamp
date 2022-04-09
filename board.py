from unicornhatmini import UnicornHATMini
from gpiozero import Button
from data.pixel_art_matrices import battery as battery_matrix
import time

class Board:
    button_map = {
        5: "A",
        6: "B",
        16: "X",
        24: "Y"
    }

    def __init__(self):
        """
        This board is based off of the Pimoroni Unicorn HAT, a 17x7 Matrix with WS2812 LEDs. 
        https://shop.pimoroni.com/products/unicorn-hat?variant=932565325

        """
        self.width                  =   17
        self.height                 =   7 
        self.brightness_level       =   0.25
        self.client                 =   UnicornHATMini()

        self.client.set_brightness(self.brightness_level)

        self.button_a = Button(5)
        self.button_b = Button(6)
        self.button_x = Button(16)
        self.button_y = Button(24)

        self.button_a.when_pressed = self.pressed
        self.button_b.when_pressed = self.pressed
        self.button_x.when_pressed = self.pressed
        self.button_y.when_pressed = self.pressed
        
        # self.boot_up()

    def boot_up(self):
        """
        Pretty useless, but felt like adding a progress bar to show that the board is booting up.
        Open to different visuals here.
        """
        self.client.clear()

        while True:
            for x, row in enumerate(battery_matrix):
                for y, pixel in enumerate(row):
                    self.client.set_pixel(x, y, pixel[0], pixel[1], pixel[2])

            self.client.show()

            for col_num in range(self.width):
                if(col_num % 2) != 0:
                    continue
                
                self.client.set_pixel(col_num, 2, 255, 255, 255)
                self.client.set_pixel(col_num, 3, 255, 255, 255)
                self.client.set_pixel(col_num, 4, 255, 255, 255)

                self.client.show()

                time.sleep(.25)
            
            time.sleep(2)
            break

        self.client.clear()
    
    def display_scrolling_art(self, pixel_art_matrix=[[]]) -> None:
        """
        Display pixel art in scrolling form from right to left.

        :param 2DMatrix pixel_art_matrix    A 17x6 matrix with each cell (or pixel) being an RGB value. 
                                            The RGB value will be an array of three values from 0 to 255.
        """
        current_col = self.width

        ## This will run until the pixel art reaches the left edge of the board.
        while True:
            self.client.clear()
            to_display = pixel_art_matrix[:self.width - current_col]

            for col_num, col in enumerate(to_display):
                for row_num, pixel in enumerate(col):
                    self.client.set_pixel(
                        col_num + current_col, 
                        row_num, 
                        pixel[0], 
                        pixel[1], 
                        pixel[2]
                    )

            self.client.show()

            if(current_col == 0):
                break

            current_col -= 1
            time.sleep(.1)

        ## This will run until we reach the end of the pixel art matrix.
        while True:
            self.client.clear()

            if(current_col >= len(pixel_art_matrix)):
                break

            to_display = pixel_art_matrix[current_col:self.width+current_col]

            for x, col in enumerate(to_display):
                for y, pixel in enumerate(col):
                    self.client.set_pixel(
                        x, 
                        y, 
                        pixel[0], 
                        pixel[1], 
                        pixel[2]
                    )

            self.client.show()

            current_col += 1
            time.sleep(.1)
        
        self.client.clear()

    def display_art(self, pixel_art_matrix=[[]]) -> None:
        """
        Display pixel art.

        :param 2DMatrix pixel_art_matrix    A 17x6 matrix with each cell (or pixel) being an RGB value. 
                                            The RGB value will be an array of three values from 0 to 255.  
        """

        to_display = pixel_art_matrix if(len(pixel_art_matrix) <= self.width) else pixel_art_matrix[:self.width]

        self.client.clear()

        for x, col in enumerate(to_display):
            for y, pixel in enumerate(col):
                self.client.set_pixel(
                    x, 
                    y, 
                    pixel[0], 
                    pixel[1], 
                    pixel[2]
                )

        self.client.show()

        time.sleep(1)
        
        self.client.clear()

    def display_animation(self, pixel_art_matrices=[[]]) -> None:
        """
        Display pixel animation, aka GIFs.

        :param 2DMatrix pixel_art_matrices  An array of 17x6 matrices with each cell (or pixel) being an RGB value. 
                                            The RGB value will be an array of three values from 0 to 255.
        """
        counter = 0

        while counter < 5:
            for pixel_art_matrix in pixel_art_matrices:
                to_display = pixel_art_matrix if(len(pixel_art_matrix) <= self.width) else pixel_art_matrix[:self.width]

                self.client.clear()

                for x, col in enumerate(to_display):
                    for y, pixel in enumerate(col):
                        self.client.set_pixel(
                            x, 
                            y, 
                            pixel[0], 
                            pixel[1], 
                            pixel[2]
                        )

                self.client.show()

                time.sleep(.1)
                
                self.client.clear()

            counter += 1

    def pressed(self, button):
        """
        https://github.com/pimoroni/unicornhatmini-python/blob/master/examples/buttons.py

        Unsure of what to do with buttons yet. For now, it'll just log that you pressed the button.
        """
        button_name = self.button_map[button.pin.number]
        print(f"Button {button_name} pressed!")