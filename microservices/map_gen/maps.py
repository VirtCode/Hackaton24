import svg
import json
import logging
import copy
import os

class Map():
    def __init__(self, path) -> None:
        self.size_x = 0
        self.size_y = 0

        try:
            with open(path, 'r') as file:
                data = json.load(file)

            with open('resources/styling.json', 'r') as stylefile:
                self.style = json.load(stylefile)


            for element in data['floor'][0]['objects']:
                if self.size_x < element['x'] + element['width']:
                    self.size_x = element['x'] + element['width']

                if self.size_y < element['y'] + element['height']:
                    self.size_y = element['y'] + element['height']

            # we adjust the viewport dnymically
            self.inner_x = 10
            self.inner_y = 10
            self.inner_width = self.size_x
            self.inner_height = self.size_y

            # padding
            self.size_x += 20
            self.size_y += 20

            self.container = svg.G(elements=[], class_ = ["container"])
            self.svgMap = svg.SVG(viewBox=f'0 0 {self.size_x} {self.size_y}', elements=[self.container])

            for element in data['floor'][0]['objects']:
                current = self.style[element['class']]

                if (element['type'] == 1): # RECT
                    self.container.elements.append(svg.Rect(
                        class_=element['class'],
                        x=element['x'] + 10, # again, padding
                        y=element['y'] + 10,
                        width=element['width'],
                        height=element['height'],

                        fill=current['fill_color'],
                        fill_opacity=current['fill_opacity'],
                        stroke=current['stroke_color'],
                        stroke_width=current['stroke_width'],
                        rx=current['border_radius'],
                        ry=current['border_radius']
                    ))
        except:
            logging.error(f'No file with name: {path} found!')

    def createRect(self, className, start_x, start_y, width, height, fill_color, opacity, stroke_color = "BLACK", stroke_width = 0):
       return svg.Rect(class_=className, x=start_x, y=start_y, width=width, height=height, fill=fill_color, fill_opacity=opacity, stroke=stroke_color, stroke_width=stroke_width)

def calcTableX(relTableX, tableAreaWidth, innerX, innerWidth):
    return innerX + (innerWidth / tableAreaWidth) * relTableX

def calcTableY(relTableY, tableAreaHeight, innerY, innerHeight):
    return calcTableX(relTableY, tableAreaHeight, innerY, innerHeight)

def calcTableWidth(relTableWidth, tableAreaWidth, innerWidth):
    return (innerWidth / tableAreaWidth) * relTableWidth

def calcTableHeight(relTableHeight, tableAreaHeight, innerHeight):
    return calcTableWidth(relTableHeight, tableAreaHeight, innerHeight)

def addTables(myMap, jsonData, highlight = None):

    table_start_x = jsonData['x']
    table_start_y = jsonData['y']
    table_area_width = jsonData['width']
    table_area_height = jsonData['height']
    tables_data = jsonData['tables']

    center_x = 0
    center_y = 0
    center_magnitude = 0

    for entry in tables_data:

        if highlight and entry['id'] == highlight:
            current = myMap.style['highlight']
            center_x = calcTableX(entry['x'] + (entry['width'] / 2), table_area_width, myMap.inner_x, myMap.inner_width)
            center_y = calcTableY(entry['y'] + (entry['height'] / 2), table_area_height, myMap.inner_y, myMap.inner_height)

            mag_test = calcTableWidth(entry['width'], table_area_width, myMap.inner_width)
            if center_magnitude < mag_test:
                center_magnitude = mag_test
            mag_test = calcTableHeight(entry['height'], table_area_height, myMap.inner_height)
            if center_magnitude < mag_test:
                center_magnitude = mag_test
        else:
            current = myMap.style['table']

        table = svg.Rect(
            id = entry['id'],
            class_ = ["table"],
            x = calcTableX(entry['x'], table_area_width, myMap.inner_x, myMap.inner_width),
            y = calcTableY(entry['y'], table_area_height, myMap.inner_y, myMap.inner_height),
            width=calcTableWidth(entry['width'], table_area_width, myMap.inner_width),
            height=calcTableHeight(entry['height'], table_area_height, myMap.inner_height),

            fill=current['fill_color'],
            fill_opacity=current['fill_opacity'],
            stroke=current['stroke_color'],
            stroke_width=current['stroke_width'],
            rx=current['border_radius'],
            ry=current['border_radius']
       )

        myMap.container.elements.append(table)

    # doesn't work for some fucking reason, viewbox seems to be broken
    if highlight and False:
        print(center_x)
        print(center_y)

        myMap.container.elements.append(svg.Rect(x = center_x, y = center_y, width = 10, height = 10, fill = "RED"))

        center_magnitude = 100
        myMap.svgMap.viewBox = f'{center_x - center_magnitude} {center_y - center_magnitude} {center_x + center_magnitude} {center_y + center_magnitude}'

    return myMap
