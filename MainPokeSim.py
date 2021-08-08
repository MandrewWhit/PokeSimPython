import pygame
import random as rnd
import os
import time as t
from Pokemon import Pokemon
from Button import Button
from Player import Player
from BattleBar import BattleBar
from HpMeter import HpMeter
from Moveset import Move


def main():

    # initialize game
    pygame.init()
    rnd.seed(os.urandom(2))


    # Setup app logo
    logo = pygame.image.load("plogo.png")

    # load red picture
    red = pygame.image.load("red.png")
    red = pygame.transform.scale(red, (100, 120))

    # Setup logo and caption
    main_logo = pygame.image.load("PokeSimLogo.png")
    main_logo = pygame.transform.scale(main_logo, (300, 100))
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Poke Sim")

    # Setup Clock
    clock = pygame.time.Clock()

    # create events
    start_event = pygame.USEREVENT + 1
    misty_event = pygame.USEREVENT + 2
    lapras_event = pygame.USEREVENT + 3
    hp_event = pygame.USEREVENT + 4
    move_event = pygame.USEREVENT + 5
    lapras_faint_event = pygame.USEREVENT + 6
    move_animation_event = pygame.USEREVENT + 7
    pika_faint_event = pygame.USEREVENT + 8
    pygame.time.set_timer(start_event, 1)

    # Setup display
    screen = pygame.display.set_mode((600, 600))
    screen.fill(pygame.Color(255, 255, 255))
    screen.blit(main_logo, (150, 50))
    pygame.display.flip()

    # miscellaneous variables
    running = True
    xloc = 500

    # initialize misty variables
    misty_xloc = 500
    misty_come = True
    misty_stay = False
    misty_leave = False
    misty_stay_count = 0
    start_bas = True
    misty = pygame.image.load("misty.png")
    misty = pygame.transform.scale(misty, (150, 120))

    # setup start screen buttons and music
    hit_sound_effect = pygame.mixer.Sound("lapras_cry.wav")
    create_buttons(screen)
    battle_music_start = True
    start_music = True
    music = True
    game_start = True

    # create player object
    player = Player(100, 100, "red_back.png")

    # create pikachu object
    pika_moves = [Move("Thunderbolt", True, 40, ["water", "flying"], ["ground"]),
                  Move("Iron Tail", True, 10, ["water", "flying"], ["ground"]),
                  Move("Tail Whip", True, 30, ["water", "flying"], ["ground"]),
                  Move("Electro Ball", True, 50, ["water", "flying"], ["ground"])]
    current_move = pika_moves[0]
    move_event_toggle = True
    pikachu = Pokemon("pika.png", "electric", -225, 255, 150, 150, pika_moves)
    move_counter = 0

    # create lapras object
    lapras_moves = [Move("Water Gun", True, 40, ["water", "flying"], ["ground"]),
                    Move("Water Pulse", True, 60, ["water", "flying"], ["ground"]),
                    Move("Hydro Pump", True, 90, ["water", "flying"], ["ground"]),
                    Move("Tackle", True, 10, ["water", "flying"], ["ground"])]
    lapras = Pokemon("lapras.png", "water", 700, 50, 150, 150, lapras_moves)

    # battle bars
    battle_bars = BattleBar()

    # hp event variables
    setup_hp = False

    # move settings
    my_move = pika_moves[0]
    opp_move = lapras_moves[0]
    final_move = True
    bar_animation_complete = True
    deduct_opp_hp = True
    deduct_my_hp = False
    my_start_hp = 0
    opp_start_hp = 0
    y_val = 0
    drawing_animation = False
    flip_count = 0
    pikachu_hp_animation = True

    # screen
    home_screen = True
    game_screen = False
    settings_screen = False
    battle_started = False
    fainted_screen = False
    end_screen = False
    end_screen_2 = False

    # main game loop
    while running:
        if game_screen:

            battle_music_start = play_battle_music(battle_music_start, music)
            battle_animation_sequence(screen, misty_event, misty_xloc, start_bas, misty)
            start_bas = False

            for event in pygame.event.get():
                if event.type == misty_event:
                    if misty_come:
                        player.xloc += 1
                        misty_xloc -= 1
                        draw_misty(screen, misty_xloc, misty)
                        player.draw(screen)
                        if misty_xloc < 400:
                            misty_come = False
                            misty_stay = True
                    if misty_stay:
                        battle_bars.draw(screen)
                        draw_misty(screen, misty_xloc, misty)
                        player.draw(screen)
                        misty_stay_count += 1
                        if misty_stay_count > 500:
                            battle_bars.erase(screen)
                            misty_stay = False
                            misty_leave = True
                    if misty_leave:
                        misty_xloc += 1
                        player.xloc -= 1
                        player.draw(screen)
                        draw_misty(screen, misty_xloc, misty)
                        if misty_xloc > 600:
                            misty_leave = False
                            pygame.time.set_timer(misty_event, 0)
                            pygame.time.set_timer(lapras_event, 1)
                            display_text(screen, "Gym Leader Misty sends out Lapras!")

                if event.type == lapras_event:
                    if lapras.xloc > 400:
                        lapras.set_xloc(lapras.xloc - 1)
                        pikachu.set_xloc(pikachu.xloc + 1)
                        lapras.show(screen)
                        pikachu.show(screen)
                        opponent_hp = HpMeter(140, 75, 160, 50, screen)
                        my_hp = HpMeter(300, 275, 160, 50, screen)
                    else:
                        lapras.show(screen)
                        pikachu.show(screen)
                        battle_started = True
                        game_screen = False
                        display_text(screen, "")
                        pygame.time.set_timer(lapras_event, 0)
                        # setup_hp = my_hp.deduct_hp(hp_event, screen, 30)
                        # my_hp.start_deduct = True

                if event.type == hp_event:
                    if setup_hp:
                        deduct = 0
                        setup_hp = False
                    if my_hp.start_deduct:
                        pygame.draw.rect(screen, (255, 255, 255), (my_hp.xloc + 150 - deduct, my_hp.yloc + 25, 1, 10))
                        if deduct == my_hp.deduct:
                            pygame.time.set_timer(hp_event, 0)
                            my_hp.start_deduct = False
                    if opponent_hp.start_deduct:
                        pygame.draw.rect(screen, (255, 255, 255), (opponent_hp.xloc + 150 - deduct, opponent_hp.yloc + 25, 1, 10))
                        if deduct == opponent_hp.deduct:
                            pygame.time.set_timer(hp_event, 0)
                            opponent_hp.start_deduct = False
                    deduct += 1

                if event.type == move_event:
                    move_counter += 1
                    if move_event_toggle:
                        screen.blit(current_move.image, (lapras.xloc, lapras.yloc))
                        move_event_toggle = False
                        pygame.display.flip()
                    else:
                        pygame.draw.rect(screen, (255, 255, 255), (lapras.xloc, lapras.yloc, 50, 100))
                        move_event_toggle = True
                        pygame.display.flip()
                    if move_counter > 6:
                        move_counter = 0
                        pygame.time.set_timer(move_event, 0)

                if event.type == pygame.QUIT:
                    running = False

        if home_screen:
            if game_start:
                screen.fill((255, 255, 255))
                screen.blit(main_logo, (150, 50))
                create_buttons(screen)
                start_music = play_start_music(start_music, music)
                game_start = False

            mouse = pygame.mouse.get_pos()
            if 210 < mouse[0] < (210 + 180) and 310 < mouse[1] < (310 + 50):
                pygame.draw.rect(screen, (0, 0, 0), (210, 310, 180, 50), 8)
            else:
                pygame.draw.rect(screen, (50, 205, 50), (210, 310, 180, 50), 8)
            """
            if 210 < mouse[0] < (210 + 180) and 370 < mouse[1] < (370 + 50):
                pygame.draw.rect(screen, (0, 0, 0), (210, 370, 180, 50), 8)
            else:
                pygame.draw.rect(screen, (255, 0, 0), (210, 370, 180, 50), 8)
            """
            click = pygame.mouse.get_pressed()
            if click[0] == 1:
                mouse = pygame.mouse.get_pos()
                if 210 < mouse[0] < (210 + 180) and 310 < mouse[1] < (310 + 50):
                    stop_start_music()
                    home_screen = False
                    game_screen = True
                """
                if 210 < mouse[0] < (210 + 180) and 370 < mouse[1] < (370 + 50):
                    home_screen = False
                    settings_screen = True
                """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == start_event:
                    pygame.draw.rect(screen, (255, 255, 255), (xloc, 150, 100, 120))
                    xloc -= 1
                    if xloc == 250:
                        pygame.time.set_timer(start_event, 0)
                    screen.blit(red, (xloc, 150))

        if settings_screen:
            screen.fill((255, 255, 255))
            mute = Button(screen, 225, 225, 150, 50, (124, 252, 0), "Mute", 32, 15, 17)
            back = Button(screen, 10, 10, 100, 30, (255, 0, 0), "Back", 10, 5, 17)
            settings_mouse = pygame.mouse.get_pos()

            print(settings_mouse)
            if 225 < mouse[0] < (225 + 150) and 225 < mouse[1] < (225 + 50):
                pygame.draw.rect(screen, (0, 0, 0), (225, 225, 150, 50))
            else:
                pygame.draw.rect(screen, (124, 252, 0), (225, 225, 150, 50))
            click = pygame.mouse.get_pressed()
            if click[0] == 1:
                mouse = pygame.mouse.get_pos()
                if 225 < mouse[0] < (225 + 150) and 225 < mouse[1] < (225 + 50):
                    stop_start_music()
                    if music:
                        music = False
                    else:
                        music = True

                if 10 < mouse[0] < (10 + 100) and 10 < mouse[1] < (10 + 30):
                    home_screen = True
                    settings_screen = False
                    game_start = True

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

        if battle_started:
            deduct_opp_hp = True
            deduct_my_hp = False
            my_start_hp = 0
            opp_start_hp = 0
            no_move_selected = True
            not_using_move = True
            my_move = pikachu.moves[0]
            while pikachu.hp > 0 and lapras.hp > 0:
                if not_using_move:
                    if no_move_selected:
                        display_moves(pikachu, screen)
                        mouse = pygame.mouse.get_pos()
                        if 35 < mouse[0] < 35 + 265 and 425 < mouse[1] < 425 + 70:
                            pygame.draw.rect(screen, (0, 0, 0), (35, 425, 265, 70), 8)
                        if 305 < mouse[0] < 305 + 260 and 425 < mouse[1] < 425 + 70:
                            pygame.draw.rect(screen, (0, 0, 0), (305, 425, 260, 70), 8)
                        if 35 < mouse[0] < 35 + 265 and 500 < mouse[1] < 500 + 70:
                            pygame.draw.rect(screen, (0, 0, 0), (35, 500, 265, 70), 8)
                        if 305 < mouse[0] < 305 + 260 and 500 < mouse[1] < 500 + 70:
                            pygame.draw.rect(screen, (0, 0, 0), (305, 500, 260, 70), 8)
                        click = pygame.mouse.get_pressed()
                        if click[0] == 1:
                            mouse = pygame.mouse.get_pos()

                            if 35 < mouse[0] < 35 + 265 and 425 < mouse[1] < 425 + 70:
                                no_move_selected = False
                                my_move = pikachu.moves[0]
                                opp_move = get_opponent_move(lapras)
                                my_start_hp = pikachu.hp
                                opp_start_hp = lapras.hp
                                use_moves(pikachu, lapras, my_move, opp_move, move_animation_event)
                                display_text(screen, "Pikachu used " + my_move.name + "!")
                                t.sleep(1)
                                thunder_sound_effect = pygame.mixer.Sound("pika_voice.wav")
                                pygame.mixer.Sound.play(thunder_sound_effect)
                                not_using_move = False
                                deduct_opp_hp = True
                            if 305 < mouse[0] < 305 + 260 and 425 < mouse[1] < 425 + 70:
                                no_move_selected = False
                                my_move = pikachu.moves[1]
                                opp_move = get_opponent_move(lapras)
                                my_start_hp = pikachu.hp
                                opp_start_hp = lapras.hp
                                use_moves(pikachu, lapras, my_move, opp_move, move_animation_event)
                                display_text(screen, "Pikachu used " + my_move.name + "!")
                                t.sleep(1)
                                thunder_sound_effect = pygame.mixer.Sound("pika_voice.wav")
                                pygame.mixer.Sound.play(thunder_sound_effect)
                                not_using_move = False
                                deduct_opp_hp = True
                            if 35 < mouse[0] < 35 + 265 and 500 < mouse[1] < 500 + 70:
                                no_move_selected = False
                                my_move = pikachu.moves[2]
                                opp_move = get_opponent_move(lapras)
                                my_start_hp = pikachu.hp
                                opp_start_hp = lapras.hp
                                use_moves(pikachu, lapras, my_move, opp_move, move_animation_event)
                                display_text(screen, "Pikachu used " + my_move.name + "!")
                                t.sleep(1)
                                thunder_sound_effect = pygame.mixer.Sound("pika_voice.wav")
                                pygame.mixer.Sound.play(thunder_sound_effect)
                                not_using_move = False
                                deduct_opp_hp = True
                            if 305 < mouse[0] < 305 + 260 and 500 < mouse[1] < 500 + 70:
                                no_move_selected = False
                                my_move = pikachu.moves[3]
                                opp_move = get_opponent_move(lapras)
                                my_start_hp = pikachu.hp
                                opp_start_hp = lapras.hp
                                use_moves(pikachu, lapras, my_move, opp_move, move_animation_event)
                                display_text(screen, "Pikachu used " + my_move.name + "!")
                                t.sleep(1)
                                thunder_sound_effect = pygame.mixer.Sound("pika_voice.wav")
                                pygame.mixer.Sound.play(thunder_sound_effect)
                                not_using_move = False
                                deduct_opp_hp = True


                    """
                    else:
                        opp_move = lapras.moves[0]
                        use_moves(pikachu, lapras, my_move, opp_move)
                        if pikachu.hp > 0 and lapras.hp > 0:
                            no_move_selected = True
                            my_hp.start_deduct = True
                            not_using_move = False
                            display_text(screen, "Pikachu used " + my_move.name + "!")
                            t.sleep(3)
                            thunder_sound_effect = pygame.mixer.Sound("tse.wav")
                            pygame.mixer.Sound.play(thunder_sound_effect)
                            hit_sound_effect = pygame.mixer.Sound("small_hit_sound_effect.wav")
                            pygame.mixer.Sound.play(hit_sound_effect)
                            setup_hp = opponent_hp.deduct_hp(hp_event, screen, my_move.damage)
                            opponent_hp.start_deduct = True
                            my_hp.start_deduct = False
                    """
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == move_animation_event:
                        if deduct_opp_hp:
                            opponent_hp.show(opp_start_hp)
                            opp_start_hp -= 1
                            if opp_start_hp < lapras.hp:
                                deduct_opp_hp = False
                                if lapras.hp > 0:
                                    deduct_my_hp = True
                                    display_text(screen, "Lapras used " + opp_move.name + "!")
                                    pygame.mixer.Sound.play(hit_sound_effect)
                                    t.sleep(2)

                        if deduct_my_hp:
                            my_hp.show(my_start_hp)
                            my_start_hp -= 1
                            if my_start_hp < pikachu.hp:
                                deduct_my_hp = False
                                pygame.time.set_timer(move_animation_event, 0)
                                not_using_move = True
                                no_move_selected = True
                                display_text(screen, "")

                    """
                    if event.type == hp_event:
                        if setup_hp:
                            deduct = 0
                            setup_hp = False
                            not_using_move = False
                        if opponent_hp.start_deduct:
                            pygame.draw.rect(screen, (255, 255, 255), (opponent_hp.xloc + 150 - deduct, opponent_hp.yloc + 25, 1, 10))
                            if deduct == my_hp.deduct:
                                opponent_hp.start_deduct = False
                                hit_sound_effect = pygame.mixer.Sound("small_hit_sound_effect.wav")
                                display_text(screen, "Lapras used " + opp_move.name + "!")
                                t.sleep(3)
                                display_text(screen, "")
                                pygame.mixer.Sound.play(hit_sound_effect)
                                var = my_hp.deduct_hp(hp_event, screen, opp_move.damage)
                                my_hp.start_deduct = True
                                deduct = 0
                        if my_hp.start_deduct:
                            pygame.draw.rect(screen, (255, 255, 255), (my_hp.xloc + 150 - deduct, my_hp.yloc + 25, 1, 10))
                            if deduct == my_hp.deduct:
                                pygame.time.set_timer(hp_event, 0)
                                my_hp.start_deduct = False
                                not_using_move = True
                        deduct += 1
                        """
                pygame.display.flip()
            battle_started = False
            fainted_screen = True

        if fainted_screen:

            if lapras.hp <= 0:
                # if drawing_animation:
                #    lapras.hide(screen)

                if bar_animation_complete:
                    if final_move:
                        y_val = lapras.yloc + lapras.height
                        # display_text(screen, "Pikachu used " + my_move.name + "!")
                        # t.sleep(1)
                        # thunder_sound_effect = pygame.mixer.Sound("tse.wav")
                        # pygame.mixer.Sound.play(thunder_sound_effect)
                        # hit_sound_effect = pygame.mixer.Sound("small_hit_sound_effect.wav")
                        # pygame.mixer.Sound.play(hit_sound_effect)
                        deduct_opp_hp = True
                        deduct_my_hp = False
                        pygame.time.set_timer(move_animation_event, 1)
                        final_move = False
                        bar_animation_complete = False
                    else:
                        display_text(screen, "Lapras Fainted!")
                        my_hp.hide()
                        opponent_hp.hide()
                        t.sleep(2)
                        pygame.time.set_timer(lapras_faint_event, 1)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == lapras_faint_event:
                        lapras.hide(screen)
                        lapras.yloc += 1
                        lapras.show(screen)
                        draw_white_box(screen, lapras.xloc, y_val, lapras.width, lapras.height)
                        if lapras.yloc >= y_val:
                            drawing_animation = False
                            pygame.time.set_timer(lapras_faint_event, 0)
                            fainted_screen = False
                            end_screen = True
                            screen.fill((255, 255, 255))
                            pygame.mixer.music.load("victory_music.mp3")
                            pygame.mixer.music.play(-1)

                    if event.type == move_animation_event:
                        if deduct_opp_hp:
                            opponent_hp.show(opp_start_hp)
                            opp_start_hp -= 1
                            if opp_start_hp < lapras.hp:
                                # opponent_hp.show_empty_meter()
                                deduct_opp_hp = False
                                bar_animation_complete = True
                                pygame.time.set_timer(move_animation_event, 0)
                        if deduct_my_hp:
                            my_hp.show(my_start_hp)
                            my_start_hp -= 1
                            if my_start_hp < pikachu.hp:
                                deduct_my_hp = False
                                pygame.time.set_timer(move_animation_event, 0)

            else:
                if pikachu_hp_animation:
                    pika_yloc = pikachu.yloc + pikachu.height + 20
                    deduct_opp_hp = True
                    deduct_my_hp = False
                    pikachu_hp_animation = False
                    pygame.time.set_timer(move_animation_event, 3)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == start_event:
                        pikachu.hide(screen)
                        pikachu.yloc += 1
                        pikachu.show(screen)
                        display_text(screen, "Pikachu Fainted!")
                        if pikachu.yloc > pika_yloc:
                            pygame.time.set_timer(start_event, 0)
                            fainted_screen = False
                            end_screen_2 = True
                            screen.fill((255, 255, 255))
                            display_text(screen, "Pikachu Fainted!")
                            pygame.mixer.music.load("victory_music.mp3")
                            pygame.mixer.music.play(-1)

                    if event.type == move_animation_event:
                        if deduct_opp_hp:
                            opponent_hp.show(opp_start_hp)
                            opp_start_hp -= 1
                            if opp_start_hp < lapras.hp:
                                display_text(screen, "Lapras used " + opp_move.name + "!")
                                t.sleep(1)
                                pygame.mixer.Sound.play(hit_sound_effect)
                                deduct_opp_hp = False
                                deduct_my_hp = True

                        if deduct_my_hp:
                            my_hp.show(my_start_hp)
                            my_start_hp -= 1
                            if my_start_hp < pikachu.hp:
                                deduct_my_hp = False
                                pygame.time.set_timer(move_animation_event, 0)
                                my_hp.hide()
                                opponent_hp.hide()
                                pygame.time.set_timer(start_event, 2)

        if end_screen_2:
            display_text(screen, "You have been defeated by Misty!")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        if end_screen:
            display_text(screen, "You have defeated Gym Leader Misty!")
            # pygame.display.flip()
            # t.sleep(3)
            # screen.fill((255, 255, 255))
            # display_text(screen, "Game Over!")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        flip_count += 1
        if flip_count > 100:
            pygame.display.flip()
            flip_count = 0


def draw_white_box(screen, x_val, y_val, width, height):
    pygame.draw.rect(screen, (255, 255, 255), (x_val, y_val, width, height))


def play_battle_music(battle_music, music):
    if music:
        if battle_music:
            pygame.mixer.music.load("battletheme.mp3")
            pygame.mixer.music.play(-1)
    return False


def play_start_music(start_music, music):
    if music:
        if start_music:
            pygame.mixer.music.load("startscreentheme.mp3")
            pygame.mixer.music.play(-1)
    return False


def stop_start_music():
    pygame.mixer.music.stop()
    return True


def create_buttons(screen):
    # Create start menu buttons
    # border


    green = (50, 205, 50)
    red = (255, 0, 0)

    start_btn = Button(screen, 210, 310, 180, 50, green, 'Start', 45, 15, 20)
    # settings_btn = Button(screen, 210, 370, 180, 50, red, 'Settings', 15, 15, 20)


def battle_animation_sequence(screen, event, misty_xloc, start_bas, misty):
    if start_bas:
        screen.fill((255, 255, 255))
        display_text(screen, "Gym Leader Misty wants to battle!")
        pygame.time.set_timer(event, 1)


def draw_misty(screen, misty_xloc, misty):
    pygame.draw.rect(screen, (255, 255, 255), (misty_xloc, 50, 150, 120))
    screen.blit(misty, (misty_xloc, 50))


def display_text(screen, text):
    textbox = pygame.image.load("blanktextbox.png")
    pygame.draw.rect(screen, (255, 255, 255), (0, 400, 600, 200))
    textbox = pygame.transform.scale(textbox, (600, 200))
    # sprite = pygame.sprite.Sprite()
    # sprite.image = textbox
    # sprite.rect = textbox.get_rect()

    # screen = screen.blit(textbox, (0, 400))
    if text == "":
        screen.blit(textbox, (0, 400))
        pygame.display.flip()
    else:
        textbox_image = pygame.image.load("blanktextbox.png")
        textbox_image = pygame.transform.scale(textbox, (600, 200))
        font = pygame.font.Font("PokemonGb-RAeo.ttf", 15)
        message = font.render(text, True, (0, 0, 0))
        image = pygame.Surface((500, 180), pygame.SRCALPHA)
        screen.blit(textbox_image, (0, 400))
        screen.blit(message, (40, 450))

        pygame.display.flip()


def display_moves(p, screen):
    # display_text(screen, "")
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 128, 0)
    yellow = (255, 255, 0)

    move_button_1 = Button(screen, 35, 425, 265, 70, red, p.moves[0].name, 50, 30, 15)
    move_button_2 = Button(screen, 305, 425, 260, 70, blue, p.moves[1].name, 75, 30, 15)
    move_button_3 = Button(screen, 35, 500, 265, 70, green, p.moves[2].name, 75, 30, 15)
    move_button_4 = Button(screen, 305, 500, 260, 70, yellow, p.moves[3].name, 50, 30, 15)


def get_opponent_move(p):
    rand_num = rnd.randint(0, 3)
    opp_move = p.moves[rand_num]
    return opp_move


def use_moves(p1, p2, my_move, opp_move, event):
    p2.hp = p2.hp - my_move.damage
    p1.hp = p1.hp - opp_move.damage
    pygame.time.set_timer(event, 3)


main()

