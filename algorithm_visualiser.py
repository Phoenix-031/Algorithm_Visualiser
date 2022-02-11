import random
import pygame

pygame.init()

class game:

    BLCK = 0,0,0
    WHT = 255,255,255
    GRN = 0,255,0
    RED = 255,0,0

    SHADES_GRAY = [
        (128,128,128),
        (160,160,160),
        (192,192,192)
    ]

    pads = 100
    padt = 200

    FONT = pygame.font.SysFont('comicsans',20)
    
    def __init__(self,width,height,lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Algorithm's Visualiser")
        self.calc_list(lst)
        
    def calc_list(self,lst):
        self.lst = lst
        self.max_v = max(lst)
        self.min_v = min(lst)

        self.bar_width = int((self.width - self.pads)/len(lst))
        self.bar_height = int((self.height - self.padt)/(self.max_v - self.min_v))
        self.start_x = self.pads//2


def genrate_list(n,max,min):
    lst = []
    for _ in range(n):
        val = random.randint(min,max)
        lst.append(val)

    return lst


def draw_screen(game_ins,algo_name,ascending):
    game_ins.window.fill(game_ins.WHT)

    algo_n = game_ins.FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}" ,1,game_ins.RED)
    game_ins.window.blit(algo_n, (100,3))

    ptext = game_ins.FONT.render("R - reset | SPACE - start sorting | A - ascending | D - descending",1,game_ins.BLCK)
    game_ins.window.blit(ptext , (100,40))

    atext = game_ins.FONT.render("B - Bubble Sort | S - Selection Sort | I - Instertion Sort",1,game_ins.BLCK)
    game_ins.window.blit(atext , (100,70))

    draw_bar(game_ins)
    pygame.display.update()



def draw_bar(game_ins,color_b ={},clear_bg = 0):
    list_val = game_ins.lst
    
    if clear_bg:
        c_rect = (game_ins.start_x // 2, game_ins.padt, game_ins.width - game_ins.pads, game_ins.height)
        pygame.draw.rect(game_ins.window,game_ins.WHT,c_rect)

    for i,val in enumerate(list_val):

        x = game_ins.start_x + game_ins.bar_width * i
        y = game_ins.height - (val - game_ins.min_v)* game_ins.bar_height

        color = game_ins.SHADES_GRAY[i%3]

        if i in color_b:
            color = color_b[i]

        pygame.draw.rect(game_ins.window, color, (x,y,game_ins.bar_width,game_ins.height))
    
    if clear_bg:
        pygame.display.update()



def bubble_sort(game_ins,ascending):
    lst  = game_ins.lst

    for i in range(len(lst) -1):
        for j in range(len(lst) -i -1):
            if (lst[j] > lst[j+1] and ascending) or (lst[j] < lst[j+1] and not ascending):
                lst[j],lst[j+1] = lst[j+1],lst[j]
                draw_bar(game_ins,{j: game_ins.GRN, j+1 : game_ins.RED}, 1)
                yield True

    return lst

def selection_sort(game_ins,ascending):
    lst = game_ins.lst

    for i in range(len(lst) - 1):
        indx = i
        for j in range(i+1, len(lst)):
            if (lst[j] < lst[indx] and ascending) or (lst[j] > lst[indx] and not ascending):
                indx = j

        lst[i],lst[indx] = lst[indx],lst[i]
        draw_bar(game_ins,{i: game_ins.GRN, min : game_ins.RED}, 1)
        yield True
        
    return lst

def insertion_sort(game_ins,ascending):
    lst = game_ins.lst

    for i in range(1,len(lst)):
        min = lst[i]
        j=i-1
        while (j >=0 and min < lst[j] and ascending) or (j>=0 and min > lst[j] and not ascending):
            lst[j+1] = lst[j]
            lst[j] = min
            j-=1
       
        draw_bar(game_ins,{min: game_ins.GRN, j : game_ins.RED}, 1)
        yield True

    return lst


def main():
    n=100
    max_val = 400
    min_val = 0
    lst = genrate_list(n,max_val,min_val)
    game_ins = game(1280,700,lst)
    clock = pygame.time.Clock()
    
    sorting = 0
    ascending = 1

    sorting_algo = bubble_sort
    algo_name = None
    algo_gen = None

    run = 1

    while run:
        clock.tick(50)
        if sorting:
            try:
                next(algo_gen)
            except StopIteration:
                sorting = 0

        else:
            draw_screen(game_ins,algo_name,ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    lst = genrate_list(n,max_val,min_val)
                    game_ins.calc_list(lst)
                    sorting = 0

                elif event.key == pygame.K_SPACE and sorting == 0:
                    sorting = 1
                    algo_gen = sorting_algo(game_ins,ascending)

                elif event.key == pygame.K_a and sorting == 0:
                    ascending = 1

                elif event.key == pygame.K_d and sorting == 0:
                    ascending = 0

                elif event.key == pygame.K_i and sorting == 0:
                    sorting_algo = insertion_sort
                    algo_name = "Insertion Sort"
                
                elif event.key == pygame.K_s and sorting == 0:
                    sorting_algo = selection_sort
                    algo_name = "Selection Sort"
                
                elif event.key == pygame.K_b and sorting == 0:
                    sorting_algo = bubble_sort
                    algo_name = "Bubble Sort"
                
                elif event.key == pygame.K_m and sorting == 0:
                    pass

                elif event.key == pygame.K_q and sorting == 0:
                    pass

                


    pygame.quit()


if __name__ == '__main__':
    main()
    
