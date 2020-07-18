import os
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import pyscreenshot as screenshot
import cv2
import numpy
import pyautogui
from pynput.keyboard import Key, Listener


def capture_region(region):
    capture = screenshot.grab(region)
    #return numpy.array(capture)
    return cv2.cvtColor(numpy.array(capture), cv2.COLOR_RGB2BGR)


def cash_cow(region):
    print('Starting Cash Cow...')
    colors = [sRGBColor(13, 233, 242, True), sRGBColor(73, 55, 254, True), sRGBColor(254, 115, 3, True), sRGBColor(60, 220, 73, True), sRGBColor(23, 139, 249, True)]
    replay_template = cv2.cvtColor(cv2.imread('CashCow/Replay.png'), cv2.COLOR_BGR2GRAY)
    play_game_template = cv2.cvtColor(cv2.imread('CashCow/PlayGame.png'), cv2.COLOR_BGR2GRAY)
    add_row_template = cv2.cvtColor(cv2.imread('CashCow/AddRow.png'), cv2.COLOR_BGR2GRAY)
    grid_top_left_template = cv2.cvtColor(cv2.imread('CashCow/GridTopLeft.png'), cv2.COLOR_BGR2GRAY)
    grid_bottom_right_template = cv2.cvtColor(cv2.imread('CashCow/GridBottomRight.png'), cv2.COLOR_BGR2GRAY)
    starting = True
    while starting:
        capture = capture_region(region)
        capture_gray = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)
        #draw_matches(capture, play_game_template, find_in_image(capture_gray, play_game_template, 0.6))
        #cv2.imwrite('game.png', capture)
        for pt in find_in_image(capture_gray, play_game_template, 0.8):
            h, w = play_game_template.shape
            pyautogui.leftClick(region[0] + pt[0] + w / 2, region[1] + pt[1] + h / 2)
            starting = False
            break
    print('Finding grid bounds...')
    bounds = None
    milk_size = None
    while True:
        capture = capture_region(region)
        capture_gray = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)
        matches_down_right = find_in_image(capture_gray, grid_bottom_right_template, 0.9)
        matches_up_left = find_in_image(capture_gray, grid_top_left_template, 0.9)
        #draw_matches(capture, grid_bottom_right_template, matches_down_right)
        #draw_matches(capture, grid_top_left_template, matches_up_left)
        #cv2.imwrite('game.png', capture)

        down_right = None
        for pt in matches_down_right:
            down_right = pt
            break
        up_left = None
        for pt in matches_up_left:
            up_left = pt
            break
        if down_right is not None and up_left is not None:
            print('Found bounds for grid')
            h, w = grid_top_left_template.shape
            bounds = up_left[0] + w, up_left[1] + h, down_right[0], down_right[1]
            milk_size = (bounds[2] - bounds[0]) / 10, (bounds[3] - bounds[1]) / 12
            break
        print('Couldn\'t find bounds, trying again...')

    while True:
        #print('Start: -----------------------------------------')
        capture = capture_region(region)
        capture_gray = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)
        #draw_matches(capture, milk_template, find_in_image(capture_gray, milk_template, 0.6))
        #cv2.imwrite('game.png', capture)

        #for pt in find_in_image(capture_gray, milk_template, 0.6):
        #    print(pt)
        #print(bounds)
        cv2.rectangle(capture, (bounds[0], bounds[1]), (bounds[2], bounds[3]), (0, 0, 255), 2)
        grid = []
        for i in range(0, 10):
            column = []
            for j in range(0, 12):
                x = int(bounds[0] + milk_size[0] / 2 + milk_size[0] * i)
                y = int(bounds[1] + milk_size[1] / 2 + milk_size[1] * j)
                #print('')
                pixel = capture[y][x]
                #print(i)
                #print(j)
                #print(x)
                #print(y)
                #print(pixel)
                color = None
                for c in colors:
                    if delta_e_cie2000(convert_color(c, LabColor), convert_color(sRGBColor(pixel[0], pixel[1], pixel[2], True), LabColor)) < 1:
                        color = c
                        #print(c)
                    #print(delta_e_cie2000(convert_color(c, LabColor), convert_color(sRGBColor(pixel[0], pixel[1], pixel[2], True), LabColor)))
                column.append(color)
                cv2.rectangle(capture, (x - 10, y - 10), (x + 10, y + 10), (0, 0, 0), 2)
            #print(column)
            grid.append(column)

        indices = [[-1 for i in range(12)] for j in range(10)]
        index = 0
        matches = []

        # for x in range(0, 10):
        # print('')
        # for y in range(0, 12):
        # print(grid[i][j])
        # if grid[i][j] is not None:
        # capture[j][i] = grid[i][j].get_upscaled_value_tuple()

        def search(x, y, i):
            indices[x][y] = i
            count = 1
            if x > 0 and indices[x - 1][y] == -1 and grid[x][y] == grid[x - 1][y]:
                count += search(x - 1, y, i)
            if y > 0 and indices[x][y - 1] == -1 and grid[x][y] == grid[x][y - 1]:
                count += search(x, y - 1, i)
            if x < 9 and indices[x + 1][y] == -1 and grid[x][y] == grid[x + 1][y]:
                count += search(x + 1, y, i)
            if y < 11 and indices[x][y + 1] == -1 and grid[x][y] == grid[x][y + 1]:
                count += search(x, y + 1, i)
            return count

        for x in range(0, 10):
            for y in range(0, 12):
                if indices[x][y] != -1 or grid[x][y] is None:
                    continue
                count = search(x, y, index)
                if count > 2:
                    matches.append(((x, y), count))
                index += 1
        #print(index)
        #print(matches)

        highest = None
        highest_coords = None
        for coords, count in matches:
            if highest is None or count > highest:
                highest = count
                highest_coords = coords

        #print(highest_coords)
        #print(highest)

        if highest_coords is not None:
            pyautogui.leftClick(region[0] + bounds[0] + milk_size[0] / 2 + milk_size[0] * highest_coords[0], region[1] + bounds[1] + milk_size[1] / 2 + milk_size[1] * highest_coords[1])
            #time.sleep(5)
        else:
            for pt in find_in_image(capture_gray, add_row_template, 0.8):
                h, w = add_row_template.shape
                pyautogui.leftClick(region[0] + pt[0] + w / 2, region[1] + pt[1] + h / 2)
                break

        #cv2.imwrite('game.png', capture)
        #print(bounds)
        #print(milk_size)
        #print(x)
        #print(y)

        for pt in find_in_image(capture_gray, play_game_template, 0.8):
            h, w = play_game_template.shape
            pyautogui.leftClick(region[0] + pt[0] + w / 2, region[1] + pt[1] + h / 2)
            break

        for pt in find_in_image(capture_gray, replay_template, 0.8):
            h, w = replay_template.shape
            pyautogui.leftClick(region[0] + pt[0] + w / 2, region[1] + pt[1] + h / 2)
            break


games = {'CashCow.png': cash_cow}


def determine_game(region):
    print('Determining game...')
    while True:
        capture = capture_region(region)
        capture_gray = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('game.png', capture)
        for image, game in games.items():
            template = cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2GRAY)
            for _ in find_in_image(capture_gray, template):
                print('Found game!')
                return game
        print('Didn\'t successfully determine game, trying again...')


def find_in_image(image, template, threshold=0.8):
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    loc = numpy.where(res >= threshold)
    return zip(*loc[::-1])


def draw_matches(image, template, matches):
    h, w = template.shape
    for pt in matches:
        cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)


def locate_game():
    print('Locating game window...')
    template_down_right = cv2.imread("GameBoundDownRight.png")
    template_down_right_gray = cv2.cvtColor(template_down_right, cv2.COLOR_BGR2GRAY)
    template_up_left = cv2.imread("GameBoundTopLeft.png")
    template_up_left_gray = cv2.cvtColor(template_up_left, cv2.COLOR_BGR2GRAY)
    while True:
        screen = screenshot.grab()
        image = cv2.cvtColor(numpy.array(screen), cv2.COLOR_RGB2BGR)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        matches_down_right = find_in_image(image_gray, template_down_right_gray, 0.9)
        matches_up_left = find_in_image(image_gray, template_up_left_gray, 0.9)
        #draw_matches(image, template_down_right_gray, matches_down_right)
        #draw_matches(image, template_up_left_gray, matches_up_left)
        #cv2.imwrite('game.png', image)

        down_right = None
        for pt in matches_down_right:
            down_right = pt
            break
        up_left = None
        for pt in matches_up_left:
            up_left = pt
            break
        if down_right is not None and up_left is not None:
            h, w = template_up_left_gray.shape
            print('Located game window!')
            return up_left[0] + w, up_left[1] + h, down_right[0], down_right[1]
        print('Couldn\'t find window, trying again...')


if __name__ == '__main__':
    def on_press(key):
        if key == Key.esc:
            os._exit(69)

    Listener(on_press=on_press).start()

    game_region = locate_game()
    determine_game(game_region)(game_region)
