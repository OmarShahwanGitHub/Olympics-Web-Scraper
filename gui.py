import pygame
import sys
import webscraper
import country_converter as coco

pygame.init()

SW, SH = 1600, 900

screen = pygame.display.set_mode((SW, SH))

BG = pygame.image.load("assets/background.png") 

# We store the countries with their info as a dictionary from the webscraper's function
COUNTRIES = {}

COUNTRIES = webscraper.generate_data()

pygame.display.set_caption("Olympics")
pygame.display.set_icon(pygame.image.load("assets/icon_image.png"))

# Function for making the font at the designated size.

font = pygame.font.Font("assets/RobotoCondensed-Bold.ttf", 60)

ALL_DATA = []

# Creation of all the rows of data along with the information in them.

def generate_surfaces():
    for i, country_name in enumerate(COUNTRIES): #loop through each country to create their rows 
        ALL_DATA.append([pygame.image.load("assets/empty rect.png"), (200, i*125+175)]) 
        if country_name != "ROC":
            abb = font.render(coco.convert(names=country_name, to='name_short'), True, "white") #abbreviating country names using country_converter library
        else: #abbreviate Russian Olympic Committee as its too long
            abb = font.render("ROC", True, "white")
        
        #appending the country abbreviations and medals-won data of each country
        ALL_DATA.append([abb, (210, i*125+185)])
        gold = font.render(str(COUNTRIES[country_name]["gold"]), True, "white")
        ALL_DATA.append([gold, (625, i*125+185)])
        silver = font.render(str(COUNTRIES[country_name]["silver"]), True, "white")
        ALL_DATA.append([silver, (925, i*125+185)])
        bronze = font.render(str(COUNTRIES[country_name]["bronze"]), True, "white")
        ALL_DATA.append([bronze, (1225, i*125+185)])

generate_surfaces()


#Scrolling logic using arrow keys or mouse wheel
scroll_speed = 50  # Adjust this value to change scroll speed
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pos()[0] in range(200, 440) and pygame.mouse.get_pos()[1] in range(50, 145):
                if showing_countries:
                    showing_countries = False
                    ALL_DATA = []
                else:
                    showing_countries = True
                    generate_surfaces()
            
            # Mouse wheel scrolling
            if event.button == 4:  # Scroll up
                if ALL_DATA[0][1][1] < 175:
                    for surface in ALL_DATA:
                        new_rect = (surface[1][0], surface[1][1] + scroll_speed) #surface[1][1] is the y coordinate of the data, [1][0] is the x
                        surface[1] = new_rect
            elif event.button == 5:  # Scroll down
                if ALL_DATA[-1][1][1] > SH - 100: #stop scrolling after passing last row
                    for surface in ALL_DATA:
                        new_rect = (surface[1][0], surface[1][1] - scroll_speed)
                        surface[1] = new_rect

    # Keyboard scrolling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        if ALL_DATA[-1][1][1] > SH - 100:
            for surface in ALL_DATA:
                new_rect = (surface[1][0], surface[1][1] - 20)
                surface[1] = new_rect
    if keys[pygame.K_UP]:
        if ALL_DATA[0][1][1] < 175:
            for surface in ALL_DATA:
                new_rect = (surface[1][0], surface[1][1] + 20)
                surface[1] = new_rect
    
    screen.blit(BG, (0, 0))
    
    # Blitting info on the screen
    for i in range(0, len(ALL_DATA), 5):  # Iterate over groups of 5 (empty row + 4 pieces of data)
        rect = ALL_DATA[i] #empty rect of each row is assigned here
        if 100 <= rect[1][1] <= SH:  # Check if the rect is on screen (y coordinate is in rect[1][1])
            for j in range(5):  # Render the rect and its associated data
                surface = ALL_DATA[i + j] #accesses each medal within the empty rect's data group
                screen.blit(surface[0], surface[1])
    
    # Blitting titles for Country, Gold, Silver, Bronze
    screen.blit(pygame.image.load("assets/country V2.png"), (200, 50))
    screen.blit(pygame.image.load("assets/gold V2.png"), (525, 50))
    screen.blit(pygame.image.load("assets/silver V2.png"), (825, 50))
    screen.blit(pygame.image.load("assets/bronze V2.png"), (1125, 50))
    
    pygame.display.update()